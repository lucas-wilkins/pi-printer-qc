import cv2 as cv
from numpy import zeros, uint8
import os

from util import rotate_image

def get_centre(image, x_size, y_size):
    """ Gets the central portion of an image"""
    w, h, n = image.shape
    return image[(w - x_size)/2 : (w + x_size)/2, (h - y_size)/2 : (h + y_size)/2, :]

def layouter(n_x, n_y, other_axis=False, mod_value=0):
    """Returns a function that gives the image number for a grid position"""
    def fun(i, j):
        # j = n_y - j - 1
        i = n_x - i - 1
        if other_axis:
            if i%2 == mod_value:
                j = n_y - j - 1
        else:
            if j%2 == mod_value:
                i = n_x - i - 1

        return (n_y * i) + j
    return fun


def stitch(directory, n_x: int, n_y: int, x_size: int, y_size: int, rotation: float, filter: int = 0, unsharp=0):
    out = zeros((n_x*x_size, n_y*y_size, 3), dtype=uint8)

    # Filenames don't start at zero, picXXXX.jpg
    filenames = [filename for filename in os.listdir(directory) if filename.endswith(".jpg")]
    filename_offset = int(sorted(filenames)[0][3:7])

    layout = layouter(n_x, n_y, True, 1)

    for i in range(n_x):
        for j in range(n_y):

            #a = n_x - i - 1
            a = i
            #b = n_y - j - 1
            b = j

            fname = directory + ("/pic%04i.jpg"%(layout(a,b)+filename_offset))
            #print("Reading '%s'"%fname)

            image = cv.imread(fname)

            if filter != 0:
                image = cv.GaussianBlur(image, (2 * filter + 1, 2 * filter + 1), filter)

            #if unsharp != 0:
            #    blurred = cv.GaussianBlur(image, (2*unsharp+1, 2*unsharp+1), unsharp)
            #    image = cv.subtract(image, blurred)

            image = rotate_image(image, rotation)
            centre_image = get_centre(image, x_size, y_size)

            out[i*x_size:(i+1)*x_size, j*y_size:(j+1)*y_size, :] = centre_image


    return out










if __name__ == "__main__":

    """ Running in __main__ will give the dimensions that we want """

    h_max = 1232
    w_max = 1640

    h = 1232
    w = 1640

    big_jump = True

    rotation = -1.4

    while True:
        im = stitch("test_data/Test1/Layer1", 3, 4, h, w,rotation=rotation)

        s = 10 if big_jump else 1

        cv.imshow('image', im)
        key = cv.waitKey(0)

        if key == 37:
            w -= s
        elif key == 38:
            h += s
        elif key == 39:
            w += s
        elif key == 40:
            h -= s
        elif key == ord("a"):
            rotation += s*0.01
        elif key == ord("s"):
            rotation -= s*0.01

        elif key == ord("m"):
            big_jump = not big_jump
        elif key == ord("q"):
            break

        if h > h_max:
            h = h_max

        if w > w_max:
            w = w_max

        print(w,h,rotation)

    cv.destroyAllWindows()




