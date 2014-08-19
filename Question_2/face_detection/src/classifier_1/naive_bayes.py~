#!/usr/bin/env python
import os
import pandas
import math
import csv
import sys

def pro_face(df, target_img):
    left_eye = target_img[0]
    forehead = target_img[1]
    right_eye = target_img[2]
    nose_bridge = target_img[3]
    left_cheek = target_img[4]
    right_cheek = target_img[5]
    nose = target_img[6]
    mouth = target_img[7]

    pros = [0 for i in xrange(8)]
    #left_eye
    mean_left_eye = df.left_eye.ix[0]
    var_left_eye = df.left_eye.ix[1]
    pros[0] = formula(left_eye, mean_left_eye, var_left_eye)

    #forehead
    mean_forehead = df.forehead.ix[0]
    var_forehead = df.forehead.ix[1]
    pros[1] = formula(forehead, mean_forehead, var_forehead)

    #right_eye
    mean_right_eye = df.right_eye.ix[0]
    var_right_eye = df.right_eye.ix[1]
    pros[2] = formula(right_eye, mean_right_eye, var_right_eye)

    #nose_bridge
    mean_nose_bridge = df.nose_bridge.ix[0]
    var_nose_bridge = df.nose_bridge.ix[1]
    pros[3] = formula(nose_bridge, mean_nose_bridge, var_nose_bridge)

    #left_cheek
    mean_left_cheek = df.left_cheek.ix[0]
    var_left_cheek = df.left_cheek.ix[1]
    pros[4] = formula(left_cheek, mean_left_cheek, var_left_cheek)

    #right_cheek
    mean_right_cheek = df.right_cheek.ix[0]
    var_right_cheek = df.right_cheek.ix[1]
    pros[5] = formula(right_cheek, mean_right_cheek, var_right_cheek)

    #nose
    mean_nose = df.nose.ix[0]
    var_nose = df.nose.ix[1]
    pros[6] = formula(nose, mean_nose, var_nose)
    
    #mouth
    mean_mouth = df.mouth.ix[0]
    var_mouth = df.mouth.ix[1]
    pros[7] = formula(mouth, mean_mouth, var_mouth)

    result = _mul(pros)
    return result

def _mul(pros):
    sum = 1
    for pro in pros:
        sum *= pro
    return sum

def readfile(filename):
    df = pandas.read_csv(filename)
    return df

def formula(value, mean, var):
    w = 1 / math.sqrt(2 * math.pi * var)
    k = math.exp(0.5 * (-math.pow((value - mean), 2) / (2 * var)))
    return w * k

def _compare(face, non_face):
    if face > non_face:
        return 1
    else:
        return 0

def extract_target_data(filename):
    detect = []
    with open(filename, 'r') as detect_file:
        face_reader = csv.reader(detect_file, delimiter = ',')
        for i, row in enumerate(face_reader):
            if i == 0:
                continue
            r = []
            for item in row:
                r.append(float(item))
            detect.append(r)
    return detect

def distributor(result_file, dataset, face_file, non_face_file):
    result_title = ['result']
    result_dataset = []
    for img in dataset:
        item = []
        face_pro = pro_face(face_file, img)
        non_face_pro = pro_face(non_face_file, img)
        item.append(_compare(face_pro, non_face_pro))
        result_dataset.append(item)

    per = percentage(result_dataset)
    with open(result_file, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(result_title)
        writer.writerows(result_dataset)
    return per

def percentage(result):
    sums = 0.0
    for item in result:
        if item[0] == 1:
            sums += 1
    return (sums / len(result))

def paste(temp_result_file, target_file, result):
    pathname = os.path.dirname(result)
    result = os.path.basename(result)
    os.system("paste -d',' %s %s > %s" % (temp_result_file, target_file, pathname + '/' + result))
    os.system("tr -d '\015' < %s > %s/temp_%s" % (pathname + '/' + result, pathname, result))
    os.system("rm %s" % pathname + '/' + result)
    os.system("mv %s/temp_%s %s" % (pathname, result, pathname + '/' + result))



def comparison(test_face_dataset_file, test_non_face_dataset_file,\
                train_face_file, train_non_face_file):
    tp = fp = 0
    result = []
    #read file
    test_face_dataset = extract_target_data(test_face_dataset_file)
    test_non_face_dataset = extract_target_data(test_non_face_dataset_file)
    train_face = readfile(train_face_file)
    train_non_face = readfile(train_non_face_file)

    #calculate tp
    pathname = os.path.dirname(test_face_dataset_file)
    training_sample_no = train_face_file[train_face_file.find('0') : train_face_file.find('0') + 2]
    test_face_dataset_new_file = os.path.basename(test_face_dataset_file)
    test_face_dataset_new_file = test_face_dataset_file[:test_face_dataset_file.find('0') + 3] +\
            training_sample_no + test_face_dataset_file[test_face_dataset_file.find('0') + 2:]

    test_face_dataset_new_file = os.path.basename(test_face_dataset_new_file)
    temp_result_file = pathname + '/temp_result_' + test_face_dataset_new_file
    tp = distributor(temp_result_file, test_face_dataset, train_face,\
            train_non_face)
    result.append(tp)
    result_file = pathname + '/result_' + test_face_dataset_new_file
    paste(temp_result_file, pathname + '/' + os.path.basename(test_face_dataset_file), result_file)


    #calculate fp
    pathname = os.path.dirname(test_non_face_dataset_file)
    training_sample_no = train_non_face_file[train_non_face_file.find('0') : train_non_face_file.find('0') + 2]
    test_non_face_dataset_new_file = os.path.basename(test_non_face_dataset_file)
    test_non_face_dataset_new_file = test_non_face_dataset_file[:test_non_face_dataset_file.find('0') + 3] +\
            training_sample_no + test_non_face_dataset_file[test_non_face_dataset_file.find('0') + 2:]
    test_non_face_dataset_new_file = os.path.basename(test_non_face_dataset_new_file)
    temp_result_file = pathname + '/temp_result_' + test_non_face_dataset_new_file
    fp = distributor(temp_result_file, test_non_face_dataset, train_face, \
            train_non_face)
    result_file = pathname + '/result_' + test_non_face_dataset_new_file
    paste(temp_result_file, pathname + '/' + os.path.basename(test_non_face_dataset_file), result_file)
    result.append(fp)
    write_file(result)

def write_file(result):
    title = ["tp", "fp"]
    start_data = [0, 0]
    end_data = [1, 1]
    if not os.path.exists("./result/classifier_1/tp_fp.csv"):
        with open ("./result/classifier_1/tp_fp.csv", 'w') as f:
            writer = csv.writer(f)
            writer.writerow(title)
            writer.writerow(start_data)
            writer.writerow(end_data)
            writer.writerow(result)
    else:
        with open ("./result/classifier_1/tp_fp.csv", 'a') as f:
            writer = csv.writer(f)
            writer.writerow(result)
    f.close()

if __name__ == "__main__":
    comparison(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


