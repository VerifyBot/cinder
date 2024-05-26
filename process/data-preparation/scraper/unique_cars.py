import json

# non-unique cars have the same image url

with open('../../../data/carsDataEmbedding.json', encoding='utf8') as f:
  cars = json.load(f)

# calculate the number of unique cars

unique_cars = set()

for car in cars:
  cars_len = len(unique_cars)

  with open('images/' + car['id'] + '.png', 'rb') as f:
    img = f.read()
    unique_cars.add(img)

  # if it isn't a unique car, add a new key to the car
  if cars_len == len(unique_cars):
    car['duplicate'] = True

print(f'There are {len(unique_cars)}/{len(cars)} unique cars in the dataset.')

with open('../../../data/carsDataEmbeddingDuplicatedMark.json', 'w', encoding='utf8') as f:
  json.dump(cars, f, ensure_ascii=False, indent=2)
