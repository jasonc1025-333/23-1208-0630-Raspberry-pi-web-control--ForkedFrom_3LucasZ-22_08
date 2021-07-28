from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import cv2
import time
import RPi.GPIO as GPIO
import smbus2 as smbus
import int_to_byte

#App set up
app = Flask(__name__)
socketio = SocketIO(app)
#Camera set up
camera = cv2.VideoCapture(0)
time.sleep(3)
camera.set(3, 80)
camera.set(4, 80)
#motor setup
PIN_I2C6_POWER_ENABLE = 17
bus = smbus.SMBus(3)
DEVICE_ADDRESS = 0x53
GPIO.setmode(GPIO.BCM)
time.sleep(0.1) #important
GPIO.setup(PIN_I2C6_POWER_ENABLE, GPIO.OUT)
time.sleep(0.1) #important
speed = 50

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
    motors_on()
    print('A client connected.')


@socketio.on('disconnect')
def disconnect():
    motors_off()
    print('A client disconnected.')


@socketio.on('motorsOn')
def motors_on():
    GPIO.output(PIN_I2C6_POWER_ENABLE, GPIO.HIGH)
    print("motor on received")


@socketio.on('motorsOff')
def motors_off():
    GPIO.output(PIN_I2C6_POWER_ENABLE, GPIO.LOW)
    print("motor off received")


@socketio.on('turnLeft')
def turn_left():
    bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(speed))
    bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(-1 * speed))
    print("turn left received")
    time.sleep(0.1)
    stop_motors()


@socketio.on('turnRight')
def turn_right():
    bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(-1 * speed))
    bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(speed))
    print("turn right received")
    time.sleep(0.1)
    stop_motors()


@socketio.on('forward')
def forward():
    bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(speed))
    bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(speed))
    print("forward received")
    time.sleep(0.1)
    stop_motors()

@socketio.on('backward')
def backward():
    bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(-1 * speed))
    bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(-1 * speed))
    print("backward received")
    time.sleep(0.1)
    stop_motors()

def stop_motors():
    bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(0))
    bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(0))
    print("stop motors received")


@socketio.on('setSpeed')
def set_speed(data):
    global speed
    speed = int(data)
    print("Speed:", speed)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='8080', threaded=True)