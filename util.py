import numpy
import cv2

def path_length(xs, ys):
    xy = [t for t in zip(xs, ys)]
    tot = 0.0
    for i in range(len(xy)-1):
        x1, y1 = xy[i]
        x2, y2 = xy[i+1]

        tot += numpy.sqrt((x2-x1)**2 + (y2-y1)**2)

    return tot

def layer_length(data):
    tot = 0.0
    for x, y in data:
        tot += path_length(x,y)
    return tot


def rotate_image(im, angle):
    rows = im.shape[0]
    cols = im.shape[1]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    return cv2.warpAffine(im, M, (cols, rows))