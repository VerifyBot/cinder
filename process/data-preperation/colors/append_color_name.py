import json
import math

with open('availableColors.json') as f:
  dt = json.load(f)


def name_from_weight(weight):
  weight = weight.replace('a100', '1000').replace('a200', '1100').replace('a400', '1200').replace('a700', '1300')
  weight = int(weight)
  return f'lighten-{math.ceil(5 - weight / 100)}' if weight < 500 else f'darken-{weight // 100 - 4}'

import webcolors
def get_color_from_hex(hex, weight_fallback):
  try:
    return webcolors.hex_to_name(hex)
  except ValueError:
    print('failed')
    return name_from_weight(weight_fallback)

mapping = {
  ashex: get_color_from_hex(ashex, weight)
  for name, ls in dt['full'].items()
  for weight, ashex in ls.items()
}

print(mapping)

with open('../carsData.json', encoding='utf8') as f:
  cars = json.load(f)


for car in cars:
  if car['color'] in mapping:
    car['colorName'] = mapping[car['color']]
  else:
    car['colorName'] = 'unknown'

with open('../cars.json', 'w', encoding='utf8') as f:
  json.dump(cars, f, indent=2, ensure_ascii=False)