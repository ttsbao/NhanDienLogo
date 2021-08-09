import socketio

class Server():
    def __init__(self):
        self.sio = socketio.Client()
        self.sio.connect('http://localhost:5000')
        self.sid = self.sio.sid
        #self.sio.emit('yolo', "Connected Yolo")
        self.client_key = None

    def emit_server(self, msg, type=None):
        self.sio.emit('yolo', [msg, self.client_key, type])

    def emit_detect(self, msg, type=None):
        self.sio.emit('yolo-detection', [msg, self.client_key, type])

    def get_name(self, data):
        if "\\" in data:
            data = data.replace("\\", "/")
        data = data.split("/")[-1]
        return data.split(".")[0]

    def set_client_key(self, key):
        self.client_key = key