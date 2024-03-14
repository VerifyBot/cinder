"""
Decrator checks for routes.
These should be used under the @endpoints decorator.

Example:
  @endpoints.get('/me')
  @checks.authenticated()
  def me(ctx: endpoints.Contex):
    return dict(user=ctx.user.asdict())
"""

import functools
from network import router, errors
from .models import User

def authenticated():
  """
  Apply a check to see if the user is authenticated,
  based on whether a token is provided in the request headers.
  If it is, ctx.user will be available in the function.
  """

  def decorator(func):
    @functools.wraps(func)
    def wrapper(ctx: router.Context, *args, **kwargs):
      token = ctx.request.headers.get("Authorization")

      if not token:
        raise errors.NotAuthenticated(f"An Authorization header must be passed for this endpoint")

      query = "SELECT * FROM users WHERE token = ?"
      resp = User(ctx.db.execute(query, (token,)).fetchone())

      if resp is None:
        raise errors.NotAuthenticated("InvalidToken", "The token provided is invalid")

      # set ctx.user to the user object
      ctx.user = resp

      return func(ctx, *args, **kwargs)

    return wrapper

  return decorator
