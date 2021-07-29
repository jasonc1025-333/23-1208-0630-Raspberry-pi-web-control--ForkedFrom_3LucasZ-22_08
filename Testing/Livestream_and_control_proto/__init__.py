from flask import Flask,request, render_template
from flask_socketio import SocketIO
import cv2
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)
camera = cv2.VideoCapture(0)
camera.set(3, 64)
camera.set(4, 64)
FPS = 30

@socketio.on('server')
def sendmessage():
    while True:
        retval, frame = camera.read()
        retval, jpg = cv2.imencode('.jpg', frame)
        jpg_as_text = str(base64.b64encode(jpg))
        jpg_as_text = jpg_as_text[2:-1]
        socketio.emit('jpg_string', jpg_as_text)
        socketio.sleep(1/FPS)

@socketio.on('connect')
def connect():
    print('A client connected.')

@socketio.on('disconnect')
def disconnect():
    print('A client disconnected.')

@socketio.on('motorsOn')
def motors_on():
    print("motor on received")

@socketio.on('motorsOff')
def motors_off():
    print("motor off received")

@socketio.on('turnLeft')
def turn_left():
    print("turn left received")

@socketio.on('turnRight')
def turn_right():
    print("turn right received")

@socketio.on('forward')
def forward():
    print("forward received")

@socketio.on('backward')
def backward():
    print("backward received")

@socketio.on('setSpeed')
def set_speed(speed):
    print("Speed:", int(speed))

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)