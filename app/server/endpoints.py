import hashlib
import random
import re
import secrets
import sqlite3
import traceback
from typing import Optional

from utils.typehints import Regex
from utils import models
from utils import checks
from network import router, errors
from utils.story import create_story_for_nlp_embedding as car_story
from recommendations import supported_methods

# compile regex for valid username, email, password
valid_username = re.compile(r'^[a-zA-Z0-9_]{3,20}$'), \
  "must be 3-20 chars long and only contain letters, numbers and underscores"

valid_email = re.compile(r'^[a-zA-Z0-9_]+@[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+$'), \
  "must have a proper email format (ie: test@example.com)"

valid_password = re.compile(r'^.{4,}$'), \
  "must be at least 4 chars long"


def does_user_exist(ctx: router.Context, username: str = None, email: str = None):
  """
  Check if a user exists in the database. A user can be checked by either
  their username, email or both.
  :param ctx:
  """

  assert username is not None or email is not None, "username or email must be provided"

  query = "SELECT 1 FROM users WHERE {} = ?".format("username" if username else "email")
  return ctx.db.execute(query, (username or email,)).fetchone() is not None


@router.get('/test')
def test(ctx: router.Context, arg: Regex[(re.compile(r'a'), 'must be a')],
         arg2: Regex[(re.compile(r'b'), 'must be b')]):
  return dict(test="test", arg=arg, arg2=arg2)


@router.post('/signup')
def signup(
    ctx: router.Context,
    username: Regex[valid_username],
    email: Regex[valid_email],
    password: Regex[valid_password]
) -> dict:
  """
  Signup handler. This will sign up the user to the service and return a token
  that can be used to authenticate the user in future requests.
  """

  # check if username / email already exists
  if does_user_exist(ctx, username, email):
    raise errors.BadParameterError("AccountExists", "an account with that username or email already exists")

  # insert user to db. hash the password with a salt
  hashed_password = hashlib.sha256((password + ctx.config.get("secrets", "password_salt")).encode()).hexdigest()
  token = secrets.token_hex(32)

  add_user_query = "INSERT INTO users (username, email, password, token) VALUES (?, ?, ?, ?)"
  resp = ctx.db.execute(add_user_query, (username, email, hashed_password, token))

  user_id = resp.lastrowid

  return dict(user_id=user_id, token=token)


@router.post('/login')
def login(
    ctx: router.Context,
    username: Optional[Regex[valid_username]],
    email: Optional[Regex[valid_email]],
    password: Regex[valid_password]
) -> dict:
  """
  Login handler. This will log the user in and return a token that can be used
  A user can log in with either their username or email.
  """

  # check if username / email already exists
  if not does_user_exist(ctx, username, email):
    raise errors.BadParameterError("AccountMissing", "an account with that username or email does not exist")

  # check if the password matches
  hashed_password = hashlib.sha256((password + ctx.config.get("secrets", "password_salt")).encode()).hexdigest()

  query = "SELECT id, username, token FROM users WHERE {} = ? AND password = ?".format(
    "username" if username else "email")
  resp = models.User(ctx.db.execute(query, (username or email, hashed_password)).fetchone())

  if resp is None:
    raise errors.BadParameterError("WrongPassword", "the password provided is incorrect")

  return dict(user=resp.asdict(), token=resp.token)


@router.get('/me')
@checks.authenticated()
def me(ctx: router.Context):
  """
  me route. This will return the user's information.
  """

  # since we used the @authenticated decorator, we have ctx.user accessible
  return dict(user=ctx.user.asdict())


@router.get('/chats')
@checks.authenticated()
def chats(ctx: router.Context):
  """
  Chats routes. This will return the user's chats with the bot
  """
  # select all user's opened chats
  chats_query = "SELECT * FROM chats WHERE user_id = ? ORDER BY created_at DESC"
  chats = [
    models.Chat(chat)
    for chat in
    ctx.db.execute(chats_query, (ctx.user.id,)).fetchall()]
  return dict(chats=[chat.asdict() for chat in chats])

  return [dict(name=f"Car Manager {ctx.user.username}", related_car_name="Cacdila 10v (improved)")]


@router.get('/chat')
@checks.authenticated()
def chat(ctx: router.Context, car_id: int):
  """
  Chat route. This will return the chat's messages.
  """
  chat_query = "SELECT * FROM chats WHERE user_id = ? AND car_id = ?"
  chat = models.Chat(ctx.db.execute(chat_query, (ctx.user.id, car_id)).fetchone())

  if chat is None:
    raise errors.BadParameterError("UnknownChat", "the chat with the provided id does not exist")

  messages_query = "SELECT * FROM messages WHERE chat_id = ? ORDER BY id"
  messages = [
    models.Message(message)
    for message in
    ctx.db.execute(messages_query, (chat.id,)).fetchall()]

  return dict(chat=chat.asdict(), messages=[message.asdict() for message in messages],
              car=next(c for c in ctx.server.cars if c['id'] == car_id))


@router.post('/swipe')
@checks.authenticated()
def swipe(ctx: router.Context, car_id: int, like: bool):
  """
  Swipe route, to like or dislike a car.
  This will update the recommendation system with the user's choice.
  To get the next car, call the /car route.
  """

  car_exists_query = "SELECT 1 FROM cars WHERE id = ?"
  if ctx.db.execute(car_exists_query, (car_id,)).fetchone() is None:
    raise errors.BadParameterError("UnknownCar", "the car with the provided id does not exist")

  # update users_swipes, on conflict update the liked value
  update_swipe_query = "INSERT INTO users_swipes (user_id, car_id, liked) VALUES (?, ?, ?) ON CONFLICT (user_id, car_id) DO UPDATE SET liked = ?"
  ctx.db.execute(update_swipe_query, (ctx.user.id, car_id, like, like))
  ctx.recommendation_update(car_id, like)  # update the recommendation system

  # create a new chat (20% if rated like=True on more than 5 cars otherwise 0%)
  if like and random.random() < 0.2:
    # create a new chat
    # logging.info("CREATING A NEW CHAT")

    try:
      _car = next(c for c in ctx.server.cars if c['id'] == car_id)
      new_chat_query = "INSERT INTO chats (user_id, car_id, car_name, car_img) VALUES (?, ?, ?, ?)"
      ctx.db.execute(new_chat_query, (ctx.user.id, car_id, f"{_car['company']} {_car['name']}", _car['image']))

      resp = ctx.db.execute("SELECT * FROM chats WHERE user_id = ? AND car_id = ?", (ctx.user.id, car_id)).fetchone()
      # print(f'{dict(resp)=}')
      chat = models.Chat(
        resp
      )
      # print(f'{chat=}')
      # print(chat.id)

      # insert a message from the bot
      new_message_query = "INSERT INTO messages (chat_id, is_bot, content) VALUES (?, ?, ?)"
      ctx.db.execute(new_message_query, (chat.id, True, random.choice([
        "Hey there! I see you liked this car, do you want to know more about it? 😊",
        "Hello! I think we have a match, do you have any questions about this car? 😊",
        "Hi! I think that car is a great choice, do you want to know more about it? 😊"
      ])))

      return dict(chat=chat.asdict(), new_chat=True)
    except sqlite3.IntegrityError as e:
      traceback.print_exc()
      pass  # chat already exists


@router.get('/car')
@checks.authenticated()
def car(ctx: router.Context):
  """
  return the next car to show the user, and possibly create a new chat.

  Returns:
    {
      car: Car,  # the next car to show the user
      chat: Optional[Chat],  # the chat that was created, if it was
      chat_reminder: Optional[bool]  # if a chat already existed with the car, and the odds were in favor of creating a new chat, this will be True
                                     # on the client side, make sure to remind them that the bot wants to talk
    }
  """

  car = {**ctx.recommendation_next()}

  car.pop("embedding")  # don't send the embedding to the client

  # load the car image
  car['image'] = ctx.load_image(car['id'])

  return car


@router.post('/send')
@checks.authenticated()
def send(ctx: router.Context, car_id: int, content: str):
  """
  Send a message to the bot (car manager - chatpt), and get a response.
  """
  chat_query = "SELECT * FROM chats WHERE user_id = ? AND car_id = ?"
  chat = models.Chat(ctx.db.execute(chat_query, (ctx.user.id, car_id)).fetchone())

  if chat is None:
    raise errors.BadParameterError("UnknownChat", "the chat with the provided id does not exist")

  new_message_query = "INSERT INTO messages (chat_id, is_bot, content) VALUES (?, ?, ?)"
  ctx.db.execute(new_message_query, (chat.id, False, content))

  # write a response...
  resp = ctx.chatgpt.ask(
    f"""
    {ctx.server.system_prompt}
    Here is the car's information:
    {car_story(next(c for c in ctx.server.cars if c['id'] == car_id))}
    
    Here is the question:
    {content}
    """, convo_id=f'C{ctx.user.id}I{chat.id}N{car_id}D')

  ctx.db.execute(new_message_query, (chat.id, True, resp))

  query = "SELECT * FROM messages WHERE chat_id = ? ORDER BY id DESC LIMIT 1"
  new_message = models.Message(ctx.db.execute(query, (chat.id,)).fetchone())

  return dict(message=new_message.asdict())


@router.get('/method')
@checks.authenticated()
def method_get(ctx: router.Context):
  """
  Get the user's recommendation method
  """
  query = "SELECT recommendation_method FROM users WHERE id = ?"
  method = ctx.db.execute(query, (ctx.user.id,)).fetchone()['recommendation_method']

  return dict(method=method)


@router.post('/methodChange')
@checks.authenticated()
def method_change(ctx: router.Context):
  """
  Change the user's recommendation method
  """

  query = "SELECT recommendation_method FROM users WHERE id = ?"
  method = ctx.db.execute(query, (ctx.user.id,)).fetchone()['recommendation_method']

  next_method = supported_methods[(supported_methods.index(method) + 1) % len(supported_methods)]

  query = "UPDATE users SET recommendation_method = ? WHERE id = ?"
  ctx.db.execute(query, (next_method, ctx.user.id))

  return dict(method=next_method)


@router.post('/recommendationReset')
@checks.authenticated()
def recommendation_reset(ctx: router.Context):
  """
  Reset the user's recommendation system
  """

  query = "DELETE FROM users_swipes WHERE user_id = ?"
  ctx.db.execute(query, (ctx.user.id,))
  query = "UPDATE users SET unique_liked_ids_array = '[]', unique_liked_sum_vector = '[]', unique_liked_count = 0 WHERE id = ?"
  ctx.db.execute(query, (ctx.user.id,))

  return


@router.post('/clearChats')
@checks.authenticated()
def clear_chats(ctx: router.Context):
  """
  Clear all the user's chats
  """

  query = "DELETE FROM chats WHERE user_id = ?"
  ctx.db.execute(query, (ctx.user.id,))

  return

@router.post('/reverse')
def reverse(ctx: router.Context, text: str) -> dict:
  """
  Reverse the provided string.
  """
  print(f'On reverse({text})')
  return dict(reversed=text[::-1])