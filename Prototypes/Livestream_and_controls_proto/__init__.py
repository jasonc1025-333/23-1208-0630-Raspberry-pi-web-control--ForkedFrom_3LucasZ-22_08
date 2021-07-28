from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import cv2

app = Flask(__name__)
socketio = SocketIO(app)
camera = cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


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


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='8080')