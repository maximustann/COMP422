#!/usr/bin/env python
import Image
import numpy
import sys
import math
import numpy


def otsu(img, width, height):
    threshold = 0
    pixelCount = [0 for x in xrange(256)]
    pixelPro = [0.0 for x in xrange(256)]
    for i in xrange(width):
        for j in xrange(height):
            pixelCount[img[i][j]] += 1
    for i in xrange(256):
        pixelPro[i] = pixelCount[i] / float(width * height)

    w0 = w1 = u0tmp = u1tmp = u0 = u1 = u = deltaTmp = deltaMax = 0.0
    for i in xrange(256):
        w0 = w1 = u0tmp = u1tmp = u0 = u1 = u = deltaTmp  = 0.0
        for j in xrange(256):
            if j <= i:
                w0 += pixelPro[j]
                u0tmp += j * pixelPro[j]
            else:
                w1 += pixelPro[j]
                u1tmp += j * pixelPro[j]

        if w0 == 0.0:
            continue
        u0 = u0tmp / w0
        if w1 == 0.0:
            continue
        u1 = u1tmp / w1
        u = u0tmp + u1tmp
        deltaTmp = w0 * math.pow((u0 - u), 2) + w1 * math.pow((u1 - u), 2)
        if deltaTmp > deltaMax:
            deltaMax = deltaTmp
            threshold = i

    return threshold

def get_pixel(pixel, img, row, col):
    for i in xrange(3):
        for j in xrange(3):
            pixel[i][j] = img[row][col]
            col += 1
        col -= 3
        row += 1
    return pixel

def write_img_black(img, row, col):
    pixel = [[0 for x in xrange(3)] for x in xrange(3)]
    write_img(pixel, img, row, col)
def write_img_white(img, row, col):
    pixel = [[255 for x in xrange(3)] for x in xrange(3)]
    write_img(pixel, img, row, col)

def write_img(pixel, img, row, col):
    for i in xrange(3):
        for j in xrange(3):
            img[row][col] = pixel[i][j]
            col += 1
        col -= 3
        row += 1
    return img

def scan_image(img, saved_img, row, col, threshold):
    for i in xrange(row - 2):
        for j in xrange(col - 2):
            pixel = [[0 for x in xrange(3)] for x in xrange(3)]
            get_pixel(pixel, img, i, j)
            ots(threshold, saved_img, i, j, img, pixel)
    return saved_img

def ots(threshold, saved_img, row, col, img, pixel):
    if pixel[1][1] < threshold:
        write_img_black(saved_img, row, col)
    else:
        write_img_white(saved_img, row, col)

