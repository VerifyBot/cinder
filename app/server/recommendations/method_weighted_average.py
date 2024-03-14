import json
import random
from sqlite3 import Connection

from network.router import Context

from .base import BaseRecommendationService
from .method_average import AverageRecommendation, cosine_similarity


class WeightedAverageRecommendation(BaseRecommendationService):
  """
  Similar to the average recommendation, yet this method
  give higher weight to the most recent cars liked by the user.
  """

  def __init__(self, cars: list[dict], db: Connection):
    self.cars = cars
    self.cars_map = {car['id']: car for car in self.cars}

    self.db = db

  def update(self, ctx: Context, car_id: int, like: bool):
    return AverageRecommendation.update(self, ctx, car_id, like)

  def next(self, ctx: Context) -> dict:
    """
    Similar to the average recommendation, yet this method
    calculates the weighted average of the liked cars vector
    on this method and not in the update method. While this
    may cause a slight performance hit, it allows for a more
    flexible recommendation system.
    """

    # get the user's liked cars list
    query = """SELECT unique_liked_ids_array FROM users WHERE id = ?"""

    liked_ids = list(json.loads(self.db.execute(query, (ctx.user.id,)).fetchone()['unique_liked_ids_array']))
    liked_vectors = [self.cars_map[car_id]["embedding"] for car_id in liked_ids]

    if len(liked_vectors) == 0:
      # print('returning a random car')
      return random.choice(self.cars)


    # create a weighted average of the vectors as a single vector
    # the most recent cars will have a higher weight

    user_vector = [0] * len(liked_vectors[0])

    for i, vector in enumerate(liked_vectors):
      weight = (i + 1) / len(liked_vectors)
      user_vector = [user_vector[j] + vector[j] * weight for j in range(len(user_vector))]

    # normalize the vector
    user_vector = [v / len(liked_vectors) for v in user_vector]

    # calculate the cosine similarity of the average vector with the car embeddings
    # and return the car with the highest similarity, that hasn't been recommended yet

    # get the cars that the user has seen
    query = """SELECT car_id FROM users_swipes WHERE user_id = ?"""
    seen_cars = set(row['car_id'] for row in self.db.execute(query, (ctx.user.id,)))

    new_cars = list(car for car in self.cars if car["id"] not in seen_cars)

    # calculate the cosine similarity
    best_car = None

    for car in new_cars:
      similarity = cosine_similarity(user_vector, car["embedding"])
      if best_car is None or similarity > best_car["similarity"]:
        best_car = {"car": car, "similarity": similarity}

    best_car = {"similarity": best_car["similarity"], **best_car["car"]}

    return best_car
