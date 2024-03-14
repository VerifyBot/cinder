import json
import random
from sqlite3 import Connection

from network.router import Context

from .base import BaseRecommendationService


def cosine_similarity(v1: list[int], v2: list[int]):
  """
  Calculate the cosine similarity of two vectors
  """

  assert len(v1) == len(v2), "Vectors must have the same length"

  dot_product = sum(v1[i] * v2[i] for i in range(len(v1)))
  magnitude1 = sum(v1[i] ** 2 for i in range(len(v1))) ** 0.5
  magnitude2 = sum(v2[i] ** 2 for i in range(len(v2))) ** 0.5

  return dot_product / (magnitude1 * magnitude2)


class AverageRecommendation(BaseRecommendationService):
  """
  This recommendation method takes into account only liked cars.
  It keeps a track of a user's liked cars vector (sum of all embeddings) and the count of liked cars rated.
  On the next recommendation, it will calculate the average of the liked cars vector and return the car with
  the closest embedding to that average, using the cosine similarity as the distance metric.

  Notes:
     (*) Cars will not be recommended twice.
     (*) If the user has not liked any cars, the recommendation will be random.
  """

  def __init__(self, cars: list[dict], db: Connection):
    self.cars = cars
    self.db = db

  def update(self, ctx: Context, car_id: int, like: bool):
    """
    Update the recommendation system with the user's choice
    :param car_id: The rated car
    :param like: Whether the user liked the car or not
    """

    if not like:
      return  # this method only cares about liked cars

    # make sure the car exists
    assert next((car for car in self.cars if car["id"] == car_id), None) is not None, "The car does not exist"

    # before updating the vector, make sure the car isn't already in the liked list
    query = """SELECT unique_liked_ids_array FROM users WHERE id = ?"""
    liked_ids = list(json.loads(self.db.execute(query, (ctx.user.id,)).fetchone()['unique_liked_ids_array']))

    if car_id in liked_ids:
      return  # ignore

    liked_ids.append(car_id)

    # update the liked cars vector
    query = """SELECT unique_liked_sum_vector FROM users WHERE id = ?"""
    sum_vector = json.loads(self.db.execute(query, (ctx.user.id,)).fetchone()['unique_liked_sum_vector']) \
                 or [0] * len(self.cars[0]["embedding"])

    # get the embedding of the car
    # print(self.cars)
    # print(str(car_id))
    # print(next(car for car in self.cars if car["id"] == car_id))
    car = json.loads(self.db.execute("SELECT embedding FROM cars WHERE id=?", (car_id,)).fetchone()['embedding'])
    #
    # assert all('embedding' in c for c in ctx.server.cars), f"All cars must have an embedding, {[c['name']+c['src'] for c in ctx.server.cars if not 'embedding' in c]} dont"
    #
    # car = next(car for car in self.cars if car["id"] == car_id)["embedding"]

    # update the sum vector
    for i, v in enumerate(car):
      sum_vector[i] += v

    # update the table
    query = """
    UPDATE users
    SET unique_liked_ids_array = ?,
        unique_liked_sum_vector = ?,
        unique_liked_count = unique_liked_count + 1
    WHERE id = ?
    """
    self.db.execute(query, (json.dumps(list(liked_ids)), json.dumps(sum_vector), ctx.user.id))

  def next(self, ctx: Context) -> dict:
    """
    Get the next car to show the user
    by measuring the cosine similarity of the average liked cars vector with the car embeddings.
    If the user has not liked any cars, the recommendation will be random.
    """

    # get the user's liked cars vector, and the count of liked cars
    query = """SELECT unique_liked_sum_vector, unique_liked_count FROM users WHERE id = ?"""

    resp = self.db.execute(query, (ctx.user.id,)).fetchone()
    sum_vector = json.loads(resp['unique_liked_sum_vector'])
    count = resp['unique_liked_count']

    if count == 0:
      # print('returning a random car')
      return random.choice(self.cars)

    # calculate the average vector
    avg_vector = [v / count for v in sum_vector]

    # calculate the cosine similarity of the average vector with the car embeddings
    # and return the car with the highest similarity, that hasn't been recommended yet

    # get the cars that the user has seen
    query = """SELECT car_id FROM users_swipes WHERE user_id = ?"""
    seen_cars = set(row['car_id'] for row in self.db.execute(query, (ctx.user.id,)))

    new_cars = list(car for car in self.cars if car["id"] not in seen_cars)

    # calculate the cosine similarity
    best_car = None

    for car in new_cars:
      similarity = cosine_similarity(avg_vector, car["embedding"])
      if best_car is None or similarity > best_car["similarity"]:
        best_car = {"car": car, "similarity": similarity}

    best_car = {"similarity": best_car["similarity"], **best_car["car"]}
    # print(f'returning {best_car}')
    return best_car
