from flask import Flask,request, render_template
from flask_socketio import SocketIO
import cv2
import base64

#app set up
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

#camera set up
#use primary camera
camera = cv2.VideoCapture(0)
#camera resolution
camera.set(3, 64)
camera.set(4, 64)
#stream fps
FPS = 30


#give client camera data stream
@socketio.on('server')
def send_camera_stream():
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


#serve starting web page via http
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)