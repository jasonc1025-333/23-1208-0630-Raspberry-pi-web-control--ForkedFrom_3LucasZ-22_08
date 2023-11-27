#IMPORTS
#websocket and flask
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit, send


#video stream
# jwc, install simply and briefly 'sudo apt install python3-opencv'
import cv2
import base64


###jwc o #motor control
###jwc o import RPi.GPIO as GPIO
###jwc o import smbus2 as smbus
###jwc o from Modules.utils import int_to_byte_array
import time


###jwc o #rplidar
###jwc o import os
###jwc o from math import floor
###jwc o  from adafruit_rplidar import RPLidar


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
FPS = 10
sentCamera = False


###jwc o #motor setup
###jwc o PIN_I2C6_POWER_ENABLE = 17
###jwc o bus = smbus.SMBus(1)
###jwc o DEVICE_ADDRESS = 0x53
###jwc o GPIO.setmode(GPIO.BCM)
###jwc o time.sleep(0.1) #important
###jwc o GPIO.setup(PIN_I2C6_POWER_ENABLE, GPIO.OUT)
###jwc o time.sleep(0.1) #important
###jwc o speed = 50

#debug
###jwc o prev_t_lidar = 0
prev_t_cam = 0

###jwc o # Setup the RPLidar
###jwc o PORT_NAME = '/dev/ttyUSB0'
###jwc o lidar = RPLidar(None, PORT_NAME, timeout=3)
###jwc o sentLidar = False
###jwc o #360 element array of distances
###jwc o scan_data = [0]*360


#INFINITE SENDING
#constantly send camera data if client send needCamera message
@socketio.on('needCamera')
def send_camera():
    global prev_t_cam
    print("sending cam data now")
    while True:
        retval, frame = camera.read()
        #my camera is placed upside down ._.
        #to get the correct image, we must flip the camera vertically and horizontally
        frame = cv2.flip(frame, -1)
        retval, jpg = cv2.imencode('.jpg', frame)
        jpg_as_text = str(base64.b64encode(jpg))
        jpg_as_text = jpg_as_text[2:-1]
        emit('jpg_string', jpg_as_text)
        print("sent a picture. time: " + str(time.time()-prev_t_cam))
        prev_t_cam = time.time()
        socketio.sleep(1/FPS)


###jwc o #constantly send lidar data if client sends needLidar message
###jwc o @socketio.on('needLidar')
###jwc o def send_lidar():
###jwc o     global prev_t_lidar
###jwc o     print("sending lidar data now")
###jwc o  
###jwc o     #get the most recent scans from scan generator
###jwc o     counter = 0
###jwc o     for scan in lidar.iter_scans(3):
###jwc o         counter += 1 
###jwc o         #scan has array of points
###jwc o         #each point has 3 properties: quality, angle, distance
###jwc o         for (_, angle, distance) in scan:
###jwc o             #ensure accessing index in range
###jwc o             scan_data[min([359, floor(angle)])] = int(distance)
###jwc o             socketio.sleep(0)
###jwc o         #send all clients scan_data array
###jwc o         #print(scan_data)
###jwc o         if counter % 5 == 0:
###jwc o             emit("scanData", scan_data)
###jwc o             print("sent a scan. time: " + str(time.time()-prev_t_lidar))
###jwc o             prev_t_lidar = time.time()
###jwc o         socketio.sleep(0)


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
    ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(speed))
    ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(-1 * speed))
    print("turn left received")


@socketio.on('turnRight')
def turn_right():
    ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(-1 * speed))
    ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(speed))
    print("turn right received")


@socketio.on('forward')
def forward():
    ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(speed))
    ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(speed))
    print("forward received")


@socketio.on('backward')
def backward():
    ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(-1 * speed))
    ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(-1 * speed))
    print("backward received")


@socketio.on('stopMotors')
def stop_motors():
    ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(0))
    ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(0))
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

#PROGRAM CLEAN UP
GPIO.cleanup()
###jwc o lidar.stop()
###jwc o lidar.disconnect()
