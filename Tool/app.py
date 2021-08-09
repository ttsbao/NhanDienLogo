from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit
from flask_session import Session
import os
import base64
from PIL import Image
from io import BytesIO
import shutil
import sys
import datetime
import ruamel
from ruamel import yaml
import numpy as np
from sklearn.model_selection import train_test_split

# pip install ruamel.yaml
# pip install gevent, eventlet, socketIO-client
# pip install tf-nightly-gpu
# pip install subprocess

MAXSIZE = 10000000
ping = int((sys.maxsize)/100000000000000)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ttsbao'
socketio = SocketIO(app, ping_interval=ping, ping_timeout=ping)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOADED_PATH'] = os.path.join(app.root_path, 'upload')
Session(app)

CONTROL_ID = {}


path_client = "client/"

def esock(s, **kwargs):
    command, note = "  --> ", ""
    for k, v in kwargs.items():
        if k == "command":
            command = "  " + v + " "
        if k == 'note':
            note = str(v)
    if note == "":
        link = ""
    else:
        link = " " + command.replace(" ", "") + " "
    print(command + s + link + note)

def remove_dir(path):
    esock("Removing Directory: " + path, command="---")
    try:
        os.rmdir(path)
        esock("Rmoved")
    except FileNotFoundError:
        esock("Directory does not exist !!! ", note=path)
    except OSError as err:
        if 'The directory is not empty' in str(err):
            shutil.rmtree(path)
            esock("Removed With Shutil", note=path)

def create_dir(path):
    esock("Creating Directory", command="---", note=path)
    try:
        os.makedirs(path)
        esock("Created Directory", note=path)
    except FileExistsError:
        esock("Directory already exists !!!", note=path)


def close(client_key):
    print("* Close Project:", client_key, session.get(client_key))
    remove_dir(path_client + client_key)
    # # if session.get(client_key) == True:
    # #     print("Session ", client_key, " is training!, Can't Close")
    # # else:
    # #     print("Session Close: ", client_key)

@socketio.on('init_project')
def init(client_key):
    print("* Start project:", client_key)
    create_dir(path_client+client_key)
    client_dir = path_client + client_key + "/"
    create_dir(client_dir + "images")
    create_dir(client_dir + "labels")
    create_dir(client_dir + "weights")
    setItem([client_key, request.sid])

@socketio.on('init_progress')
def init_pro(data, name=None):
    if name is None:
        name = request.sid
    progress, total = data[0], data[1]
    key = "Progress|||"+progress+"|||"+name
    value = "0" + "|||" + str(total) + "|||" + "0"
    setItem([key, value])

def emit_client(data: object, client_key: object) -> object:
    emit('private_server', data, room=client_key)

def setPregressNoLenIDX(progress, rate, client_key):
    emit_client([progress, round(rate, 4), ''], client_key)

def setProgress(key, dataemit):
    data = session[key]
    data = data.split("|||")
    current = int(data[0]) + 1
    total = int(data[1])
    rate = round(current/total, 4)
    check_rate = int(rate*100)
    value = str(current) + "|||" + str(total) + "|||" + str(rate)
    session[key] = value
    keydata = key.split("|||")
    progress, client_key = keydata[1], keydata[2]
    if check_rate in [0, 50, 100]:
        esock('Progressing ' + progress + ': ' + str(rate) + "-" + str(check_rate) + "%", note=client_key)
    key_client = 'Progress' + "|||" + progress + "|||RJ"
    emit_client([key_client, rate, dataemit[0]], client_key)

@socketio.on('set-session')
def setItem(data, noprint=True):
    key, value = data[0], data[1]
    session[key] = value
    if noprint is True:
        esock("Set Session: " + str(key), note=value)

@socketio.on('pop-session')
def popItem(key, noprint=True):
    session.pop(key, None)
    if noprint is True:
        esock("Pop Session: " + str(key), note=None)


def msglist(msg):
    s = str(msg).split('-')
    for i in ['', ' ']:
        if i in s:
            s = [value for value in s if value != i]
    return s

@socketio.on('message')
def handleMessage(msg):
    #send(msg, broadcast=True)
    pass

@socketio.on('images-upload')
def imageUpload(data):
    client_key, name, type, img = data[0], data[1], data[2].split("/")[1], data[3]
    # print("  --- Uploading Images: ", client_key, name)
    path_save = path_client + client_key + "/images/" + name
    im = Image.open(BytesIO(base64.b64decode(img)))
    if 'png' not in type:
        im = im.convert('RGB')
    try:
        im.save(path_save, format=type)
        key = "Progress|||Upload_Images|||" + client_key
        value = [name]
        setProgress(key, value)
    except:
        esock("Error Saving Image Upload !!!")

@socketio.on('labels-upload')
def labelUpload(data):
    client_key, name, type, label = data[0], data[1], data[2].split("/")[1], data[3]
    path_save = path_client + client_key + "/labels/" + name
    lb = BytesIO(base64.b64decode(label))
    try:
        with open(path_save, "wb") as f:
            f.write(lb.getbuffer())
        key = "Progress|||Upload_Labels|||" + client_key
        value = [name]
        setProgress(key, value)
    except:
        esock("Error Saving Label Upload !!!")

@socketio.on('image-delete')
def imageDelete(name_img):
    client_key = request.sid
    path_file = path_client + client_key + "/images/" + name_img
    try:
        if os.path.exists(path_file):
            os.remove(path_file)
            esock("Removed Images", note=path_file)
        else:
            esock("Image Doesn't Exist", note=path_file)
    except:
        esock("Removed Image Error !!!", note=path_file)

@socketio.on('images-reset')
def imagesReset():
    client_key = request.sid
    client_dir = path_client + client_key + "/"
    esock("Reset Upload Images", note=client_dir + 'images')
    remove_dir(client_dir + "images")
    create_dir(client_dir + "images")
    emit_client(["ResetImages|||Done"], client_key)

@socketio.on('labels-reset')
def labelsReset():
    client_key = request.sid
    client_dir = path_client + client_key + "/"
    esock("Reset Upload Labels", note=client_dir + 'labels')
    remove_dir(client_dir + "labels")
    create_dir(client_dir + "labels")
    emit_client(["ResetLabels|||Done"], client_key)

@socketio.on('check_labels')
def checkLabels():
    client_key = request.sid
    client_dir = path_client + client_key + "/"
    im = client_dir + 'images/'
    lb = client_dir + 'labels/'
    l_im = os.listdir(im)
    l_imx = [y.split(".")[0] for y in l_im]
    l_c = [l_im[l_imx.index(x)] for x in l_imx if x not in [x.split(".")[0] for x in os.listdir(lb)]]
    emit_client(['CheckLabels|||', l_c], request.sid)

def makeYAML(client_key, nc, name):
    inp = """\
    path:  .
    train: train.txt
    val: val.txt
    test: test.txt
    nc: .
    names: .
    """
    code = ruamel.yaml.load(inp, Loader=ruamel.yaml.RoundTripLoader)
    code['path'] = "../client/" + client_key
    code['nc'] = nc
    code['names'] = name
    data = ruamel.yaml.dump(code, Dumper=ruamel.yaml.RoundTripDumper)
    data = data.replace('"', '')
    data = data.replace("\\", "")
    return data


@socketio.on('create-yaml')
def createYAML(msg):
    client_key = request.sid
    path = path_client + client_key + "/" + client_key + ".yaml"
    name = "["
    for i in msg:
        name += "'" + i + "', "
    name = name[:-2] + "]"
    data = makeYAML(client_key, len(msg), name)
    try:
        with open(path, 'w') as f:
            f.write(data)
        emit_client(['CreateYAML|||'], request.sid)
    except:
        esock("Error Creating YAML file", note=path)

@socketio.on('yaml-upload')
def uploadYAML(msg):
    client_key = request.sid
    path = path_client + client_key + "/" + client_key + ".yaml"
    s = BytesIO(base64.b64decode(msg)).read().decode("utf-8")
    s = s.replace("\r\n", "")
    indexnc = s.index("nc:")
    indexname = s.index("names:")
    nc = s[indexnc+3: indexname]
    if "#" in nc:
        indexh = nc.index("#")
        nc = nc[: indexh]
    nc = int(nc.replace(" ", ""))
    indexs, indexe = s.index("["), s.index("]")
    names = s[indexs:indexe+1]
    names = names.replace("  ", " ")
    names = names.replace("   ", " ")
    names = names.replace("  ", " ")
    data = makeYAML(request.sid, nc, names)
    for i in [" ", "[", "]", "'", '"']:
        names = names.replace(i, "")
    names = names.split(",")
    try:
        with open(path, 'w') as f:
            f.write(data)
        emit_client(['UploadYAML|||', names], request.sid)
    except:
        esock("Error Upload YAML file", note=path)


@socketio.on('upload-weight')
def uploadWeight(msg):
    part_data = base64.b64decode(msg[0])
    #part_data = msg[0]
    try:
        setItem(["Weights|||" + str(msg[1]) + "|||" + request.sid, part_data], noprint=False)
        key = "Progress|||Upload_Weights|||" + request.sid
        value = [msg[1]]
        setProgress(key, value)
    except:
        esock("Upload Weight Erro Part !!!")

@socketio.on('upload-video')
def uploadVideo(msg):
    part_data = base64.b64decode(msg[0])
    #part_data = msg[0]
    try:
        setItem(["Video|||" + str(msg[1]) + "|||" + request.sid, part_data], noprint=False)
        key = "Progress|||Upload_Video|||" + request.sid
        value = [msg[1]]
        setProgress(key, value)
    except:
        esock("Upload Weight Erro Part !!!")


@socketio.on('upload-detection')
def uploadCWeight(msg):
    part_data = base64.b64decode(msg[0])
    try:
        setItem(["Detection|||" + str(msg[1]) + "|||" + request.sid, part_data], noprint=False)
        key = "Progress|||Upload_Detection|||" + request.sid
        value = [msg[1]]
        setProgress(key, value)
    except:
        esock("Upload Detection Erro Part !!!")


@socketio.on('compress-upload-weight')
def compressUpLoadWeights():
    sizechunk = int(session["Progress|||Upload_Weights|||"+request.sid].split("|||")[1])
    data = session["Weights|||" + str(0) + "|||" + request.sid]
    popItem("Weights|||" + str(0) + "|||" + request.sid, noprint=False)
    path = path_client+request.sid+"/weights/" + "model.pt"
    for i in range(1, sizechunk):
        data += session["Weights|||" + str(i) + "|||" + request.sid]
        popItem("Weights|||" + str(i) + "|||" + request.sid, noprint=False)
    try:
        with open(path, "wb") as f:
            f.write(data)
            esock("Compress Weights Done!", note=path)
            emit_client(['Compress|||Done', None], request.sid)
    except:
        esock("Erro Compress Weights")

@socketio.on('compress-upload-video')
def compressUpLoadVideo():
    sizechunk = int(session["Progress|||Upload_Video|||"+request.sid].split("|||")[1])
    data = session["Video|||" + str(0) + "|||" + request.sid]
    popItem("Video|||" + str(0) + "|||" + request.sid, noprint=False)
    path = path_client+request.sid+"/weights/" + "video.mp4"
    for i in range(1, sizechunk):
        data += session["Video|||" + str(i) + "|||" + request.sid]
        popItem("Video|||" + str(i) + "|||" + request.sid, noprint=False)
    try:
        with open(path, "wb") as f:
            f.write(data)
            esock("Compress Video Done!", note=path)
            emit_client(['VideoCompress|||Done', None], request.sid)
            #exportVideo2()
    except:
        esock("Erro Compress Video")

def exportVideo2():
    client_key = request.sid
    client_dir = path_client + client_key + "/weights/video.mp4"
    data = createChunk(client_dir, MAXSIZE)
    emit_client(['ExportVideo|||len|||', len(data)], client_key)
    for i in range(len(data)):
        emit_client(['ExportVideo|||'+str(i)+'|||', data[i]], client_key)
        key = "Progress|||Object_Detection|||RJ"
        setPregressNoLenIDX(key, 0.85 + ((i + 1) / len(data)) / 6.5, client_key)
    emit_client(['FinishVideo|||'], client_key)

@socketio.on('compress-upload-detection')
def compressUpLoadCWeights():
    sizechunk = int(session["Progress|||Upload_Detection|||"+request.sid].split("|||")[1])
    data = session["Detection|||" + str(0) + "|||" + request.sid]
    popItem("Detection|||" + str(0) + "|||" + request.sid, noprint=False)
    path = path_client+request.sid+"/weights/" + "custom_model.pt"
    for i in range(1, sizechunk):
        data += session["Detection|||" + str(i) + "|||" + request.sid]
        popItem("Detection|||" + str(i) + "|||" + request.sid, noprint=False)
    try:
        with open(path, "wb") as f:
            f.write(data)
            esock("Compress Detection Done!", note=path)
            emit_client(['DetectionCompress|||Done', None], request.sid)
    except:
        esock("Erro Compress Weights")

@socketio.on('reset-model')
def resetModel():
    global test
    msg = test
    with open("test.mp4", "wb") as f:
        print("create")
        f.write(msg)

@socketio.on('control')
def setControl():
    global CONTROL_ID
    key = request.sid
    CONTROL_ID.update({key: None})
    print("* New Control Joined: ", key)

def setClientControl(client_key):
    global CONTROL_ID
    key = None
    check = True
    for k, v in CONTROL_ID.items():
        if v == client_key:
            check = False
            key = k
            break
    if check:
        for k, v in CONTROL_ID.items():
            if v is None:
                key = k
                CONTROL_ID.update({k: client_key})
    esock("Control_ID", note=CONTROL_ID[key])

def findControl(client_key):
    global CONTROL_ID
    for k, v in CONTROL_ID.items():
        if v == client_key:
            return k
    return None

def callTrain(control_id):
    emit('train', room=control_id)

def callTest(control_id):
    emit('test', room=control_id)

def callSet(control_id, data):
    emit('config', data, room=control_id)

def callSetDetect(control_id, data):
    emit('config-d', data, room=control_id)

def callDetection(control_id):
    emit('detect', room=control_id)

def callKill(control_id):
    global CONTROL_ID
    for k, v in CONTROL_ID.items():
        if k == control_id:
            emit('kill', room=control_id)
            CONTROL_ID.update({k: None})
            esock("Set Control", note=CONTROL_ID[k])

global idx
@socketio.on('yolo')
def yolomess(msg):
    data, client_id, type = msg[0], msg[1], msg[2]
    # global idx
    # client_id = idx
 
    if type is None:
        if 'Model Summary' in data:
            emit_client(['Progress_Step|||Checking|||0|||0', str(1.0)], client_id)
        if 'Optimizer stripped' not in data:
            emit_client(['TrainConsole|||' + data], client_id)
    else:
        mode = type.split("|||")

        if 'Start Scan|||TRAIN|||' in type:
            emit_client(['TrainConsole|||' + data + "..."], client_id)
            emit_client(['Progress_Step|||Preprocessing|||1|||1', str(0.0)], client_id)
        if 'Scanning|||TRAIN|||' in type and 'Start' not in type:
            if mode[2] != 'OK':
                emit_client(['TrainConsole|||' + data + "... " + str(float(mode[2]) * 100) + "%"], client_id)
                emit_client(['Progress_Step|||Preprocessing|||1|||1', str(float(mode[2])/2.5)], client_id)
            else:
                #emit_client(['TrainConsole|||' + data + "... 100%"], client_id)
                emit_client(['Progress_Step|||Preprocessing|||1|||1', str(0.4)], client_id)
                
        if 'Start Caching|||TRAIN|||' in type:
            emit_client(['TrainConsole|||' + data + "..."], client_id)
            emit_client(['Progress_Step|||Preprocessing|||1|||1', str(0.4)], client_id)
        if 'Caching|||TRAIN|||' in type and 'Start' not in type:
            if mode[2] != 'OK':
                emit_client(['TrainConsole|||' + data + "... " + str(float(mode[2]) * 100) + "%"], client_id)
                emit_client(['Progress_Step|||Preprocessing|||1|||1', str((float(mode[2])/2.5) + 0.4)], client_id)
            else:
                #emit_client(['TrainConsole|||' + data + "... 100%"], client_id)
                emit_client(['Progress_Step|||Preprocessing|||1|||1', str(0.8)], client_id)

        if 'Start Scan|||VAL|||' in type:
            emit_client(['TrainConsole|||' + data + "..."], client_id)
            emit_client(['Progress_Step|||Preprocessing|||1|||1', str(0.8)], client_id)
        if 'Scanning|||VAL|||' in type and 'Start' not in type:
            if mode[2] != 'OK':
                emit_client(['TrainConsole|||' + data + "... " + str(float(mode[2]) * 100) + "%"], client_id)
                emit_client(['Progress_Step|||Preprocessing|||1|||1', str((float(mode[2]) / 10) + 0.8)], client_id)
            else:
                #emit_client(['TrainConsole|||' + data + "... 100%"], client_id)
                emit_client(['Progress_Step|||Preprocessing|||1|||1', str(1.0)], client_id)

        if 'Start Caching|||VAL|||' in type:
            emit_client(['TrainConsole|||' + data + "..."], client_id)
            emit_client(['Progress_Step|||Preprocessing|||1|||1', str(0.9)], client_id)
        if 'Caching|||VAL|||' in type and 'Start' not in type:
            if mode[2] != 'OK':
                emit_client(['TrainConsole|||' + data + "... " + str(float(mode[2]) * 100) + "%"], client_id)
                emit_client(['Progress_Step|||Preprocessing|||1|||1', str((float(mode[2]) / 10) + 0.9)], client_id)
            else:
                #emit_client(['TrainConsole|||' + data + "... 100%"], client_id)
                emit_client(['Progress_Step|||Preprocessing|||1|||1', str(1.0)], client_id)

        if 'Start Training|||' in type:
            emit_client(['TrainConsole|||' + data + "..."], client_id)
            emit_client(['Progress_Step|||Training|||1|||2', str(0.0)], client_id)
        if 'Training|||' in type and 'Start' not in type:
            if mode[1] != 'OK':
                emit_client(['TrainConsole|||' + data + "... " + str(float(mode[1]) * 100) + "%"], client_id)
                emit_client(['Progress_Step|||Training|||1|||2', str(float(mode[1]))], client_id)
            else:
                emit_client(['Progress_Step|||Training|||1|||2', str(1.0)], client_id)
                trainCompleted(client_id)

@socketio.on('test-model')
def testModel():
    client_key = request.sid
    setClientControl(client_key)
    control_id = findControl(client_key)
    callTest(control_id)

@socketio.on('kill-train')
def killModel():
    client_key = request.sid
    setClientControl(client_key)
    control_id = findControl(client_key)
    client_dir = path_client + client_key + "/"
    remove_dir(client_dir + "train")
    create_dir(client_dir + "train")
    callKill(control_id)
    emit_client(['KillTrain|||'], client_key)


@socketio.on('train-model')
def trainModel(data):
    # global idx
    # idx = request.sid
    client_key = request.sid
    setClientControl(client_key)
    control_id = findControl(client_key)
    client_dir = path_client + client_key + "/"
    remove_dir(client_dir + "train")
    create_dir(client_dir + "train")
    emit_client(['Progress_Step|||Checking|||0|||0', str(0.2)], request.sid)
    hold_out(request.sid)
    emit_client(['Progress_Step|||Checking|||0|||0', str(0.5)], request.sid)

    img, batch, epoch, name = data[0], data[1], data[2], client_key
    if data[3] == -1:
        w = "../client/" + name + "/weights/model.pt"
    else:
        w = "yolov5s.pt"
    para = [img, batch, epoch, name, w]
    callSet(control_id, para)
    emit_client(['Progress_Step|||Checking|||0|||0', str(0.8)], request.sid)
    callTrain(control_id)

def trainCompleted(client_key):
    w = path_client + client_key + "/train/exp/weights/best.pt"
    d = path_client + client_key + "/weights/best.pt"
    c = path_client + client_key + "/weights/custom_model.pt"
    try:
        shutil.copyfile(w, d)
        shutil.copyfile(w, c)
    except FileNotFoundError:
        w = path_client + client_key + "/train/exp/weights/last.pt"
        shutil.copyfile(w, d)
        shutil.copyfile(w, c)
    emit_client(['Progress_Step|||Completed|||2|||3', str(5.0)], client_key)
    emit_client(['ModelStep'], client_key)

@socketio.on('compress_video_export')
def compress_done():
    ci = findControl(request.sid)
    callKill(ci)
    key = "Progress|||Object_Detection|||RJ"
    setPregressNoLenIDX(key, 1.0, request.sid)
    client_dir = path_client + request.sid + "/detect/"
    remove_dir(client_dir)
    create_dir(client_dir)


def createChunk(filepath, csize):
    chunks = []
    with open(filepath, "rb") as fp:
        data = fp.read()
    data = base64.b64encode(data).decode('utf-8')
    start = 0
    end = len(data)
    while start < end:
        new = start + csize
        chunks.append(data[start:new])
        start = new
    return chunks

@socketio.on('export_video')
def exportVideo():
    client_key = request.sid
    client_dir = path_client + client_key + "/weights/export_video.mp4"
    data = createChunk(client_dir, MAXSIZE)
    emit_client(['ExportVideo|||len|||', len(data)], client_key)
    for i in range(len(data)):
        emit_client(['ExportVideo|||'+str(i)+'|||', data[i]], client_key)
        key = "Progress|||Object_Detection|||RJ"
        setPregressNoLenIDX(key, 0.85 + ((i + 1) / len(data)) / 6.5, client_key)
    emit_client(['FinishVideo|||'], client_key)

@socketio.on('export_model')
def exportModel():
    client_key = request.sid
    client_dir = path_client + client_key + "/weights/best.pt"
    data = createChunk(client_dir, MAXSIZE)
    emit_client(['ExportModel|||len|||', len(data)], client_key)
    init_pro(['Train_Model', len(data)], name=client_key)
    for i in range(len(data)):
        emit_client(['ExportModel|||'+str(i)+'|||', data[i]], client_key)
        key = "Progress|||Train_Model|||" + request.sid
        value = [str(i+1)]
        setProgress(key, value)
    emit_client(['FinishModel|||'], client_key)
    emit_client(['Progress_Step|||Completed|||2|||3', str(9.0)], client_key)
    emit_client(['YAMLStep'], client_key)

@socketio.on('export_yaml')
def exportYAML():
    client_key = request.sid
    client_dir = path_client + client_key + "/" + client_key + ".yaml"
    data = createChunk(client_dir, MAXSIZE)
    emit_client(['ExportYAML|||len|||', len(data)], client_key)
    for i in range(len(data)):
        print(i, ": ", len(data[i]), data[i])
        emit_client(['ExportYAML|||'+str(i)+'|||', data[i]], client_key)
    emit_client(['FinishYAML|||'], client_key)
    emit_client(['Progress_Step|||Completed|||2|||3', str(1.0)], client_key)
    control_id = findControl(client_key)
    callKill(control_id)


def hold_out(client_key):
    client_dir = path_client + client_key + "/"
    im = client_dir + 'images/'
    lb = client_dir + 'labels/'
    l_im = os.listdir(im)
    l_imx = [y.split(".")[0] for y in l_im]
    l_c = [l_im[l_imx.index(x)] for x in l_imx if x not in [x.split(".")[0] for x in os.listdir(lb)]]
    X = ['./images/' + x for x in l_im if x not in l_c]
    if len(X) < 4:
        emit_client(["TrainError|||The number of training set is too small"], client_key)
    else:
        emit_client(['Progress_Step|||Checking|||0|||0', str(0.6)], request.sid)
        X = np.reshape(np.array(X, dtype=object), (len(X), 1))
        y = np.ones(X.shape[0])
        train, val_test, __, _ = train_test_split(X, y, test_size=0.3, shuffle=True)
        val, test, __, _ = train_test_split(val_test, _, test_size=2/3, shuffle=True)
        emit_client(['Progress_Step|||Checking|||0|||0', str(0.8)], request.sid)
        try:
            np.savetxt(client_dir + "train.txt", train, fmt="%s")
            np.savetxt(client_dir + "val.txt", val, fmt="%s")
            np.savetxt(client_dir + "test.txt", test, fmt="%s")
            emit_client(['Progress_Step|||Checking|||0|||0', str(1)], request.sid)
        except:
            emit_client(["TrainError|||The number of training set is too small"], client_key)

@socketio.on('yolo-detection')
def msgDetection(msg):
    data, client_key, type = msg[0], msg[1], msg[2]
    idpro = 'Progress|||Object_Detection|||RJ'
    if type == 'Step':
        setPregressNoLenIDX(idpro, float(data)/1.25 + 0.05, client_key)
    if type == 'OK':
        setPregressNoLenIDX(idpro, 1 / 1.25 + 0.05, client_key)
        emit_client(['DetectionDone|||'], client_key)
        w = path_client + client_key + "/detect/" + client_key + "/video.mp4"
        d = path_client + client_key + "/weights/export_video.mp4"
        try:
            shutil.copyfile(w, d)
            setPregressNoLenIDX(idpro, 0.85, client_key)
        except FileNotFoundError:
            pass

@socketio.on('object-detection')
def object_detection(data):
    client_key = request.sid
    client_dir = path_client + client_key + "/detect/"
    remove_dir(client_dir)
    create_dir(client_dir)
    img, th, iou, maxd, name = data[0], data[1], data[2], data[3], client_key
    datasend = [img, th, iou, maxd, name]
    setClientControl(client_key)
    control_id = findControl(client_key)
    callSetDetect(control_id, datasend)
    socketio.sleep(5)
    callDetection(control_id)
    setPregressNoLenIDX('Progress|||Object_Detection|||RJ', 0.05, client_key)


@socketio.on('client_disconnecting')
def disconnect_details(data):
    popItem(data['client_key'])
    close(data['client_key'])

def init_server():
    print("* Starting Server")
    interval = datetime.timedelta(seconds=ping)
    timeout = datetime.timedelta(seconds=ping)
    esock("Set Ping Interval", note=interval)
    esock("Set Ping Time Out", note=timeout)

    print("* Cleaning Server")
    if os.path.isdir(path_client) is True:
        client_list = os.listdir(path_client)
        for i in client_list:
            remove_dir(path_client + i)
    else:
        create_dir('client')
    esock("Cleaned")

@app.route("/", methods = ['POST', 'GET'])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    init_server()
    socketio.run(app)
    app.run(debug=True)
