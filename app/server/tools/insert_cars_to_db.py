import os.path
import sqlite3
from sqlite3 import Connection
import json
import logging

import coloredlogs

coloredlogs.install(level="INFO")


def main(cars: list[dict], conn: Connection):
  """
  Insert the cars data into the database.
  """

  try:
    conn.execute("SELECT 1 FROM cars").fetchone()
  except sqlite3.OperationalError:
    raise Exception('The database does not seem to be set up. Run setupdb.py file first.')

  # insert the cars
  logging.info("Inserting cars data...")

  insert_data = []

  conn.execute("DELETE FROM cars")

  for car in cars:
    insert_data.append((
      int(car.pop('id')),
      car.pop('name'),
      json.dumps(car.pop('embedding')),
      json.dumps(car)
    ))

  conn.executemany("INSERT INTO cars (id, name, embedding, attrs) VALUES (?, ?, ?, ?)", insert_data)

  conn.commit()

  logging.info(f"🚗 Inserted {len(insert_data)} cars into the database.")



if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser(description='Insert cars to the database')
  parser.add_argument('--cars', default='../../data/carsDataEmbeddingDuplicatedMark.json', help='Path to the cars data file')
  parser.add_argument('--db', default='cinder.db', help='Path to the database file')

  args = parser.parse_args()

  assert os.path.exists(args.cars), f'Cars data file not found in {os.path.abspath(args.cars)}'
  assert os.path.exists(args.db), f'Database file not found in {os.path.abspath(args.db)}'

  logging.info("Loading cars data...")
  with open(args.cars, 'r', encoding='utf8') as f:
    cars = json.load(f)

  logging.info("Connecting to the database...")
  conn = sqlite3.connect(args.db)

  main(cars, conn)

  conn.close()
