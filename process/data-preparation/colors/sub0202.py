import io
import json
import os.path
import time
import traceback
from pathlib import Path

## Color Detector
from colorthief import ColorThief


from PIL import Image, ImageEnhance

## Colors
def get_image_dominant_color(file_path) -> str:
  """
  Returns the dominant color in the image as hex
  """

  # increase the files brightness/saturation/whatever so that closer colors look the same
  im = Image.open(file_path)
  enhancer = ImageEnhance.Brightness(im)
  im = enhancer.enhance(1.1)
  enhancer = ImageEnhance.Color(im)
  im = enhancer.enhance(1.2)
  enhancer = ImageEnhance.Contrast(im)
  im = enhancer.enhance(1.3)
  enhancer = ImageEnhance.Sharpness(im)
  im = enhancer.enhance(1.3)

  # show it
  # save it so it can be used with Image.open again
  buffer = io.BytesIO()
  im.save(buffer, format="PNG")
  buffer.seek(0)
  color_thief = ColorThief(buffer)
  dominant_color = color_thief.get_palette(quality=1, color_count=2)
  return '#%02x%02x%02x' % tuple(dominant_color[0])


def color_main(images_folder: str, update_cars: str):
  images_paths = list(Path(images_folder).glob('*.png'))

  with open(update_cars, encoding='utf8') as fp:
    cars_data = json.load(fp)
    # allow fast id reference
    cars_access = {c['id']: i for i, c in enumerate(cars_data)}

  for i, fpath in enumerate(images_paths):
    car_id = os.path.basename(fpath).split('.')[0]

    # if cars_data[cars_access[car_id]].get('color'):
    #   continue

    start_time = time.time()

    try:
      color_hex = get_image_dominant_color(fpath)
    except Exception as e:
      traceback.print_exc()
      print(f'Failed to get color for {fpath} >> {e}')
      continue

    print(
      f'[{i + 1}/{len(images_paths)} @ color] Processed Car#{car_id} >> {color_hex} ({time.time() - start_time:.2f}s)')

    car_index = cars_access[car_id]
    cars_data[car_index]['color'] = color_hex

  with open(update_cars, 'w', encoding='utf8') as fp:
    json.dump(cars_data, fp, indent=2, ensure_ascii=False)


import rembg
def crop_image(file_path, dest):
  """
  Crop the image so we can get the color of the car with the least noise
  :param file_path: path to the image
  :param dest: destination folder to save the cropped image
  :return:
  """

  try:
    with open(file_path, 'rb') as i:
      with open(os.path.join(dest, os.path.basename(file_path)), 'wb') as o:
        inp = i.read()
        output = rembg.remove(inp)
        o.write(output)
  except Exception as e:
    print(f'Failed to crop {file_path} >> {e}')


def crop_main(raw_images_folder, clean_images_destination):
  if not os.path.exists(clean_images_destination):
    os.makedirs(clean_images_destination)

  images_paths = list(Path(raw_images_folder).glob('*.png'))

  for i, fpath in enumerate(images_paths):
    # already done?
    if os.path.exists(os.path.join(clean_images_destination, os.path.basename(fpath))):
      continue

    car_id = os.path.basename(fpath).split('.')[0]
    start_time = time.time()

    crop_image(str(fpath), dest=clean_images_destination)
    print(f'[{i + 1}/{len(images_paths)} @ crop] Processed Car#{car_id} ({time.time() - start_time:.2f}s)')


def main(images_folder, cars_data):
  cropped_folder = "temp_cropped2"
  cropped_available = os.path.exists(cropped_folder) and (
      len(list(Path(cropped_folder).glob('*.png'))) == len(list(Path(images_folder).glob('*.png')))
  )

  if not cropped_available:
    print('✂️ Cropping images...')
    crop_main(images_folder, cropped_folder)
  else:
    print('✂️ Cropped images already available')

  print('🎨 Getting colors...')
  color_main(cropped_folder, update_cars=cars_data)


if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument('--images-source', type=str, required=True)
  parser.add_argument('--cars-data', type=str, required=True)
  args = parser.parse_args()

  main(images_folder=args.images_source, cars_data=args.cars_data)
