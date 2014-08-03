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

def set_pixel_black(img, row, col):
    pixel = [[0 for x in xrange(3)] for x in xrange(3)]
    write_pixel(pixel, img, row, col)

def set_pixel_write(img, row, col):
    pixel = [[255 for x in xrange(3)] for x in xrange(3)]
    write_pixel(pixel, img, row, col)

def scan_image(img, saved_img, row, col, threshold):
    for i in xrange(row - 2):
        for j in xrange(col - 2):
            pixel = [[0 for x in xrange(3)] for x in xrange(3)]
            get_pixel(pixel, img, i, j)
            sobel(gx, gy, pixel, threshold, i, j, saved_img)
    return saved_img


def sobel(gx, gy, pixel, threshold, row, col, saved_img):
    gxsum = 0
    gysum = 0
    for i in xrange(3):
        for j in xrange(3):
            gxsum += gx[i][j] * pixel[i][j]
            gysum += gy[i][j] * pixel[i][j]
    gxsum *= gxsum
    gysum *= gysum

    fin = math.sqrt(gxsum + gysum)
    #print fin - threshold
    if fin - threshold > 0:
        set_pixel_black(saved_img, row, col)
    else:
        set_pixel_write(saved_img, row, col)




if __name__ == "__main__":

    im = Image.open(sys.argv[1])
    width = im.size[0]
    height = im.size[1]
    my_im = Image.new("L", (width, height))
    my_im_array = numpy.array(my_im)
    imarray = numpy.array(im)
    gx = [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]]

    gy = [
            [1, 2, 1], 
            [0, 0, 0], 
            [-1, -2, -1]]

    threshold = 90
    scan_image(imarray, my_im_array, height, width, threshold)
    mytiff = Image.fromarray(my_im_array)
    mytiff.save(sys.argv[2])
