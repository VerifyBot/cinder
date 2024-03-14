import re
import inspect
import typing


class ValidationError(Exception):
  pass


class Regex:
  """
  A regex typehint validator for routes.
  It will run the regex against the value and raise a ValidationError if it doesn't match

  Usage:
  @router.post('/login')
  def login(
      ctx: router.Context,
      username: Optional[regex(r"[a-zA-Z]+")],
      email: Optional[regex(r"[a-zA-Z]+")],
      password: regex(r"[a-zA-Z]+")
  ) -> dict:
    pass
  """

  def __init__(self, regex, error_msg=None):
    self.regex = regex
    self.error_msg = error_msg

  def __call__(self):
    pass

  def __or__(self, rhs):
    return typing.Union[self, rhs]

  def __class_getitem__(cls, item):
    if isinstance(item, tuple):
      return cls(regex=item[0], error_msg=item[1])
    return cls(regex=item)

  def convert(self, value):
    if not re.fullmatch(self.regex, str(value)):
      raise ValidationError(self.error_msg or f"Invalid value {value} for matching - {self.__error_msg__}")
    return value


def validate_annotations(func, data: dict):
  """
  Validates the annotations of a function against the data provided
  Returns: the new data (with the transformed values), the missing parameters and the parameters with wrong types
  """
  params = inspect.signature(func).parameters  # function signature {param: typehint}

  # collect errors
  missing, wrong_type = set(), set()

  # print(f'{func=} got {data=}, required: {params=}')

  rdata = {}
  for i, (param, hint) in enumerate(params.items()):
    if i == 0:  # context
      continue


    ann = hint.annotation

    # print(f'running on {param=} with {ann=}')

    has_default = params[param].default != inspect._empty
    is_optional = typing.get_origin(ann) is typing.Union and type(None) in typing.get_args(ann)
    # print(f'{has_default=} {is_optional=} {data.get(param)=}')

    if (param not in data) or (data.get(param) is None and is_optional):  # is provided?
      # is it optional? (has a default value or typing.Optional)
      if has_default or is_optional:
        rdata[param] = None if hint.default == inspect._empty else hint.default
        # print(f'calling {param} as default because it has {data.get(param)=}')
        continue
      #
      # print(f'problem with {param}')
      th = f'type {ann.__name__}' if not hasattr(ann, 'error_msg') else ann.error_msg
      missing.add(f"{param} ({th})")
      continue

    # it might be typing.Optional but the value is not None, so let's get the converter inside it
    if is_optional:
      ann = typing.get_args(ann)[0]

    # has a convert method (validator)
    if hasattr(ann, 'convert'):
      try:
        rdata[param] = ann.convert(data[param])
      except ValidationError as e:
        wrong_type.add(f'{param} {e}')
    else:
      try:
        if typing.get_origin(ann) is typing.Union:
          # print(f'{ann=} {typing.get_args(ann)=} {data} {data[param]}')
          rdata[param] = typing.get_args(ann)[0](data[param])
        else:
          rdata[param] = ann(data[param])
      except ValueError:
        wrong_type.add(f'{param} must be of type {ann.__name__}')

  return rdata, missing, wrong_type
