import cv2
import os
import numpy as np
from shutil import copyfile

fill_color=(0, 0, 0)

c = 0

path_save = "D:/Project/MachineLearning/NhanDienLogo/datasets/LogoTM/"

path_label = "D:/Project/MachineLearning/NhanDienLogo/datasets/Logo/labels/"

path_image = "D:/Project/MachineLearning/NhanDienLogo/datasets/Logo/images/"

path_test = "D:/Project/MachineLearning/NhanDienLogo/datasets/Logo/test_0.txt"

test = []

testfile = open(path_test, 'r')
linestest = testfile.readlines()
for line in linestest:
    s = line.strip().split("/")[2]
    test.append(s.split(".")[0])

print(test)
are, w, h = [], [], []
allfile = os.listdir(path_image)
for file in allfile:
    print(allfile.index(file), "/", len(allfile))
    name = file.split(".")[0]
    if name not in test:
        label = open(path_label + name + ".txt", 'r')
        Lines = label.readlines()
        try:
            img = cv2.imread(path_image + file)
            dimensions = img.shape
            height = img.shape[0]
            width = img.shape[1]

            for line in Lines:
                c += 1
                ano = line.strip().split(" ")
                x_min = int((float(ano[1])-float(ano[3])/2)*width)
                x_max = int((float(ano[1])+float(ano[3])/2)*width)
                y_min = int((float(ano[2])-float(ano[4])/2)*height)
                y_max = int((float(ano[2])+float(ano[4])/2)*height)
                cl = path_save + str(int(ano[0]))
                crop_img = img[y_min:y_max, x_min:x_max]

                are.append(crop_img.shape[0]*crop_img.shape[1])
                w.append(crop_img.shape[0])
                h.append(crop_img.shape[1])

                size = max(crop_img.shape[0], crop_img.shape[1])

                resized = cv2.resize(crop_img, (size, size), interpolation = cv2.INTER_AREA)

                #cv2.imwrite(cl + "/" + str(c) + ".jpg", resized)
        except:
            pass
        pass
    else:
        #copyfile(path_image + file, path_save + "test/" + file)
        pass

a_max, a_min = max(are), min(are)
imax, imin = are.index(a_max), are.index(a_min)

print(a_max, a_min)
print(w[imax], h[imax])
print(w[imin], h[imin])