import json

with open('../carsData.json', 'r', encoding='utf8') as fp:
  cars_data = json.load(fp)

unique_colors = set(
  car['color']
  for car in cars_data
  if car.get('color')
)

print(unique_colors)
print(f'{len(unique_colors)=}')