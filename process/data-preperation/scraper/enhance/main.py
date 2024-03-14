import json
import os.path
import shutil

import requests

import bgfixer
import run_effect

import hashlib

SETTINGS = dict(
  enhanceMainImage=True,

  # i decided that this is too much. we can just display all extra images in a grid
  # where every image takes a small part and looks high quality.
  enhanceExtraImages=False,
)

# save them all
dir = '../images'

with open('../withimgs_carsData.json', encoding='utf8') as fp:
  cars = json.load(fp)



def hash_bytes(data):
  return hashlib.sha256(data).hexdigest()

# some cars have the same image (actually many)
# so lets hash every image as the dict key and the enhanced fn as the value
# when a car has the same image as another car, we can just copy the cached enhanced image
cached_imgs = {

}

for car_idx, car in enumerate(cars):
  id = car['id']

  imgs_enhanced = 0

  if SETTINGS['enhanceMainImage']:
    fn = os.path.join(dir, f'{id}.png')

    low_quality_main = requests.get(car['image']).content
    lqm_hash = hash_bytes(low_quality_main)

    if os.path.exists(fn):
      cached_imgs[lqm_hash] = fn  # cache if enhanced before
      print(f'⏩ Skipping {id}')
      continue

    if cached_path := cached_imgs.get(lqm_hash):
      print(f'{id} has the same image as another car, copying cached image from {cached_path}')
      shutil.copyfile(cached_path, fn)  # copy it
      continue


    en_main = run_effect.enhance(requests.get(car['image']).content)
    main_image = bgfixer.crop_image(en_main)
    main_image.save(fn)
    cached_imgs[lqm_hash] = fn  # cache new enhanced
    imgs_enhanced += 1
    print('✅ Enhanced main image')

  # enhance sub images
  if SETTINGS['enhanceExtraImages']:
    for i, img in enumerate(car['extraImages']):
      fn = os.path.join(dir, f'{id}_{i}.png')

      if os.path.exists(fn):
        continue

      img = bgfixer.crop_image(run_effect.enhance(requests.get(img).content))
      img.save(fn)
      imgs_enhanced += 1
      print(f'👍 Enhanced extra image ({i + 1}/{len(car["extraImages"])})')

  print(f'💐 Enhanced {imgs_enhanced} new image{"s" if imgs_enhanced != 1 else ""} for {id} ({car_idx + 1}/{len(cars)})')
