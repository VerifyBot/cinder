import base64
import functools
import logging
import os.path
import sqlite3
import configparser

from revChatGPT.V3 import Chatbot

from network import Server, router
import endpoints
from database.sqlite_safe import SafeConnection
from database.quick import load_cars
from recommendations import AverageRecommendation, WeightedAverageRecommendation


def load_car_image(ctx: router.Context, car_id: int) -> bytes:
  """
  Load the image of a car from the database
  """

  fn = os.path.join(ctx.config['paths']['cars_images'], f"{car_id}.png")
  # print(fn)
  with open(fn, "rb") as fp:
    return base64.b64encode(fp.read()).decode('utf8')


class CinderServer(Server):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.db = SafeConnection("cinder.db")  # the Server cls will handle closing the connection
    self.db.row_factory = sqlite3.Row  # fetch returns as a dict instead of a tuple

    # load all the cars into a variable
    self.cars = load_cars(self.db, "SELECT * FROM cars")

    self.recommendation_systems = {
      "average": AverageRecommendation(self.cars, self.db),
      "weighted": WeightedAverageRecommendation(self.cars, self.db)
    }

    self.system_prompt = """
      Act as a car seller.
      you need to be able to explain the car to the customer in a very short and concise manner. You need to be able to answer any questions the customer may have,
      but only if they are related to the car. If a customer asks for similar cars, or anything that involves different cars, tell them that
      they can keep swiping for cars and they will get to see more cars.
      Let the customer try to lower the price, and be able to go down to a fair price with persuasion from the customer (this is kind of a roleplay).
      Remember that your answers must be very short and to the point. If the customer asks for the image of the car, send the following code as your response: "IMG@".
      If you only respond with these 4 characters the system will be able to send the correct image.
      """
    self.chatgpt = Chatbot(
      api_key=config.get('openai', 'api_key'),
      engine='gpt-3.5-turbo',
      system_prompt=self.system_prompt
    )

    self.load_endpoints_from_module(endpoints)  # load the endpoints

  def on_ready(self):
    logging.debug("Server is accepting connections")
    super().on_start()

  def before_handle(self, ctx: router.Context):



    logging.debug(f"[{ctx.request.method} {ctx.request.path} for {ctx.client}] will be handled by: {ctx.handler}")

    # get the user's recommendation method
    method = 'average'

    if token := ctx.request.headers.get("Authorization"):
      resp = self.db.execute("SELECT recommendation_method FROM users WHERE token=?", (token,)).fetchone()
      method = resp['recommendation_method'] if resp else "average"

    # easy-access functions with the context
    ctx.recommendation_update = functools.partial(self.recommendation_systems[method].update, ctx)
    ctx.recommendation_next = functools.partial(self.recommendation_systems[method].next, ctx)
    ctx.load_image = functools.partial(load_car_image, ctx)
    ctx.chatgpt = self.chatgpt

  def after_handle(self, ctx: router.Context, response):
    logging.debug(f"[{ctx.request.method} {ctx.request.path} for {ctx.client}] handler returned {str(response)[:200]}")

  def on_close(self):
    logging.debug("Server is shutting down")
    self.db.close()
    super().on_close()


if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument("--host", default="0.0.0.0", help="The host to bind to")
  parser.add_argument("--port", default=5000, type=int, help="The port to bind to")
  parser.add_argument("--debug", action="store_true", help="Enable debug mode")
  parser.add_argument("--secure", action="store_true", default=False, help="Enable public/private key encryption")
  parser.add_argument("--config", default="config.ini", help="The path to the config file")
  args = parser.parse_args()

  logging.basicConfig(level=logging.INFO)
  # logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

  if not os.path.exists(args.config):
    logging.error(f"Missing config file {args.config} does not exist")
    exit(1)
  else:
    config = configparser.ConfigParser()
    config.read(args.config)

  server = CinderServer(host=args.host, port=args.port, secure=args.secure, config=config, debug=args.debug)
  server.run()
