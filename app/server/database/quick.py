import json
from sqlite3 import Connection, Row

def load_cars(db: Connection, query: str) -> list[dict]:
  """
  Load the cars from the database, and return a list of dicts.
  """

  cars: list[Row] = db.execute(query).fetchall()

  cars = [
    {"id": car["id"], "name": car["name"], "embedding": json.loads(car["embedding"]), **json.loads(car["attrs"]), "src": "load"}
    for car in cars
  ]

  # todo: FIND A DIFFERENT SOLUTION :P
  # don't include duplicated cars.
  cars = [car for car in cars if not car.get('duplicate', False)]

  return cars