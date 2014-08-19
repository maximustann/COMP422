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

def scan_image(img, saved_img, row, col):
    for i in xrange(row - 2):
        for j in xrange(col - 2):
            pixel = [[0 for x in xrange(3)] for x in xrange(3)]
            get_pixel(pixel, img, i, j)
            sobel(gx, gy, pixel, i, j, saved_img)
    return saved_img


def sobel(gx, gy, pixel, row, col, saved_img):
    gxsum = 0
    gysum = 0
    for i in xrange(3):
        for j in xrange(3):
            gxsum += gx[i][j] * pixel[i][j]
            gysum += gy[i][j] * pixel[i][j]
    gxsum *= gxsum
    gysum *= gysum

    fin = math.sqrt(gxsum + gysum)

    if fin > 255:
        pixel[1][1] = 255
    elif fin < 0:
        pixel[1][1] = 0
    else:
        pixel[1][1] = fin
    write_pixel(pixel, saved_img, row, col)



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

    scan_image(imarray, my_im_array, height, width)
    mytiff = Image.fromarray(my_im_array)
    mytiff.save(sys.argv[2])
