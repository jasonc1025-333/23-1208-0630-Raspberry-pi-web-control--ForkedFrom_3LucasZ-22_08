from picamera import PiCamera
import time
from flask import Flask, render_template
from flask_socketio import SocketIO


app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def home():
    camera = PiCamera()
    camera.resolution = (300, 300)
    camera.start_preview()
    time.sleep(2)
    return 'hello'


@socketio.on('connect')
def connect():
    print('A client connected.')
    

@socketio.on('disconnect')
def disconnect():
    print('A client disconnected.')


def capture():
    camera.capture('static/picture.jpg')


if __name__ == "__main__":
    #will run on: http://192.168.1.162:8080/
    app.run(host='0.0.0.0', port=8080, debug=True)
