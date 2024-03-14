import os.path
import sqlite3
import typing
from sqlite3 import Connection
import logging
import argparse

import coloredlogs

coloredlogs.install(level="INFO")


class Tables:
  users = """
  CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    created_at DATE DEFAULT (datetime('now', 'localtime')),
    
    token TEXT NOT NULL,
    
    recommendation_method TEXT DEFAULT 'average',
    
    unique_liked_ids_array TEXT DEFAULT '[]',
    unique_liked_sum_vector TEXT DEFAULT '[]',
    unique_liked_count INTEGER DEFAULT 0
    
  )
  """

  cars = """
  CREATE TABLE cars (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    embedding TEXT NOT NULL,
    attrs TEXT NOT NULL
  )
  """

  users_swipes = """
  CREATE TABLE users_swipes (
    user_id INTEGER NOT NULL,
    car_id INTEGER NOT NULL,
    liked BOOLEAN NOT NULL,
    marked_at DATE DEFAULT (datetime('now', 'localtime')),
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (car_id) REFERENCES cars(id),
    PRIMARY KEY (user_id, car_id)
  )
  """

  chats = """
  CREATE TABLE chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    car_id INTEGER NOT NULL,
    car_name TEXT NOT NULL,
    car_img TEXT NOT NULL,
    created_at DATE DEFAULT (datetime('now', 'localtime')),
    first_read BOOLEAN DEFAULT FALSE,  -- a default welcome message is sent by the bot, this is the only time we need a is-read flag
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (car_id) REFERENCES cars(id),
    UNIQUE (user_id, car_id)
  )
  """

  messages = """
  CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER NOT NULL, 
    is_bot BOOLEAN NOT NULL,
    content TEXT NOT NULL,
    created_at DATE DEFAULT (datetime('now', 'localtime')),
    
    FOREIGN KEY (chat_id) REFERENCES chats(id)
  )
  """

def setup_tables(conn: Connection, drop: typing.Union[bool, list[str]]):
  for table_name, setup_query in {k: v for k, v in Tables.__dict__.items() if not k.startswith("__")}.items():
    # drop it fist
    if (isinstance(drop, bool) and drop) or (isinstance(drop, list) and table_name in drop):
      conn.execute(f"DROP TABLE IF EXISTS {table_name}")

    try:
      conn.execute(setup_query)
      logging.info(f"✏️ Created table {table_name}")
    except sqlite3.OperationalError as e:
      if 'already exists' not in str(e.args[0]):
        logging.error(f"⚠️ Failed to create table {table_name}", exc_info=e)


if __name__ == '__main__':
  argparse = argparse.ArgumentParser()
  argparse.add_argument("--db-path", default="cinder.db", help="The path to the database file")

  args = argparse.parse_args()
  DB_PATH = args.db_path

  if os.path.exists(DB_PATH):
    logging.warning(f"🙀 Database file {DB_PATH} already exists. Do you want to set it up again? (y/n)")
    if input().lower() != 'y':
      logging.info("👋🏼 Goodbye.")
      exit(0)
  else:
    logging.info(f"📝 Creating database in {DB_PATH}...")

  conn: Connection = sqlite3.connect("cinder.db")
  setup_tables(conn, drop=['users'])