import cv2 as cv
from numpy import zeros, uint8, array, max

from gcode_reader import Printer
from photo_positions import get_grid_size
from sticher import stitch
from settings import default_scaling
from drawing import GCodeBasedImage

directory = "test_data/Test2/"

nx, ny, x_offset_mm, y_offset_mm, width_mm, height_mm = get_grid_size(directory+"Image_bed")

x_extra_offset, y_extra_offset = -17.699999999999967, 8.200000000000006

printer = Printer()
printer.parse_code(directory+"CFDMP_TC-Cover.gcode")
layers = printer.layers()

# Image for comparison
last_image = stitch(directory + "Layer0",
                    ny, nx,
                    default_scaling.h, default_scaling.w,
                    rotation=default_scaling.rotation)

last_image = cv.cvtColor(last_image, cv.COLOR_BGR2GRAY)
last_image = cv.GaussianBlur(last_image, (41,41), 20)

for layer_index in range(printer.max_layer+1):

    # Get stiched photo
    photo_im = stitch(directory + ("Layer%i"%(layer_index+1)),
                      ny, nx,
                      default_scaling.h, default_scaling.w, rotation=default_scaling.rotation)

    # shape
    imsize = photo_im.shape

    # Get greyscale version
    value = cv.cvtColor(photo_im, cv.COLOR_BGR2GRAY)

    # Get what we think we should see
    expected_image = GCodeBasedImage(imsize[1], imsize[0], width_mm, height_mm, x_offset_mm + x_extra_offset, y_offset_mm+y_extra_offset)
    render_x, render_y = zip(*layers[layer_index])
    expected_image.draw(render_x, render_y, thickness=10)
    expected = expected_image.image

    # All this stuff is about getting a nice difference
    blurred = cv.GaussianBlur(value, (41,41), 20)

    if last_image is not None:
        intensity = cv.subtract(blurred, last_image)
        #intensity = array(intensity, dtype=uint8)
        ret, diff = cv.threshold(intensity, 5, 1, cv.THRESH_BINARY)
    else:
        diff = zeros((imsize[0], imsize[1]), dtype=uint8)

    # Colour calculations
    hue = cv.subtract(120*diff, expected) # zero if expected value or background, 255 if
    sat = 255*(1 - (1-diff)*(1-expected//255)) # Logical OR, saturation where we have (difference) OR (expected line)

    # Combine channels
    hsv = cv.merge((hue, sat, value))
    im = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)


    # Show the image
    cv.imshow('image', im)

    # Wait for key
    key = cv.waitKey(0)

    # save last image for difference
    last_image = blurred
