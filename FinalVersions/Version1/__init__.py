#IMPORTS
#websocket and flask
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit, send


#video stream
import cv2
import base64


#motor control
import RPi.GPIO as GPIO
import smbus2 as smbus
import int_to_byte
import time


#rplidar
import os
from math import floor
from adafruit_rplidar import RPLidar


#other
import sys


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
FPS = 20
sentCamera = False


#motor setup
PIN_I2C6_POWER_ENABLE = 17
bus = smbus.SMBus(3)
DEVICE_ADDRESS = 0x53
GPIO.setmode(GPIO.BCM)
time.sleep(0.1) #important
GPIO.setup(PIN_I2C6_POWER_ENABLE, GPIO.OUT)
time.sleep(0.1) #important
speed = 50


# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)
sentLidar = False
#360 element array of distances
scan_data = [0]*360


#INFINITE SENDING
#constantly send camera data to clients who send needCamera message
@socketio.on('needCamera')
def send_camera():
    while True:
        retval, frame = camera.read()
        #my camera is placed upside down ._.
        #to get the correct image, we must flip the camera vertically and horizontally
        frame = cv2.flip(frame, -1)
        retval, jpg = cv2.imencode('.jpg', frame)
        jpg_as_text = str(base64.b64encode(jpg))
        jpg_as_text = jpg_as_text[2:-1]
        emit('jpg_string', jpg_as_text)
        socketio.sleep(1/FPS)


#constantly send lidar data to clients who send needLidar message
@socketio.on('needLidar')
def send_lidar():
    try:
        while True:
            #get the most recent scans from scan generator
            for scan in lidar.iter_scans(3): 
                #scan has array of points
                #each point has 3 properties: quality, angle, distance
                for (_, angle, distance) in scan:
                    #ensure accessing index in range
                    scan_data[min([359, floor(angle)])] = distance
                    print(distance)
                    print(type(distance))
                    print(sys.getsizeof(distance))
                    print(sys.getsizeof(int(distance)))
                #send all clients scan_data array
                #print(scan_data)
                emit("scanData", scan_data)
                socketio.sleep(0)
           
    except KeyboardInterrupt:
        print('Stopping.')

    lidar.stop()
    lidar.disconnect()


#COMMAND LISTENERS
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
#serve the webpage when a client connects to IP:5000
@app.route('/')
def home():
    return render_template('index.html')


#RUN THE APP
if __name__ == '__main__':
    print("ready for clients!")
    socketio.run(app, host='0.0.0.0', port=5000)