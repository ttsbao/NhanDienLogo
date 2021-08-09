import subprocess
import socketio
import sys
import os
import signal

path = os.path.dirname(os.path.abspath(__file__))+ "\\"
train = path + "train.py"
test = path + "test.py"
detect = path + "detect.py"

class Control:
    def __init__(self):
        self.p = None
        self.img = "240"
        self.batch = "4"
        self.epochs = "10"
        self.project = "../clienta/Khry8IBR8PfFqf0nAAAD/train"
        self.data = "../clienta/Khry8IBR8PfFqf0nAAAD/Khry8IBR8PfFqf0nAAAD.yaml"
        self.weights = "yolov5s.pt"
        self.name = None
        print("Contruction Control")

    def set(self, l: list):
        self.img = str(l[0])
        self.batch = str(l[1])
        self.epochs = str(l[2])
        self.project = "../client/" + l[3] + "\\train"
        self.data = "../client/" + l[3] + "\\" + l[3] + ".yaml"
        self.weights = l[4]
        self.name = l[3]

    def set_d(self, l: list):
        self.img_d = str(l[0])
        self.th_d = str(l[1])
        self.iou_d = str(l[2])
        self.max_d = str(l[3])
        self.w_d = "../client/" + l[4] + "/weights/custom_model.pt"
        self.s_d = "../client/" + l[4] + "/weights/video.mp4"
        self.p_d = "../client/" + l[4] + "/detect"
        self.name_d = l[4]

    def detect(self):
        self.p = subprocess.Popen(
            ["python", detect,
             "--img", self.img_d, "--iou", self.iou_d, "--conf", self.th_d, '--half',
             "--project", self.p_d, "--name", self.name_d, "--max", self.max_d,
             "--weights", self.w_d, "--source", self.s_d], shell=True)
        result = self.p.communicate()
        print(result)

    def train(self):
        self.p = subprocess.Popen(
            ["python", train,
             "--img", self.img, "--batch", self.batch,  "--epochs", self.epochs,
             "--project", self.project, "--data", self.data, "--cache-images",
             "--weights", self.weights, "--nosave"], shell=True)
        result = self.p.communicate()
        print(result)

    def test(self):
        self.p = subprocess.Popen(
            ["python", test,
             "--img", self.img, "--iou", str(0.65),
             "--weights",  "../client/" + self.name + "/weights/best.pt",
             "--data", "../client/" + self.name + "/" + self.name + ".yaml",
             "--half"], shell=True)

        result = self.p.communicate()
        print(result)

    def kill(self):
        os.kill(self.p.pid, signal.CTRL_C_EVENT)



control = Control()

sio = socketio.Client()
sio.connect('http://127.0.0.1:5000')


def emit_server(msg):
    sio.emit('yolo', msg)


sio.emit('control')

@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")

@sio.on('config')
def callconfig(data):
    print("Init Train")
    control.set(data)

@sio.on('train')
def calltrain():
    print("Train")
    control.train()

@sio.on('test')
def calltest():
    print("Test")
    control.test()

@sio.on('kill')
def callkill():
    print("Kill")
    control.kill()

@sio.on('mess')
def mess(data):
    print(data)

@sio.on('config-d')
def callconfig_d(data):
    print("Init Detection")
    control.set_d(data)

@sio.on('detect')
def calltrain():
    print("Detection")
    control.detect()









# subprocess.call(["python", pathfile,
#                  "--img", "240", "--batch", "4",  "--epochs", "1",
#                  "--project", "../clienta/Khry8IBR8PfFqf0nAAAD/train",
#                  "--nosave",
#                  "--data", "../clienta/Khry8IBR8PfFqf0nAAAD/Khry8IBR8PfFqf0nAAAD.yaml",
#                  "--weights", "yolov5s.pt",
#                  "--cache"])
