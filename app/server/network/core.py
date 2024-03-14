import contextlib
import inspect
import socket
import threading
import logging
import dataclasses
import uuid
from configparser import ConfigParser
import base64

import coloredlogs
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from . import errors
from .protocol import Request, Response
from . import router


@dataclasses.dataclass()
class Client:
  socket: socket.socket
  address: tuple[str, int]
  thread: threading.Thread
  id: str = None

  def __post_init__(self):
    self.id = uuid.uuid4().hex

  def __str__(self):
    return f"Client(id={self.id}, host={self.address[0]}, port={self.address[1]}, thread={self.thread.ident})"


@dataclasses.dataclass()
class SecureConnection:
  # 0 = not started, 1 = started, 2 = finished
  handshake_state: int = 0
  public_key: RSA.RsaKey = None
  cipher_rsa: PKCS1_OAEP.PKCS1OAEP_Cipher = None
  secure_token: bytes = None
  aes_cipher = None


class Server:
  """
  A rich HTTP server

  :param host: The host to bind to
  :param port: The port to bind to
  :param config: The config file
  :param secure: Enable public/private key encryption
  :param debug: Enable debug mode
  """

  def __init__(self, host: str, port: int, config: ConfigParser, secure: bool = False, debug: bool = True):
    self.host = host
    self.port = port
    self.config = config
    self.secure = secure

    # setup logging
    coloredlogs.install(level=logging.DEBUG if debug else logging.INFO)

    self.endpoints = {}

    if self.secure:
      self.add_endpoint('/handshake', self.handshake_endpoint)

    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # allows the reuse of the address so that if the server was killed unexpectedly
    # it can be restarted without waiting for the OS to release the port
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
      self.socket.bind((host, port))
    except OSError as e:
      logging.exception(f"Failed to bind to {host}:{port}. Port is perhaps unavailable", exc_info=e)

    # allow up to 20 clients to wait in the queue to be accepted
    self.socket.listen(50)

    self.clients: list[Client] = []
    self.threads: list[threading.Thread] = []

    self.secure_connections: dict[str, SecureConnection] = {}

    self._kill_signal = False

  @staticmethod
  @router.post('/handshake')
  def handshake_endpoint(ctx: router.Context, public_key: str):
    """
    The client sends its public key to the server to start the handshake
    The server responds with their public key and encrypts a token with the client's public key
    """
    if not ctx.server.secure:
      return dict(secure_required=False)

    public_key = ctx.request.headers.get('X-Client-Public-Key')

    secure_client = ctx.server.secure_connections.get(public_key)

    if secure_client is not None:
      raise errors.BadMessageError("This public key is already used in a session.")

    secure_client = SecureConnection(...)
    return dict(secure_token=...)

  def add_endpoint(self, path: str, handler: callable):
    """
    Add an endpoint to the server
    """
    if path in self.endpoints:
      logging.exception(f"Path {path} is already handled by {self.endpoints[path]}")
      return

    self.endpoints[path] = handler

  def load_endpoints_from_module(self, module):
    """
    Load the endpoints from a module
    """
    for name, obj in inspect.getmembers(module, inspect.isfunction):
      if not hasattr(obj, '__endpoint__'):
        # print(f"Skipping {name} because it has no __endpoint__ attribute")
        continue

      logging.debug(f"Loading endpoint {name} from {module.__name__} to handle {getattr(obj, '__endpoint__')}")
      self.add_endpoint(getattr(obj, '__endpoint__'), obj)

  def listen(self):
    while True:
      client_socket, client_address = self.socket.accept()

      if len(self.clients) >= 1000:
        logging.warning(f"Rejecting connection from {client_address} because the server is full")
        client_socket.close()
        continue

      logging.debug(f"Accepted connection from {client_address}")

      # create a thread for the new client
      client = Client(
        socket=client_socket, address=client_address,
        thread=threading.current_thread()
      )
      client_thread = threading.Thread(target=self.handle_client, args=(client,))

      self.clients.append(client)

      client_thread.start()

      self.threads.append(client_thread)

  def run(self):
    """
    Run the server
    """
    logging.info(f"Server is listening on {self.host}:{self.port}")

    try:
      self.listen()
    except KeyboardInterrupt:
      logging.info("Ctrl+C detected, closing server.")
      self.close()

  def read_all(self, sock: socket.socket):
    """
    Read all the data from the socket
    """
    data = b''

    sock.settimeout(0.01)
    with contextlib.suppress(socket.timeout):
      while True:
        new = sock.recv(1024)

        if not new:
          raise errors.DisconnectedError("Client disconnected")

        data += new

        if new.endswith(b'\r\n\r\n'):
          break

    return data

  def before_handle(self, ctx):
    """
    Called before sending the request to the handler
    """
    return

  def after_handle(self, ctx, response):
    """
    Called after the handler returns
    """
    return

  def override_response(self, ctx, response):
    """
    Override the response
    """
    return response

  def handle_client(self, client: Client):
    """
    Handle a client's request
    """

    try:
      raw_request = self.read_all(client.socket)

      if not raw_request:
        raise errors.DisconnectedError()

      try:
        request: Request = Request.from_raw(raw_request.decode('utf-8'))
      except Exception as e:
        logging.error(f"Failed to parse request from {client}:", exc_info=e)
        raise errors.BadMessageError("Malformed HTTP request") from e

      public_key = request.headers.get('X-Client-Public-Key')

      if self.secure:
        if public_key is None:
          raise errors.BadMessageError(
            "A public key is required in order to communicate with the server. Please attach it via a X-Client-Public-Key header."
          )

        if request.path != '/handshake':
          if not (conn := self.secure_connections.get(public_key)):
            raise errors.BadMessageError("You must complete the handshake via /handshake before sending requests.")

          # decrypt the request using the aes key in conn
          request.data = json.loads(conn.aes_cipher.decrypt(base64.b64decode(request.data)).decode('utf-8'))

      context: router.Context = router.Context(request=request, client=client, server=self, db=self.db,
                                               config=self.config)

      # who shall handle this request?
      # logging.info(f'Trying {request.path} against {self.endpoints}')

      handler = self.endpoints.get(request.path)

      if handler is None:
        raise errors.NotFoundError(f"unknown endpoint")

      # before handling
      self.before_handle(context)

      # handle the request
      logging.debug(f'Sent {request.path} to {handler} with {context}')

      response: Response = handler(context)

      # after handling
      self.after_handle(context, response)

      # override the response
      response = self.override_response(context, response)

      if self.secure and request.path != '/handshake':
        conn = self.secure_connections.get(public_key)

        # encrypt the response using the aes key in conn
        response.data = base64.b64encode(conn.aes_cipher.encrypt(json.dumps(response.data).encode('utf-8'))).decode(
          'utf-8')

      # send the response
      client.socket.sendall(response.generate())

    except errors.MethodNotAllowedError as e:  # no need to log this one, chrome sends a lot of these
      client.socket.sendall(Response.from_error(e).generate())
    except errors.BadMessageError as e:
      logging.debug(f"Client {client} sent bad message -> {e}")
      client.socket.sendall(Response.from_error(e).generate())
    except errors.RequestError as e:
      logging.debug(f"Request error for {client} -> {e}", exc_info=e)
      client.socket.sendall(Response.from_error(e).generate())
    except errors.DisconnectedError:
      logging.debug(f"Client {client} disconnected during recv()")
    except socket.error as e:
      logging.debug(f"Socket Error exit client for {client}:", exc_info=e)
      client.socket.sendall(Response.from_error(e).generate())
    except Exception as e:
      logging.error(f"General Error exit client for {client}:", exc_info=e)
      client.socket.sendall(Response.from_error(e).generate())

    client.socket.close()
    self.clients.remove(client)
    logging.debug(f"Finished transaction with {client}")

  def close(self):
    """
    Close the server
    """
    self._kill_signal = True

    for thread in self.threads:
      thread.join()

    self.socket.close()
    logging.info("Goodbye. 😴")
