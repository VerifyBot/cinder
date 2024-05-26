import dataclasses
import datetime
import json

from . import errors


@dataclasses.dataclass()
class Request:
  method: str
  path: str
  headers: dict
  data: dict | str
  params: dict

  @classmethod
  def from_raw(cls, raw: str):
    method = None
    path = None
    headers = {}
    data = {}
    params = {}

    POSSIBLE_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']

    find_next = None
    for i, ln in enumerate(raw.strip().split('\r\n')):
      if i == 0:
        method, path, _ = ln.split(' ')

        if method not in POSSIBLE_METHODS:
          raise errors.BadMessageError(f"Malformed HTTP request, not a known method.")

        # does path have params?
        if '?' in path:
          path, params = path.split('?')
          params = {k: v for k, v in [p.split('=') for p in params.split('&')]}

        find_next = 'headers'
        continue

      if find_next == 'headers':
        if ln == '':
          find_next = 'data'
          continue

        k, v = ln.split(': ')
        headers[k] = v
        continue

      if find_next == 'data':
        if headers.get('X-Client-Public-Key'):  # secure
            data = ln
            continue


        if headers['Content-Type'] == 'application/json':
          data = json.loads(ln)
          continue

        # print(ln)
        k, v = ln.split('=')
        data[k] = v
        continue

    return cls(method, path, headers, data, params)


@dataclasses.dataclass()
class Response:
  status: int = 200
  data: dict = dataclasses.field(default_factory=lambda: {"status": "ok"})
  headers: dict = dataclasses.field(default_factory=dict)

  def generate(self, secure: bool = False):
    """
    Generate the HTTP response
    """
    status_reason = {
      200: "OK",
      400: "Bad Request",
      401: "Unauthorized",
      404: "Not Found",
      500: "Internal Server Error",
    }.get(self.status, "Unknown")

    resp_headers = [
      f"HTTP/1.1 {self.status} {status_reason}",
      "Content-Type: application/json",
      f"Content-Length: {len(json.dumps(self.data)) if isinstance(self.data, dict) else len(self.data)}",
      f'Date: {datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z")} GMT+{datetime.datetime.now().astimezone().utcoffset().seconds // 3600}',
      "Server: Cinder",
      "Connection: close",
      "Access-Control-Allow-Origin: *",
      "Access-Control-Allow-Headers: *",
      "Access-Control-Allow-Methods: *",
    ]

    if self.headers:
      resp_headers += [f"{k}: {v}" for k, v in self.headers.items()]

    resp_headers = "\r\n".join(resp_headers)

    if isinstance(self.data, dict):
      resp_body = json.dumps(self.data) if self.data else ""
    else:
      resp_body = self.data

    to_send = f"{resp_headers}\r\n\r\n{resp_body}".encode()

    with open('dump.txt', 'wb') as f:
      f.write(to_send)

    return to_send

  @classmethod
  def from_error(cls, e: Exception):
    """
    Build the response for a given error
    """

    if isinstance(e, errors.RequestError):
      error = e
    else:
      error = errors.RequestError("An internal error occurred", cls="InternalError")

    return cls(200, error.to_dict())
    # return cls(e.status_code, error.to_dict())
