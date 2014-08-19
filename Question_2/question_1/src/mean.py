#!/usr/bin/env python

import Image
import numpy
import math
import sys

def get_pixel(pixel, img, row, col):
    for i in xrange(3):
        for j in xrange(3):
            pixel[i][j] = img[row][col]
            col += 1
        col -= 3
        row += 1
    return pixel

def write_pixel(pixel, img, row, col):
    img[row + 1][col + 1] = pixel[1][1]
    return img

def scan_image(img, saved_img, row, col, operator, threshold):
    for i in xrange(row - 2):
        for j in xrange(col - 2):
            pixel = [[0 for x in xrange(3)] for x in xrange(3)]
            get_pixel(pixel, img, i, j)
            mean(operator, pixel, saved_img, i, j, threshold)
    return saved_img

def mean(operator, pixel, saved_img, row, col, threshold):
    gsum = 0
    for i in xrange(3):
        for j in xrange(3):
            gsum += pixel[i][j] * operator[i][j]

    if (gsum / 9) >= threshold:
        pixel[1][1] = 255
    else:
        pixel[1][1] = 0
    write_pixel(pixel, saved_img, row, col)
    return saved_img

if __name__ == "__main__":
    im = Image.open(sys.argv[1])
    width = im.size[0]
    height = im.size[1]
    imarray = numpy.array(im)
    my_im = Image.new("L", (width, height))
    my_im_array = numpy.array(my_im)
    operator = [
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, 1]
            ]
    threshold = int(sys.argv[3])
    scan_image(imarray, my_im_array, height, width, operator, threshold)

    mytiff = Image.fromarray(my_im_array)
    mytiff.save(sys.argv[2])
