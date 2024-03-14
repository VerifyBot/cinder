import dataclasses
import datetime


def maybe_dataclass(cls):
  """
   A Dataclass decorator that might get None instead of a dict
  in that case, it will just return None and not a class.

  This is useful because the sqlite library returns None if no rows are found,
  and a tuple of the values if a row is found.

  Any param that is in the dataclass but not in the dict, it will be set to None.
  """

  def wrapper(*args, **kwargs):
    # print(f'{args=} {kwargs=}')
    if (not kwargs and not args) or (args and not args[0]):
      return None

    # then the first arg is the dict
    if not kwargs:
      kwargs = dict(args[0])


    ann = cls.__annotations__

    for req in ann.keys():
      if req not in kwargs:
        kwargs[req] = None

    cls.asdict = lambda it: {k: v for k, v in dataclasses.asdict(it).items() if v is not None}

    for k, v in ann.items():
      if isinstance(v, datetime.datetime):
        kwargs[k] = datetime.datetime.fromisoformat(kwargs[k])

    # print(f'{kwargs=}')

    # ignore all unexpceted kwargs
    kwargs = {k: v for k, v in kwargs.items() if k in ann}

    return dataclasses.dataclass(cls, kw_only=True)(**kwargs)

  return wrapper


@maybe_dataclass
class User:
  id: int
  username: str
  email: str
  password: str
  token: str
  created_at: datetime.datetime


@maybe_dataclass
class Chat:
  id: int
  car_id: int
  car_name: str
  car_img: str
  created_at: datetime.datetime
  first_read: bool

@maybe_dataclass
class Message:
  id: int
  chat_id: int
  is_bot: bool
  content: str
  created_at: datetime.datetime

if __name__ == "__main__":
  # assert User() is None
  print(User(id=1))
  print(User(**{
    "id": 1,
    "username": "test",
    "email": "trest",
    "password": "test",
    "token": "test",
    "created_at": datetime.datetime.now()
  }))
