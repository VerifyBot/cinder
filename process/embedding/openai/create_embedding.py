import json
import os.path

from openai import OpenAI

class Embedding:
  def __init__(self, api_key: str):
    self.client = OpenAI(api_key=api_key)

  def generate_embedding(self, story: str) -> list[float]:
    """
    Generate an embedding for the given story using OpenAI's embedding feature
    """

    response = self.client.embeddings.create(
      input=story,
      model="text-embedding-3-large"
    )

    return response.data[0].embedding


  def main(self, stories_data: str, cars_output: str):
    assert os.path.exists(stories_data), f'Stories data file not found in {os.path.abspath(stories_data)}'
    assert os.path.exists(cars_output), f'Cars output file not found in {os.path.abspath(cars_output)}'

    with open(stories_data, 'r', encoding='utf8') as f:
      stories = json.load(f)

    # we are going to dump it to cars_output every time which will
    # allow us to continue from where we left off in case of an error

    with open(cars_output, 'r', encoding='utf8') as f:
      cars = json.load(f)

    for i, it in enumerate(stories, start=1):
      story = it['story']
      car_id = it['car_id']

      # there are just under 1000 cars, so we can afford to do a linear search
      car = next((car for car in cars if car['id'] == car_id), None)

      if not car:
        print(f'⚠️ Car with id {car_id} not found in the cars data. Skipping...')
        continue

      if car.get('embedding'):
        print(f'⏭️️ Car #{car_id} already has an embedding.')
        continue

      embedding = self.generate_embedding(story)
      car['embedding'] = embedding

      with open(cars_output, 'w', encoding='utf8') as f:
        json.dump(cars, f, ensure_ascii=False, indent=2)

      print(f'🪄 [{i}/{len(stories)}] Added an embedding for {car_id=}')

    print(f'🧙🏼‍♂️️ Embeddings for all cars is available in {os.path.abspath(cars_output)}.')


if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('--stories-data', type=str, required=True, help='Path to the stories data file')
  parser.add_argument('--cars-output', type=str, required=True,
                      help='Path to the cars output file, this file will be updated with an `embedding` key for each car.')
  parser.add_argument('--api-key', type=str, required=True, help='OpenAI API key')

  args = parser.parse_args()

  embedding_manager = Embedding(args.api_key)
  embedding_manager.main(args.stories_data, args.cars_output)
