import io
import json
import typing

import requests
from PIL import Image

# crop
def crop_image(url_or_im: typing.Union[Image, bytes, str]) -> bytes:
  """crop the car image to remove the white cover"""
  if isinstance(url_or_im, bytes):
    im = Image.open(io.BytesIO(url_or_im))
  elif isinstance(url_or_im, str):
    im = Image.open(io.BytesIO(requests.get(img).content))
  else:
    im = url_or_im

  im = im.crop(
    (13, im.height/6 + 51, im.width - 13, im.height/1.22 - 50)
  )

  return im


if __name__ == '__main__':
  im = Image.open('test.png')
  im = crop_image(im)
  print(f'close to 9:16 ratio by {im.height/im.width:.4f} vs 0.5625')
  im.show()