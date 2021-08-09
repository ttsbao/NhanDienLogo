import subprocess
import os
import socketio

path = os.path.dirname(os.path.abspath(__file__))+ "\\"
train = path + "train.py"
test = path + "test.py"
detect = path + "detect.py"

class Control:
    def __init__(self):
        self.p = None
        self.img = "240"
        self.batch = "4"
        self.epochs = "1"
        self.project = "../clienta/Khry8IBR8PfFqf0nAAAD/train"
        self.data = "../clienta/Khry8IBR8PfFqf0nAAAD/Khry8IBR8PfFqf0nAAAD.yaml"
        self.weights = "yolov5s.pt"

    def set(self, l: list):
        self.img = str(l[0])
        self.batch = str(l[1])
        self.epochs = str(l[2])
        self.project = "../clienta/" + l[3] + "\\train"
        self.data = "../clienta/" + l[3] + "\\" + l[3] + ".yaml"
        self.weights = l[4]

    def train(self):
        self.p = subprocess.Popen(
            ["python", train,
             "--img", self.img, "--batch", self.batch,  "--epochs", self.epochs,
             "--project", self.project, "--data", self.data,
             "--weights", self.weights, "--nosave", "--cache"])

    def kill(self):
        self.p.terminate()

# cmd = ["python", train, "--img", "240", "--batch", "4", "--epochs", "10", "--project", "../clienta/Khry8IBR8PfFqf0nAAAD/train", "--data", "../clienta/Khry8IBR8PfFqf0nAAAD/Khry8IBR8PfFqf0nAAAD.yaml","--weights", "yolov5s.pt", "--nosave", "--cache"]

l =  [240, 0.25, 0.45, 500, 'vXFFE9m72J2eNh3DAAAL']

img_d = str(l[0])
th_d = str(l[1])
iou_d = str(l[2])
max_d = str(l[3])
w_d = "../client/" + l[4] + "/weights/custom_model.pt"
s_d = "../client/" + l[4] + "/weights/video.mp4"
p_d = "../client/" + l[4] + "/detect"
name_d = l[4]

cmd = ["python", detect,
             "--img", img_d, "--iou", iou_d, "--conf", th_d, '--half',
             "--project", p_d, "--name", name_d, "--max", max_d,
             "--weights", w_d, "--source", s_d]

import sys

proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
# result = proc.communicate()
# print(result)

while True:
    line = proc.stdout.readline()
    print("test:", line.strip())
    sys.stdout.flush()




