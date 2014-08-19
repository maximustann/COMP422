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
    for i in xrange(3):
        for j in xrange(3):
            img[row][col] = pixel[i][j]
            col += 1
        col -= 3
        row += 1
    return img

def scan_image(img, row, col):
    for i in xrange(row - 2):
        for j in xrange(col - 2):
            pixel = [[0 for x in xrange(3)] for x in xrange(3)]
            get_pixel(pixel, img, i, j)
            img = median(pixel, img, i, j)
    return img

def median(pixel, img, row, col):
    pixel[1][1] = sort(pixel)
    img = write_pixel(pixel, img, row, col)
    return img

def sort(pixel):
    a = []
    for i in xrange(3):
        for j in xrange(3):
            a.append(pixel[i][j])
    a = sorted(a)
    return a[4]

if __name__ == "__main__":
    im = Image.open(sys.argv[1])
    width = im.size[0]
    height = im.size[1]
    imarray = numpy.array(im)

    my_im = Image.new("L", (width, height))
    my_im_array = numpy.array(my_im)

    my_im_array = scan_image(imarray, height, width)

    mytiff = Image.fromarray(my_im_array)

    mytiff.save(sys.argv[2])
