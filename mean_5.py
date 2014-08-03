#!/usr/bin/env python

import Image
import numpy
import math
import sys

def get_pixel(pixel, img, row, col):
    for i in xrange(5):
        for j in xrange(5):
            pixel[i][j] = img[row][col]
            col += 1
        col -= 5
        row += 1
    return pixel

def write_pixel(pixel, img, row, col):
    for i in xrange(5):
        for j in xrange(5):
            img[row][col] = pixel[i][j]
            col += 1
        col -= 5
        row += 1
    return img

def scan_image(img, col, row, operator):
    for i in xrange(row - 5):
        for j in xrange(col - 5):
            pixel = [[0 for x in xrange(5)] for x in xrange(5)]
            get_pixel(pixel, img, i, j)
            img = mean(operator, pixel, img, i, j)
    return img

def mean(operator, pixel, img, row, col):
    gsum = 0
    for i in xrange(5):
        for j in xrange(5):
            if i == 1 and j == 1:
                continue
            gsum += pixel[i][j] * operator[i][j]

    pixel[1][1] = gsum / 25
    write_pixel(pixel, img, row, col)
    return img
if __name__ == "__main__":
    im = Image.open(sys.argv[1])
    width = im.size[0]
    height = im.size[1]
    imarray = numpy.array(im)
    my_im = Image.new("L", (width, height))
    my_im_array = numpy.array(my_im)
    operator = [
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1]
            ]
    my_im_array = scan_image(imarray, width, height, operator)

    mytiff = Image.fromarray(my_im_array)
    mytiff.save(sys.argv[2])
