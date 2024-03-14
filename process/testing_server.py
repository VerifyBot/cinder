import base64
import json
import random

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

with open('data-preperation/carsData.json', encoding='utf8') as fp:
  cars = json.load(fp)


@app.route('/car')
def car():
  dt = random.choice(cars)
  with open(f'data-preperation/scraper/images/{dt["id"]}.png', 'rb') as fp:
    dt['image'] = base64.b64encode(fp.read()).decode('utf8')

  # debug to see all flags
  # dt = {k: True if isinstance(v, bool) else v for k, v in dt.items()}

  return jsonify(dt)

@app.route('/chats')
def chats():
  return [dict(name="Car Manager", related_car_name="Cacdila 10v (improved)")]

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)
