class RequestError(Exception):
  """The base class for all request errors"""

  def __init__(self, *args, **kwargs):
    if len(args) > 1:
      kwargs['cls'] = args[0]
      args = args[1:]

    if (cls := kwargs.pop('cls', None)) is not None:
      self.__class__.__name__ = cls

    # set the status code
    # 1. get it from kwargs
    # 2. get it from the subclass class varaible
    # 3. default to 500
    self.status_code = kwargs.pop('status_code', getattr(self.__class__, 'status_code', 500))

    super().__init__(*args, **kwargs)

  def to_dict(self):
    return dict(
      error=self.__class__.__name__,
      message=str(self),
      ok=False
    )


class DisconnectedError(Exception):
  """
  Raised when a client disconnects during Recv()
  """


class BadMessageError(RequestError):
  """
  Raised when a client sends a bad message
  """
  status_code = 400


class NotFoundError(RequestError):
  """
  Raised when a client tries to access a non-existent path
  """
  status_code = 404


class MissingParameterError(RequestError):
  """
  Raised when a client does not provide all required parameters
  """
  status_code = 400


class NotAuthenticated(RequestError):
  """
  Raised when a client tries to access an endpoint that requires authentication
  """
  status_code = 401


class MethodNotAllowedError(RequestError):
  """
  Raised when a client tries to access an endpoint with an invalid method
  """
  status_code = 405

class BadParameterError(RequestError):
  """
  Raised when a client provides a parameter with an invalid value
  """
  status_code = 400