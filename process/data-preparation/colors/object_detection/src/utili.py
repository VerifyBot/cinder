import os.path
from matplotlib import pyplot
from matplotlib.patches import Rectangle
import numpy as np
from skimage import img_as_ubyte
from skimage.io import imsave

def zoom_in(image_array, zoom_factor=0.5):
  # Get the original image dimensions
  original_height, original_width = image_array.shape[:2]

  # Calculate the crop dimensions
  crop_height = int(original_height * (1 - zoom_factor))
  crop_width = int(original_width * (1 - zoom_factor))

  # Calculate the starting point for the crop
  start_height = (original_height - crop_height) // 2
  start_width = (original_width - crop_width) // 2

  # Crop the image
  cropped_image = image_array[start_height:start_height + crop_height, start_width:start_width + crop_width]

  return cropped_image


def encoder_dic(valid_data):
  data_dic = {}
  (valid_boxes, valid_labels, valid_scores) = valid_data
  for box, label, score in zip(valid_boxes, valid_labels, valid_scores):
    if label not in data_dic:
      data_dic[label] = [[score, box, 'kept']]
    else:
      data_dic[label].append([score, box, 'kept'])

  return data_dic


def draw_boxes(filename, valid_data, save_directory):
  data = pyplot.imread(filename)
  fn = os.path.basename(filename)

  zoomed_img_uint8 = img_as_ubyte(zoom_in(data))
  imsave(os.path.join(save_directory, fn), zoomed_img_uint8)

  return

  pyplot.imshow(data)
  ax = pyplot.gca()

  for i in range(len(valid_data[0])):
    if valid_data[1][i] != 'car':
      continue

    box = valid_data[0][i]
    y1, x1, y2, x2 = box.ymin, box.xmin, box.ymax, box.xmax
    width, height = x2 - x1, y2 - y1
    rect = Rectangle((x1, y1), width, height, fill=False, color='white')
    ax.add_patch(rect)
    print('11', valid_data[1][i], valid_data[2][i])
    label = "%s (%.3f)" % (valid_data[1][i], valid_data[2][i])
    print('22', label)
    # pyplot.text(x1, y1, label, color='white')

    cropped_data = data[y1:y2, x1:x2]
    pyplot.imshow(cropped_data)
    # pyplot.title(label)

  # get first pixel color
  p = data[0, 0]
  print(f'{p=}')

  # display

  pyplot.figure(frameon=False)
  pyplot.axis('off')

  if not os.path.isdir(save_directory):
    os.mkdir(save_directory)

  fn = os.path.basename(filename)

  pyplot.savefig(
    os.path.join(save_directory, fn),
    format='png', bbox_inches='tight', pad_inches=0
  )

  # is less than 10kb?
  if os.path.getsize(os.path.join(save_directory, fn)) < 10 * 1024:
    # save the original just zoomed 20%
    print('special')

    zoomed_img_uint8 = img_as_ubyte(zoom_in(data))
    imsave(os.path.join(save_directory, fn), zoomed_img_uint8)


    return
