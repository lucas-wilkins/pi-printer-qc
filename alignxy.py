import cv2 as cv
from numpy import zeros, uint8

from gcode_reader import Printer
from photo_positions import get_grid_size
from sticher import stitch
from settings import default_scaling
from drawing import GCodeBasedImage

directory = "test_data/Test2/"

nx, ny, x_offset_mm, y_offset_mm, width_mm, height_mm = get_grid_size(directory+"Image_bed")



printer = Printer()
printer.parse_code(directory+"CFDMP_TC-Cover.gcode")
layers = printer.layers()

last_image = None

layer_index = 1

x_extra_offset = 0.0
y_extra_offset = 0.0

photo_im = stitch(directory + ("Layer%i"%layer_index),
                  ny, nx,
                  default_scaling.h, default_scaling.w, rotation=default_scaling.rotation)

imsize = photo_im.shape

big_jump = True

while True:

    value = cv.cvtColor(photo_im, cv.COLOR_BGR2GRAY)

    expected_image = GCodeBasedImage(
        imsize[1], imsize[0],
        width_mm, height_mm,
        x_offset_mm + x_extra_offset, y_offset_mm+y_extra_offset)

    render_x, render_y = zip(*layers[layer_index])
    expected_image.draw(render_x, render_y, thickness=3)

    hsv = cv.merge((zeros((imsize[0], imsize[1]), dtype=uint8), expected_image.image, value))

    im = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)


    cv.imshow('image', im)
    key = cv.waitKey(0)

    s = 5.0 if big_jump else 0.1

    if key == 37:
        x_extra_offset -= s
    elif key == 38:
        y_extra_offset += s
    elif key == 39:
        x_extra_offset += s
    elif key == 40:
        y_extra_offset -= s

    elif key == ord("m"):
        big_jump = not big_jump
    elif key == ord("q"):
        break

    print(x_extra_offset, y_extra_offset)