#IMPORTS
from flask import Flask,request, render_template
from flask_socketio import SocketIO
import cv2
import base64
import RPi.GPIO as GPIO
import smbus2 as smbus
import int_to_byte
import time


#SETUP
#set up app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)


#camera setup
camera = cv2.VideoCapture(0)
time.sleep(1)
camera.set(3, 64)
camera.set(4, 64)
FPS = 30


#motor setup
PIN_I2C6_POWER_ENABLE = 17
bus = smbus.SMBus(3)
DEVICE_ADDRESS = 0x53
GPIO.setmode(GPIO.BCM)
time.sleep(0.1) #important
GPIO.setup(PIN_I2C6_POWER_ENABLE, GPIO.OUT)
time.sleep(0.1) #important
speed = 50


#SENDERS
#constantly send camera data
@socketio.on('needCamera')
def sendCamera():
    while True:
        retval, frame = camera.read()
        #my camera is placed upside down ._.
        #to get the correct image, we must flip the camera vertically and horizontally
        frame = cv2.flip(frame, -1)
        retval, jpg = cv2.imencode('.jpg', frame)
        jpg_as_text = str(base64.b64encode(jpg))
        jpg_as_text = jpg_as_text[2:-1]
        socketio.emit('jpg_string', jpg_as_text)
        socketio.sleep(1/FPS)


#LISTENERS
@socketio.on('connect')
def connect():
    print('A client connected.')


@socketio.on('disconnect')
def disconnect():
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


@socketio.on('turnRight')
def turn_right():
    bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(-1 * speed))
    bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(speed))
    print("turn right received")


@socketio.on('forward')
def forward():
    bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(speed))
    bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(speed))
    print("forward received")


@socketio.on('backward')
def backward():
    bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(-1 * speed))
    bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(-1 * speed))
    print("backward received")


@socketio.on('stopMotors')
def stop_motors():
    bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(0))
    bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(0))
    print("stop motors received")


@socketio.on('setSpeed')
def set_speed(data):
    global speed
    speed = int(data)
    print("Speed:", speed)


#FLASK SERVING
@app.route('/')
def home():
    return render_template('index.html')


#RUN APP
if __name__ == '__main__':
    print("ready for clients!")
    socketio.run(app, host='0.0.0.0', port=5000)