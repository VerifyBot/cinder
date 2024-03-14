import functools
import logging
import typing

from utils import typehints
from .protocol import Response, Request
from . import errors

from configparser import ConfigParser
from sqlite3 import Connection

if typing.TYPE_CHECKING:
  from .core import Server, Client


class Context:
  """
  Context object passed to handlers

  The context contains the request information,
  the client that sent the request, the server
  and the database connection.
  """

  def __init__(self, request: Request, client: 'Client', server: 'Server', db: Connection, config: ConfigParser):
    self.request = request
    self.client = client
    self.server = server
    self.db = db
    self.config = config

    self.response: Response = Response(status=200, data={}, headers={})

  @property
  def handler(self):
    return self.server.endpoints.get(self.request.path)


def route(path: str, method: str):
  """
  Decorator for requests
  :param path: the path to bind to
  """

  def decorator(func):
    @functools.wraps(func)
    def wrapper(ctx: Context):
      if ctx.request.method != method:
        raise errors.MethodNotAllowedError(f"request method is not allowed for this endpoint")

      data = ctx.request.params if method == 'GET' else ctx.request.data

      new_data, missing, wrong_types = typehints.validate_annotations(func, data)


      if missing:
        raise errors.MissingParameterError(
          f"Request expected {'url parameter(s)' if method == 'GET' else 'json object'}: {', '.join(missing)}")

      if wrong_types:
        raise errors.BadMessageError(
          # f"Improper value for {'url parameter(s)' if method == 'GET' else 'json object'}: {', '.join(wrong_types)}"
          ', '.join(wrong_types)

        )


      try:
        func_resp = func(ctx, **new_data) or {}
      except errors.RequestError as e:
        raise e
      except Exception as e:
        logging.error("Error in handler", exc_info=e)
        raise errors.RequestError(str(e), cls=e.__class__.__name__) from e

      resp = ctx.response
      resp.data = dict(data=func_resp, ok=True)
      # print(path, 'RETURNED', resp)
      return resp

    wrapper.__endpoint__ = path
    wrapper.__method__ = method
    return wrapper

  return decorator


def post(path: str):
  """
  Decorator for POST requests
  :param path: the path to bind to

  Usage:
  @router.post('/login')
  def login(ctx, ...data):
    pass
  """
  return route(path, 'POST')


def get(path: str):
  """
  Decorator for GET requests
  :param path: the path to bind to

  Usage:
  @router.get('/info')
  def info(ctx, ...params):
    pass
  """
  return route(path, 'GET')
