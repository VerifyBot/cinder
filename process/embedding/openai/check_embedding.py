import json

with open('../../../data/carsDataEmbedding.json', encoding='utf8') as f:
    cars = json.load(f)

v1_len = len(cars[0]['embedding'])
assert all(len(car['embedding']) == v1_len for car in cars), "All embeddings should have the same length"