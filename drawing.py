from typing import List

import cv2 as cv
from numpy import zeros, uint8

class GCodeBasedImage:
    def __init__(self, width_pixels, height_pixels, width_mm, height_mm, x_offset_mm=0, y_offset_mm=0):
        self.w_px = width_pixels
        self.w_mm = width_mm
        self.h_px = height_pixels
        self.h_mm = height_mm
        self.x_offset_mm = x_offset_mm
        self.y_offset_mm = y_offset_mm

        self.image = zeros((height_pixels, width_pixels), dtype=uint8)

    def x_to_pixels(self, x):
        return int( (x - self.x_offset_mm)*self.w_px/self.w_mm )

    def y_to_pixels(self, y):
        return self.h_px - int( (y - self.y_offset_mm)*self.h_px/self.h_mm )

    def draw(self, xs: List[List[float]], ys: List[List[float]], thickness=3):
        for x, y in zip(xs, ys):
            xy = [(self.x_to_pixels(x_mm), self.y_to_pixels(y_mm)) for x_mm, y_mm in zip(x,y)]
            for i in range(len(xy)-1):
                #print("Line:", xy[i], xy[i+1])
                cv.line(self.image, xy[i], xy[i+1], color=255, thickness=thickness)

    def show(self):

        cv.imshow('image', self.image)
        cv.waitKey(0)
        cv.destroyAllWindows()


if __name__ == "__main__":

    from gcode_reader import Printer
    printer = Printer()
    printer.parse_code("test_data/CFDMP_test.gcode")

    layers = printer.layers()

    render_x, render_y = zip(*layers[0])

    render = GCodeBasedImage(1024, 600, 300, 200)
    render.draw(render_x, render_y,5)
    render.show()