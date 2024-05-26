import abc
from sqlite3 import Connection

from network.router import Context


class BaseRecommendationService(abc.ABC):
  """
  Base class for recommendation services

  Required implementations:
    - __init__ (accepts cars and db)
    - update (accepts a context, car_id, like)
    - next (accepts a context)
  """

  @abc.abstractmethod
  def __init__(self, cars: list[dict], db: Connection):
    pass

  @abc.abstractmethod
  def update(self, ctx: Context, car_id: int, like: bool):
    """
    Update the recommendation system with the user's choice
    :param car_id: The rated car
    :param like: Whether the user liked the car or not
    """
    pass

  @abc.abstractmethod
  def next(self, ctx: Context):
    """
    Get the next car to show the user
    based on the recommendation system
    """
    pass
