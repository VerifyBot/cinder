# Data Preperation

## Colors
The scraped data from zap does not contain the color of the car,
this module uses [this repo](https://github.com/patrick013/Object-Detection---Yolov3)
to detect the color of each car and modify the `carsData.json` file under `data-preperation/` accordingly. 

### How it works

1. crop the car from the original image.
2. get the pallete of the car
   - get the dominant color of the car that isn't gray (car windows)
3. save to `carsData.json`

### How to run

```shell
python colors.py --images-source <path_to_cars_images> --cars-data <path_to_cars_data.json>
```