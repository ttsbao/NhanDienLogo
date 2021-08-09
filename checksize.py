import cv2
import os

path = "D:/Project/MachineLearning/NhanDienLogo/datasets/Logo/"
dir = path + "images/"

size = []

file = os.listdir(dir+"/")
j = 0
for i in file:
    print(j, " - ", len(file))
    img = cv2.imread(dir+i, cv2.IMREAD_UNCHANGED)
    try:
        s = img.shape
        w, h = s[0], s[1]
        if w not in size:
           size.append(w)
        if h not in size:
            size.append(h)
    except:
        pass
    j += 1

print(max(size), min(size))

