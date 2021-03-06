#!/usr/bin/env python
import csv
import pandas
import numpy
import sys

def cal_mean(pathname, filename):
    mean_value = []
    var_value = []
    df = pandas.read_csv(pathname + filename)
    #left_eye
    mean = float("{0:.4f}".format(round(numpy.mean(df.left_eye), 4)))
    var = float("{0:.4f}".format(round(numpy.var(df.left_eye), 4)))
    mean_value.append(mean)
    var_value.append(var)

    #forehead
    mean = float("{0:.4f}".format(round(numpy.mean(df.forehead), 4)))
    var = float("{0:.4f}".format(round(numpy.var(df.forehead), 4)))
    mean_value.append(mean)
    var_value.append(var)

    #right_eye
    mean = float("{0:.4f}".format(round(numpy.mean(df.right_eye), 4)))
    var = float("{0:.4f}".format(round(numpy.var(df.right_eye), 4)))
    mean_value.append(mean)
    var_value.append(var)

    #nose_bridge
    mean = float("{0:.4f}".format(round(numpy.mean(df.nose_bridge), 4)))
    var = float("{0:.4f}".format(round(numpy.var(df.nose_bridge), 4)))
    mean_value.append(mean)
    var_value.append(var)

    #left_cheek
    mean = float("{0:.4f}".format(round(numpy.mean(df.left_cheek), 4)))
    var = float("{0:.4f}".format(round(numpy.var(df.left_cheek), 4)))
    mean_value.append(mean)
    var_value.append(var)

    #right_cheek
    mean = float("{0:.4f}".format(round(numpy.mean(df.right_cheek), 4)))
    var = float("{0:.4f}".format(round(numpy.var(df.right_cheek), 4)))
    mean_value.append(mean)
    var_value.append(var)

    #nose
    mean = float("{0:.4f}".format(round(numpy.mean(df.nose), 4)))
    var = float("{0:.4f}".format(round(numpy.var(df.nose), 4)))
    mean_value.append(mean)
    var_value.append(var)

    #mouth
    mean = float("{0:.4f}".format(round(numpy.mean(df.mouth), 4)))
    var = float("{0:.4f}".format(round(numpy.var(df.mouth), 4)))
    mean_value.append(mean)
    var_value.append(var)

    writer = csv.writer(file('%smean_%s' % (pathname, filename), 'w'))

    title = ['left_eye', 'forehead', 'right_eye', 'nose_bridge', \
            'left_cheek', 'right_cheek', 'nose', 'mouth']

    writer.writerow(title)
    writer.writerow(mean_value)
    writer.writerow(var_value)

if __name__ == "__main__":
    cal_mean(sys.argv[1], sys.argv[2])
