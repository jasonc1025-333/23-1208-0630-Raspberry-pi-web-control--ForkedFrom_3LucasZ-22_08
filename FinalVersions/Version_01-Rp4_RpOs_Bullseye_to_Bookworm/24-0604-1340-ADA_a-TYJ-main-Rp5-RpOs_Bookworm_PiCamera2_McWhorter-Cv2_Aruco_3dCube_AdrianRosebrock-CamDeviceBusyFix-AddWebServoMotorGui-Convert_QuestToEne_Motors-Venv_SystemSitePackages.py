#IMPORTS
#websocket and flask
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit, send

# * SocketIO will use the following WSGI servers even if not imported with this file.  
# * As long as 'pip3 install' in OS, will be activated in this order
#   * 'eventlet', 'gevent' then 'flask'
#     * 'eventlet' and 'flask' works
#     * 'gevent' not work
#

# pip3 install eventlet
# TYJ Works
import eventlet

# jwc hopefully to resolve 'RuntimeError: Cannot obtain socket from WSGI environment'
# jwc not work for socketio: from waitress import serve

# NOT GOOD: pip3 install gevent & gevent-websocket
# HUJ not work
# * https://flask.palletsprojects.com/en/1.1.x/deploying/wsgi-standalone/ : Gevent
###jwc n from gevent.pywsgi import WSGIServer


#video stream
import cv2
import base64

# jwc RpOs Bullseye
#
from picamera2 import Picamera2


#motor control
import RPi.GPIO as GPIO
import smbus2 as smbus
###jwc o from Modules.utils import int_to_byte_array
###jwc o from time import sleep
import time

# jwc y Create 'symbolic_link' to access a local_library_folder 'Servos': 23-1207-1325: from Servos import servo_settings 
# jwc Created 'ln -sv ../Servos/ ./Servos'
###jwc 24-0529-2230 Rp4>Rp5 y: from Servos import servo_controller as sc


#laser
import RPi.GPIO as GPIO

###jwc o #rplidar
###jwc o import os
###jwc o from math import floor
###jwc o from adafruit_rplidar import RPLidar


### jwc o #other
### jwc o import sys

#
# Setup: Aruco Markers
#
import imutils
import argparse
import sys

# jwc 
#
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-t", "--type", type=str,
    default="DICT_ARUCO_ORIGINAL",
    help="type of ArUCo tag to detect")

args = vars(ap.parse_args())

# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
    "DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
    "DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
    "DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
    "DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

###jwc n ARUCO_DICT = {
###jwc n     "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
###jwc n }

#
# Setup: Flask w/ SocketIO
#

#SETUP
#set up app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
###jwc y socketio = SocketIO(app)
###jwc y socketio = SocketIO(app, logger=True, engineio_logger=True)
###jwc y socketio = SocketIO(app, logger=True, engineio_logger=False)
###jwc y socketio = SocketIO(app, logger=False, engineio_logger=True)
###jwc y laggy w/ 'eventlet' socketio = SocketIO(app, logger=True, engineio_logger=False)
socketio = SocketIO(app, logger=False, engineio_logger=False)


###jwc 23-1128-0540 device busy bug: # jwc RpOs Bullseye
###jwc 23-1128-0540 device busy bug: #
###jwc 23-1128-0540 device busy bug: ###jwc o #camera setup
###jwc 23-1128-0540 device busy bug: ###jwc o camera = cv2.VideoCapture(0)
###jwc 23-1128-0540 device busy bug: ###jwc o time.sleep(1)
###jwc 23-1128-0540 device busy bug: ###jwc o camera.set(3, 64)
###jwc 23-1128-0540 device busy bug: ###jwc o camera.set(4, 64)
###jwc 23-1128-0540 device busy bug: 
###jwc 23-1128-0540 device busy bug: FPS = 10
###jwc 23-1128-0540 device busy bug: ###jwc o sentCamera = False
###jwc 23-1128-0540 device busy bug: 
###jwc 23-1128-0540 device busy bug: piCam = Picamera2()
###jwc 23-1128-0540 device busy bug: # for 30fps
###jwc 23-1128-0540 device busy bug: ###jwc o piCam.preview_configuration.size=(1280,720)
###jwc 23-1128-0540 device busy bug: ###jwc o 2fps: piCam.preview_configuration.main.size=(1280,720)
###jwc 23-1128-0540 device busy bug: ###jwc y 6-7fps: piCam.preview_configuration.main.size=(640,360)
###jwc 23-1128-0540 device busy bug: 
###jwc 23-1128-0540 device busy bug: # jwc y 26-27fps
###jwc 23-1128-0540 device busy bug: ###jwc yyy piCam.preview_configuration.main.size=(320,180)
###jwc 23-1128-0540 device busy bug: ###jwc ? slower: piCam.preview_configuration.main.size=(620,360)
###jwc 23-1128-0540 device busy bug: 
###jwc 23-1128-0540 device busy bug: ###jwc yyy 90fps, im:225150 : piCam.preview_configuration.main.size=(320,180)
###jwc 23-1128-0540 device busy bug: ###jwc yy little more glitchier/laggier: piCam.preview_configuration.main.size=(640,360)
###jwc 23-1128-0540 device busy bug: # jwc seems fine as dimensions grow
###jwc 23-1128-0540 device busy bug: piCam.preview_configuration.main.size=(1280,720)
###jwc 23-1128-0540 device busy bug: 
###jwc 23-1128-0540 device busy bug: ###jwc o piCam.preview_configuration.__format__="RGB888"
###jwc 23-1128-0540 device busy bug: piCam.preview_configuration.main.format="RGB888"
###jwc 23-1128-0540 device busy bug: #jwc seems to work noton UsbCam  C720 nor C922 but on CsiCam:Lanzo RpiClone
###jwc 23-1128-0540 device busy bug: ###jwc y but only 1-2 fps: piCam.preview_configuration.controls.FrameRate=30
###jwc 23-1128-0540 device busy bug: ###jwc y 22-24fps, try 90: piCam.preview_configuration.controls.FrameRate=60
###jwc 23-1128-0540 device busy bug: # jwc 23-0927-1200 TYJ fps rose to 25-28fps :)+, even with GUI, VsCode, SSH: 95tasks, 122threads :)+
###jwc 23-1128-0540 device busy bug: ###jwc 23-0928-1330 yy piCam.preview_configuration.controls.FrameRate=90
###jwc 23-1128-0540 device busy bug: ###jwc from 12 to 48fps: piCam.preview_configuration.controls.FrameRate=100
###jwc 23-1128-0540 device busy bug: ###jwc back to 15fps: piCam.preview_configuration.controls.FrameRate=120
###jwc 23-1128-0540 device busy bug: ###jwc back to 15fps: piCam.preview_configuration.controls.FrameRate=100
###jwc 23-1128-0540 device busy bug: ###jwc y piCam.preview_configuration.controls.FrameRate=99
###jwc 23-1128-0540 device busy bug: 
###jwc 23-1128-0540 device busy bug: ###jwc 23-0929-1050 20-30fps: piCam.preview_configuration.controls.FrameRate=60
###jwc 23-1128-0540 device busy bug: piCam.preview_configuration.controls.FrameRate=90
###jwc 23-1128-0540 device busy bug: piCam.preview_configuration.align()
###jwc 23-1128-0540 device busy bug: 
###jwc 23-1128-0540 device busy bug: framecount = 0
###jwc 23-1128-0540 device busy bug: prevMillis = 0
###jwc 23-1128-0540 device busy bug: def fpsCount():
###jwc 23-1128-0540 device busy bug:     global prevMillis
###jwc 23-1128-0540 device busy bug:     global framecount
###jwc 23-1128-0540 device busy bug:     millis = int(round(time.time() * 1000))
###jwc 23-1128-0540 device busy bug:     framecount += 1
###jwc 23-1128-0540 device busy bug:     if millis - prevMillis > 1000:
###jwc 23-1128-0540 device busy bug:         print(framecount)
###jwc 23-1128-0540 device busy bug:         prevMillis = millis 
###jwc 23-1128-0540 device busy bug:         framecount = 0
###jwc 23-1128-0540 device busy bug:         
###jwc 23-1128-0540 device busy bug: # verify that the supplied ArUCo tag exists and is supported by
###jwc 23-1128-0540 device busy bug: # OpenCV
###jwc 23-1128-0540 device busy bug: if ARUCO_DICT.get(args["type"], None) is None:
###jwc 23-1128-0540 device busy bug:     print("[INFO] ArUCo tag of '{}' is not supported".format(
###jwc 23-1128-0540 device busy bug:         args["type"]))
###jwc 23-1128-0540 device busy bug:     sys.exit(0)
###jwc 23-1128-0540 device busy bug: 
###jwc 23-1128-0540 device busy bug: # load the ArUCo dictionary and grab the ArUCo parameters
###jwc 23-1128-0540 device busy bug: print("[INFO] detecting '{}' tags...".format(args["type"]))
###jwc 23-1128-0540 device busy bug: ###jwc o,n arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
###jwc 23-1128-0540 device busy bug: ###jwc o,n arucoParams = cv2.aruco.DetectorParameters_create()
###jwc 23-1128-0540 device busy bug: 
###jwc 23-1128-0540 device busy bug: arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[args["type"]])
###jwc 23-1128-0540 device busy bug: arucoParams =  cv2.aruco.DetectorParameters()
###jwc 23-1128-0540 device busy bug: arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
###jwc 23-1128-0540 device busy bug: 
###jwc 23-1128-0540 device busy bug: piCam.configure("preview")
###jwc 23-1128-0540 device busy bug: piCam.start()


###jwc 23-1128-0550
###
framecount = 0
prevMillis = 0
def fpsCount():
    global prevMillis
    global framecount
    millis = int(round(time.time() * 1000))
    framecount += 1
    if millis - prevMillis > 1000:
        ###jwc y print(framecount)
        print("FPS:" + str(framecount))
        prevMillis = millis 
        framecount = 0


target_00_Score_Int = 0
target_01_Score_Int = 0
target_02_Score_Int = 0
target_03_Score_Int = 0

# jwc Provide time to stabilize
###jwc o time.sleep(2.0)
time.sleep(2.0)

#
# Quest IO_Extension_Boardt: Servos
#

###jwc o motor setup
###jwc o PIN_I2C6_POWER_ENABLE = 17
###jwc o bus = smbus.SMBus(1)
###jwc o DEVICE_ADDRESS = 0x53
###jwc o GPIO.setmode(GPIO.BCM)
###jwc o time.sleep(0.1) #important
###jwc o GPIO.setup(PIN_I2C6_POWER_ENABLE, GPIO.OUT)
###jwc o time.sleep(0.1) #important
###jwc o speed = 50

#
# SparkFun pHat: DcMotors w/ Encoders
#

import time
import sys
###jwc o import math
import qwiic_scmd

#jwc add encoder
import qwiic_dual_encoder_reader

myMotor = qwiic_scmd.QwiicScmd()

# Motor Setup
#
###jwc o print("Motor Test.")
R_MTR = 0
L_MTR = 1
FWD = 0
BWD = 1

#jwc was 100, try max 255
motor_Speed_INT = 255
#jwc was 0.05, try real_time: 0
motor_ContinueState_Sec_DECI = 0.0

if myMotor.connected == False:
    print("*** *** Motor Driver not connected. Check connections.", \
        file=sys.stderr)
    ###jwc o return
    sys.exit(0)

    
print("*** Motors Setup 1of3: Connected.")

myMotor.begin()
time.sleep(.250)
print("*** Motors Setup 2of3: Initialized.")

# Zero Motor Speeds
myMotor.set_drive(0,0,0)
myMotor.set_drive(1,0,0)
myMotor.enable()
time.sleep(.250)
print("*** Motors Setup 3of3: Enabled H-Bridge Circuit")

# Encoder Setup
#
###jwc o print("\nSparkFun Qwiic Dual Encoder Reader   Example 1\n")
myEncoders = qwiic_dual_encoder_reader.QwiicDualEncoderReader()
if myEncoders.connected == False:
    print("*** *** The Qwiic Dual Encoder Reader device isn't connected to the system. Please check your connection", \
        file=sys.stderr)
    ###jwc o return
    sys.exit(0)

print("*** Encoders Setup 1of3: Connected.")

myEncoders.begin()
print("*** Enocders Setup 2of3: Initialized.")

#jwc Print 'Limit/Max'.  
if myEncoders.limit == 0:
    print("    *** Limit:32767 ticks (Default)")
else:
    print("    *** Limit: %d ticks" % (myEncoders.limit))
#jwc Clear Counters of any residue values: Important since Counters seem to have persistent memory of last program ran
#
myEncoders.set_count1(0)
myEncoders.set_count2(0)
print("*** Enocders Setup 3of3: Show Encoder Limit -&- Clear Encoder Values.")

#
# SparkFun pHat: I2C Oled
#

import qwiic_micro_oled

#  These three lines of code are all you need to initialize the
#  OLED and print the splash screen.

#  Before you can start using the OLED, call begin() to init
#  all of the pins and configure the OLED.

print("\nSparkFun Micro OLED Hello Example\n")
myOLED = qwiic_micro_oled.QwiicMicroOled()

if not myOLED.connected:
    print("The Qwiic Micro OLED device isn't connected to the system. Please check your connection", \
        file=sys.stderr)
    ###jwc o return
    sys.exit(0)

myOLED.begin()
#  clear(ALL) will clear out the OLED's graphic memory.
#  clear(PAGE) will clear the Arduino's display buffer.
myOLED.clear(myOLED.ALL)  #  Clear the display's memory (gets rid of artifacts)
#  To actually draw anything on the display, you must call the
#  display() function.
myOLED.display()

time.sleep(2)

myOLED.clear(myOLED.PAGE)  #  Clear the display's buffer

myOLED.print("Hello All  : )")  #  Add "Hello World" to buffer

#  To actually draw anything on the display, you must call the display() function. 
myOLED.display()

#
# Main Functions
#

#debug
###jwc o prev_t_lidar = 0
prev_t_cam = 0


###jwc 24-0529-2230 Rp4>Rp5 y: #setup servo
###jwc 24-0529-2230 Rp4>Rp5 y: trueMsg = sc.msg(True)
###jwc 24-0529-2230 Rp4>Rp5 y: falseMsg = sc.msg(False)
###jwc 24-0529-2230 Rp4>Rp5 y: ARM_PIN = 5
###jwc 24-0529-2230 Rp4>Rp5 y: DIG_PIN = 14
###jwc 24-0529-2230 Rp4>Rp5 y: speed = 5
###jwc 24-0529-2230 Rp4>Rp5 y: sc.callback_servoPWR_enable(trueMsg)
###jwc 24-0529-2230 Rp4>Rp5 y: sc.callback_servo_enable(ARM_PIN, trueMsg)
###jwc 24-0529-2230 Rp4>Rp5 y: sc.callback_servo_enable(DIG_PIN, trueMsg)
###jwc 24-0529-2230 Rp4>Rp5 y: armAngle = 90
###jwc 24-0529-2230 Rp4>Rp5 y: sc.callback_servo_angle(ARM_PIN, sc.msg(armAngle))
###jwc 24-0529-2230 Rp4>Rp5 y: digAngle = 90
###jwc 24-0529-2230 Rp4>Rp5 y: sc.callback_servo_angle(DIG_PIN, sc.msg(digAngle))
###jwc 24-0529-2230 Rp4>Rp5 y: 
###jwc 24-0529-2230 Rp4>Rp5 y: def clamp(val):
###jwc 24-0529-2230 Rp4>Rp5 y:     if (val<0):
###jwc 24-0529-2230 Rp4>Rp5 y:         return 0
###jwc 24-0529-2230 Rp4>Rp5 y:     if (val>180):
###jwc 24-0529-2230 Rp4>Rp5 y:         return 180
###jwc 24-0529-2230 Rp4>Rp5 y:     return val

###jwc 24-0529-2230 Rp4>Rp5 y: #setup laser
###jwc 24-0529-2230 Rp4>Rp5 y: laser_pin = 24
###jwc 24-0529-2230 Rp4>Rp5 y: GPIO.setmode(GPIO.BCM)
###jwc 24-0529-2230 Rp4>Rp5 y: GPIO.setup(laser_pin, GPIO.OUT)
###jwc 24-0529-2230 Rp4>Rp5 y: GPIO.output(laser_pin, GPIO.LOW)
###jwc 24-0529-2230 Rp4>Rp5 y: laser_on = False


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
    
    ###jwc 23-1128-0550
    ### global prev_t_cam
    ###jwc ? global prev_t_cam, framecount
    global prev_t_cam
    

    # jwc RpOs Bullseye
    #
    ###jwc o #camera setup
    ###jwc o camera = cv2.VideoCapture(0)
    ###jwc o time.sleep(1)
    ###jwc o camera.set(3, 64)
    ###jwc o camera.set(4, 64)
    
    ###jwc 24-0516-1610 y hopefully increase fps: FPS = 10
    # was 10, 60fps >> 20-30fps, 120fps >> same rate, try 30
    # TYJ 30fps >> 15-20fps local & decent ~1-2 sec lag remote on android phone :)+
    ###jwc y? FPS = 30
    ###jwc y: FPS = 10
    #jwc 24-0517-1500, 30 crashes 'needCamera' though 9 to 19 fps, 20 to 14fps, 60 seems too fast
    ###jwc 24-0520 ? FPS = 30
    ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?: FPS = 90

    ###jwc o sentCamera = False
    
    piCam = Picamera2()
    # for 30fps
    ###jwc o piCam.preview_configuration.size=(1280,720)
    ###jwc o 2fps: piCam.preview_configuration.main.size=(1280,720)
    ###jwc y 6-7fps: piCam.preview_configuration.main.size=(640,360)
    
    # jwc y 26-27fps
    ###jwc yyy piCam.preview_configuration.main.size=(320,180)
    ###jwc ? slower: piCam.preview_configuration.main.size=(620,360)
    
    ###jwc yyy 90fps, im:225150 : piCam.preview_configuration.main.size=(320,180)
    ###jwc yy little more glitchier/laggier: piCam.preview_configuration.main.size=(640,360)
    # jwc seems fine as dimensions grow
    piCam.preview_configuration.main.size=(1280,720)
    
    ###jwc o piCam.preview_configuration.__format__="RGB888"
    piCam.preview_configuration.main.format="RGB888"
    #jwc seems to work noton UsbCam  C720 nor C922 but on CsiCam:Lanzo RpiClone
    ###jwc y but only 1-2 fps: piCam.preview_configuration.controls.FrameRate=30
    ###jwc y 22-24fps, try 90: piCam.preview_configuration.controls.FrameRate=60
    # jwc 23-0927-1200 TYJ fps rose to 25-28fps :)+, even with GUI, VsCode, SSH: 95tasks, 122threads :)+
    ###jwc 23-0928-1330 yy piCam.preview_configuration.controls.FrameRate=90
    ###jwc from 12 to 48fps: piCam.preview_configuration.controls.FrameRate=100
    ###jwc back to 15fps: piCam.preview_configuration.controls.FrameRate=120
    ###jwc back to 15fps: piCam.preview_configuration.controls.FrameRate=100
    ###jwc y piCam.preview_configuration.controls.FrameRate=99
    
    ###jwc 23-0929-1050 20-30fps: piCam.preview_configuration.controls.FrameRate=60
    
    ###jwc 24-0520 Aruco Freeze: ? piCam.preview_configuration.controls.FrameRate=90
    
    piCam.preview_configuration.align()
    
    ###jwc o framecount = 0
    ###jwc o prevMillis = 0
    ###jwc o def fpsCount():
    ###jwc o     global prevMillis
    ###jwc o     global framecount
    ###jwc o     millis = int(round(time.time() * 1000))
    ###jwc o     framecount += 1
    ###jwc o     if millis - prevMillis > 1000:
    ###jwc o         print(framecount)
    ###jwc o         prevMillis = millis 
    ###jwc o         framecount = 0
            
    # verify that the supplied ArUCo tag exists and is supported by
    # OpenCV
    if ARUCO_DICT.get(args["type"], None) is None:
        print("[INFO] ArUCo tag of '{}' is not supported".format(
            args["type"]))
        sys.exit(0)
    
    # load the ArUCo dictionary and grab the ArUCo parameters
    print("[INFO] detecting '{}' tags...".format(args["type"]))
    ###jwc o,n arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
    ###jwc o,n arucoParams = cv2.aruco.DetectorParameters_create()
    
    arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT[args["type"]])
    arucoParams =  cv2.aruco.DetectorParameters()
    arucoDetector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
    
    piCam.configure("preview")
   
    piCam.start()
    print("* piCam.start()")

    print("sending cam data now")
    while True:
        ###jwc o retval, frame = camera.read()
        
        
        # jwc RpOs Bullseye
        frame = piCam.capture_array()

        ###jwc y 2-3fps CsiCam Lanzo seems good (better vs. CsiPiCam2): frame = imutils.resize(frame, width=1000)
        ###jwc y 7-8 fps: frame = imutils.resize(frame, width=500)
        ###jwc y 17-18fps frame = imutils.resize(frame, width=250)
        ###jwc y 33-35fps frame = imutils.resize(frame, width=125)
        ###jwc yy 15-16fps seems just right
        ###jwc yy same fps for CsiCam_Lanzo_PiCamClone
        ###jwc yy frame = imutils.resize(frame, width=320)
        ###jwc yyy 19-20fps with 'height' added and now h,w in sync w/ above 'VideoStream' :)+
        #jwc 'VideoStream: h,w' should be in sync w/ 'imutils.resize: h,w' :)+
        ###jwc y: frame = imutils.resize(frame, height=320, width=240)
        ###jwc y frame = imutils.resize(frame, height=160, width=120)
        ###jwc videostream 80,60  30fps seems but shows 6-8fps
        ###jwc frame = imutils.resize(frame, height=1600, width=1200)
        ###jwc yy frame = imutils.resize(frame, height=800, width=600)
        ###jwc y frame = imutils.resize(frame, height=1200, width=900)
        ###jwc y frame = imutils.resize(frame, height=1000, width=750)
        ###jwc y frame = imutils.resize(frame, height=800, width=600)
        ###jwc yy frame = imutils.resize(frame, height=400, width=300)
        ###jwc 1-2 sec lag: frame = imutils.resize(frame, height=750, width=500)
        
        ###jwc 23-0928-2300 wow 8-10 fps: frame = imutils.resize(frame, height=600, width=400)
        ###jwc y 15-25fps: frame = imutils.resize(frame, height=300, width=200)
        ###jwc y 20-25fps: frame = imutils.resize(frame, height=450, width=300)
        
        # jwc imx219
        #
        ###jwc yy jumped from 20-25fps to 48fps >> since > 30fps very real-time but small screen :)+
        ###jwc y 35fps: frame = imutils.resize(frame, height=225, width=150)

        # jwc imx708 non-wide
        #
        ###jwc y now w/ imx708 non_wide: 35fps: frame = imutils.resize(frame, height=225, width=150)
        ###jwc y 28fps: frame = imutils.resize(frame, height=450, width=300)
        ###jwc y 29 fps: frame = imutils.reszie(frame, height=400, width=300)
        ###jwc y 25 fps: frame = imutils.resize(frame, height=375, width=300)
        ###jwc y 33fps :)+
        ###jwc yy frame = imutils.resize(frame, height=350, width=250)
        ###jwc y more laggy: frame = imutils.resize(frame, height=800, width=600)
        frame = imutils.resize(frame, height=350, width=250)
      
       
        # detect ArUco markers in the input frame
        ###jwc o (corners, ids, rejected) = cv2.aruco.detectMarkers(frame, arucoDict, parameters=arucoParams)
        (corners, ids, rejected) = arucoDetector.detectMarkers(frame)

        # verify *at least* one ArUco marker was detected
        if len(corners) > 0:
            # flatten the ArUco IDs list
            ids = ids.flatten()
            
            # loop over the detected ArUCo corners
            for (markerCorner, markerID) in zip(corners, ids):
                # extract the marker corners (which are always returned
                # in top-left, top-right, bottom-right, and bottom-left
                # order)
                corners = markerCorner.reshape((4, 2))
                (topLeft, topRight, bottomRight, bottomLeft) = corners
                
                # convert each of the (x, y)-coordinate pairs to integers
                topRight = (int(topRight[0]), int(topRight[1]))
                bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
                bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
                topLeft = (int(topLeft[0]), int(topLeft[1]))
                
                pixelSpacing_Int = 10

                topRight_2 = (int(topRight[0])+pixelSpacing_Int, int(topRight[1])-pixelSpacing_Int)
                ###jwc y convert to shrinking tower: topRight_2 = (int(topRight[0])-pixelSpacing_Int, int(topRight[1])+pixelSpacing_Int)
                bottomRight_2 = (int(bottomRight[0])+pixelSpacing_Int, int(bottomRight[1])-pixelSpacing_Int)
                ###jwc y convert to shrinking tower: bottomRight_2 = (int(bottomRight[0])-pixelSpacing_Int, int(bottomRight[1])-pixelSpacing_Int)
                bottomLeft_2 = (int(bottomLeft[0])+pixelSpacing_Int, int(bottomLeft[1])-pixelSpacing_Int)
                ###jwc y convert to shrinking tower: bottomLeft_2 = (int(bottomLeft[0])+pixelSpacing_Int, int(bottomLeft[1])-pixelSpacing_Int)
                topLeft_2 = (int(topLeft[0])+pixelSpacing_Int, int(topLeft[1]-pixelSpacing_Int))
                ###jwc y convert to shrinking tower: topLeft_2 = (int(topLeft[0])+pixelSpacing_Int, int(topLeft[1]+pixelSpacing_Int))


                ###jwc 24-0605-1601 y: # draw the bounding 3d-cube of the ArUCo detection
                ###jwc 24-0605-1601 y: #
                ###jwc 24-0605-1601 y: color_Blue_Int = 255
                ###jwc 24-0605-1601 y: color_Green_Int = 255
                ###jwc 24-0605-1601 y: color_Red_Int = 255
                ###jwc 24-0605-1601 y: #
                ###jwc 24-0605-1601 y: 
                ###jwc 24-0605-1601 y: # draw the bounding box of the ArUCo detection
                ###jwc 24-0605-1601 y: cv2.line(frame, topLeft, topRight, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1601 y: cv2.line(frame, topRight, bottomRight, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1601 y: cv2.line(frame, bottomRight, bottomLeft, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1601 y: cv2.line(frame, bottomLeft, topLeft, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1601 y:        
                ###jwc 24-0605-1601 y: cv2.line(frame, topLeft_2, topRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1601 y: cv2.line(frame, topRight_2, bottomRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1601 y: cv2.line(frame, bottomRight_2, bottomLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1601 y: cv2.line(frame, bottomLeft_2, topLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1601 y: 
                ###jwc 24-0605-1601 y: cv2.line(frame, topLeft, topLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1601 y: cv2.line(frame, topRight, topRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1601 y: cv2.line(frame, bottomRight, bottomRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1601 y: cv2.line(frame, bottomLeft, bottomLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)


                ###jwc y cv2.rectangle(frame, topLeft, bottomRight, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                
                
                ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?: 
                ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?: # compute and draw the center (x, y)-coordinates of the
                ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?: # ArUco marker
                ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?: cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?: cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?: cv2.circle(frame, (cX, cY), 4, (color_Blue_Int, 0, 255), -1)
                ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?: 
                ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?: # draw the ArUco marker ID on the frame
                ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?: cv2.putText(frame, str(markerID),
                ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?:     (topLeft[0], topLeft[1] - 15),
                ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?:     cv2.FONT_HERSHEY_SIMPLEX,
                ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?:     0.5, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?: 
                ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?: # jwc 3, 2, 1
                ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?: # seconds
                ###jwc 24-0520-1250 causing 'needCamera' error, too laggy here?: timeDuration_Sec_Int = 1
                
                ###jwc 24-0520-1300 'needCamera' error:if markerID == 0:                
                ###jwc 24-0520-1300 'needCamera' error:    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=120
                ###jwc 24-0520-1300 'needCamera' error:    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=120
                ###jwc 24-0520-1300 'needCamera' error:    ###jwc y laggy: print("*** MarkerID: "+ str(markerID))
                ###jwc 24-0520-1300 'needCamera' error:    ###jwc o sleep(timeDuration_Sec_Int)
                ###jwc 24-0520-1300 'needCamera' error:    
                ###jwc 24-0520-1300 'needCamera' error:    ###jwc n crashes cam: stop_motors()
                ###jwc 24-0520-1300 'needCamera' error:     
                ###jwc 24-0520-1300 'needCamera' error:    ###jwc y time.sleep(timeDuration_Sec_Int)
                ###jwc 24-0520-1300 'needCamera' error:    
                ###jwc 24-0520-1300 'needCamera' error:    ###jwc print("*** MarkerID: "+ str(markerID))
                ###jwc 24-0520-1300 'needCamera' error:    
                ###jwc 24-0520-1300 'needCamera' error:    target_00_Score_Int = 0
                ###jwc 24-0520-1300 'needCamera' error:    target_01_Score_Int = 0
                ###jwc 24-0520-1300 'needCamera' error:    target_02_Score_Int = 0
                ###jwc 24-0520-1300 'needCamera' error:    target_03_Score_Int = 0
                ###jwc 24-0520-1300 'needCamera' error:    
                ###jwc 24-0520-1300 'needCamera' error:    print("!!!!!!!!!!!!!! Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int) + " !!!!!!!!!!!!!!")
                ###jwc 24-0520-1300 'needCamera' error:    print("!!!!!!!!!!!!!! Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int) + " !!!!!!!!!!!!!!")
                ###jwc 24-0520-1300 'needCamera' error:    print("!!!!!!!!!!!!!! Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int) + " !!!!!!!!!!!!!!")
                ###jwc 24-0520-1300 'needCamera' error:    print("!!!!!!!!!!!!!! Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int) + " !!!!!!!!!!!!!!")
                ###jwc 24-0520-1300 'needCamera' error:    print("!!!!!!!!!!!!!! Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int) + " !!!!!!!!!!!!!!")
                ###jwc 24-0520-1300 'needCamera' error:
                ###jwc 24-0520-1300 'needCamera' error:    ###jwc not needed 24-0520-1230: time.sleep(timeDuration_Sec_Int)
                ###jwc 24-0520-1300 'needCamera' error:
                ###jwc 24-0520-1300 'needCamera' error: if markerID == 1:                
                ###jwc 24-0520-1300 'needCamera' error:     ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=60
                ###jwc 24-0520-1300 'needCamera' error:     ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=60
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=70
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=70
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc y laggy: print("*** MarkerID: "+ str(markerID))
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc o sleep(timeDuration_Sec_Int)
                ###jwc 24-0520-1300 'needCamera' error:     
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: servoId_Left = 0
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: servoAngle_Left = 135
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: 
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: sc.callback_servo_enable(int(servoId_Left), trueMsg)
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: 
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: angle_Left = sc.msg(int(servoAngle_Left))
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: sc.callback_servo_angle(int(servoId_Left),angle_Left)
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: 
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: print("motion_Left", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: return ('id_L: ' + str(servoId_Left) + ' angle_L: ' + str(servoAngle_Left) + '|' + 'id_R: ' + str(servoId_Right) + ' angle_R: ' + str(servoAngle_Right))
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: 
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: time.sleep(timeDuration_Sec_Int)
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: 
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: stop_motors()
                ###jwc 24-0520-1300 'needCamera' error:     
                ###jwc 24-0520-1300 'needCamera' error:     target_01_Score_Int += 1
                ###jwc 24-0520-1300 'needCamera' error:     
                ###jwc 24-0520-1300 'needCamera' error:     print("*** Contact: MarkerID: "+ str(markerID))
                ###jwc 24-0520-1300 'needCamera' error:     
                ###jwc 24-0520-1300 'needCamera' error:     print("               Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int))
                ###jwc 24-0520-1300 'needCamera' error: 
                ###jwc 24-0520-1300 'needCamera' error: if markerID == 2:                
                ###jwc 24-0520-1300 'needCamera' error:     ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=120
                ###jwc 24-0520-1300 'needCamera' error:     ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=60
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=120
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=70
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc y laggy: print("*** MarkerID: "+ str(markerID))
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc o sleep(timeDuration_Sec_Int)
                ###jwc 24-0520-1300 'needCamera' error: 
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: servoId_Right = 1
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: servoAngle_Right = 45
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: 
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: sc.callback_servo_enable(int(servoId_Right), trueMsg)
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: 
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: angle_Right = sc.msg(int(servoAngle_Right))
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: sc.callback_servo_angle(int(servoId_Right),angle_Right)
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: 
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: print("motion_Right", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: return ('id_L: ' + str(servoId_Left) + ' angle_L: ' + str(servoAngle_Left) + '|' + 'id_R: ' + str(servoId_Right) + ' angle_R: ' + str(servoAngle_Right))
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: 
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: time.sleep(timeDuration_Sec_Int)
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: 
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: stop_motors()
                ###jwc 24-0520-1300 'needCamera' error:     
                ###jwc 24-0520-1300 'needCamera' error:     target_02_Score_Int += 1
                ###jwc 24-0520-1300 'needCamera' error:     
                ###jwc 24-0520-1300 'needCamera' error:     print("*** *** Contact: MarkerID: "+ str(markerID))
                ###jwc 24-0520-1300 'needCamera' error:     
                ###jwc 24-0520-1300 'needCamera' error:     print("               Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int))
                ###jwc 24-0520-1300 'needCamera' error: 
                ###jwc 24-0520-1300 'needCamera' error: if markerID == 3:                
                ###jwc 24-0520-1300 'needCamera' error:     ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=60
                ###jwc 24-0520-1300 'needCamera' error:     ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=120
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=80
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=120
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc y laggy: print("*** MarkerID: "+ str(markerID))
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc o sleep(timeDuration_Sec_Int)
                ###jwc 24-0520-1300 'needCamera' error:     
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: forward()
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: 
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: time.sleep(timeDuration_Sec_Int)
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: 
                ###jwc 24-0520-1300 'needCamera' error:     ###jwc n crashes cam: stop_motors()
                ###jwc 24-0520-1300 'needCamera' error: 
                ###jwc 24-0520-1300 'needCamera' error:     target_03_Score_Int += 1
                ###jwc 24-0520-1300 'needCamera' error:     
                ###jwc 24-0520-1300 'needCamera' error:     print("*** *** *** Contact: MarkerID: "+ str(markerID))
                ###jwc 24-0520-1300 'needCamera' error:     
                ###jwc 24-0520-1300 'needCamera' error:     print("               Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int))
                
                
                ###jwc y print("*** Contact: MarkerID: "+ str(markerID))

                if markerID == 0:                
                    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=120
                    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=120
                    ###jwc y laggy: print("*** MarkerID: "+ str(markerID))
                    ###jwc o sleep(timeDuration_Sec_Int)
                    
                    ###jwc n crashes cam: stop_motors()
                     
                    ###jwc y time.sleep(timeDuration_Sec_Int)
                    
                    ###jwc print("*** MarkerID: "+ str(markerID))
                    
                    target_00_Score_Int = 0
                    target_01_Score_Int = 0
                    target_02_Score_Int = 0
                    target_03_Score_Int = 0
                    
                    # draw the bounding 3d-cube of the ArUCo detection
                    #
                    color_Blue_Int = 0
                    color_Green_Int = 255
                    color_Red_Int = 255
                    #
                    cv2.line(frame, topLeft, topRight, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, topRight, bottomRight, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomRight, bottomLeft, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomLeft, topLeft, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    #
                    cv2.line(frame, topLeft_2, topRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, topRight_2, bottomRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomRight_2, bottomLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomLeft_2, topLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    #
                    cv2.line(frame, topLeft, topLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, topRight, topRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomRight, bottomRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomLeft, bottomLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    
                    ###jwc to reduce print_lag: print("!!!!!!!!!!!!!! Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int) + " !!!!!!!!!!!!!!")
                    ###jwc to reduce print_lag: print("!!!!!!!!!!!!!! Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int) + " !!!!!!!!!!!!!!")
                    ###jwc to reduce print_lag: print("!!!!!!!!!!!!!! Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int) + " !!!!!!!!!!!!!!")
                    ###jwc to reduce print_lag: print("!!!!!!!!!!!!!! Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int) + " !!!!!!!!!!!!!!")
                    ###jwc y print("!!!!!!!!!! Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int) + " !!!!!!!!!!")
                    ###jwc y print("             Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int))

                    print("!!! !!! Contact: MarkerID: "+ str(markerID) + " | Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int))
                    
                    ###jwc not needed 24-0520-1230: time.sleep(timeDuration_Sec_Int)
                
                if markerID == 1:                
                    ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=60
                    ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=60
                    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=70
                    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=70
                    ###jwc y laggy: print("*** MarkerID: "+ str(markerID))
                    ###jwc o sleep(timeDuration_Sec_Int)
                    
                    ###jwc n crashes cam: servoId_Left = 0
                    ###jwc n crashes cam: servoAngle_Left = 135
                    ###jwc n crashes cam: 
                    ###jwc n crashes cam: sc.callback_servo_enable(int(servoId_Left), trueMsg)
                    ###jwc n crashes cam: 
                    ###jwc n crashes cam: angle_Left = sc.msg(int(servoAngle_Left))
                    ###jwc n crashes cam: sc.callback_servo_angle(int(servoId_Left),angle_Left)
                    ###jwc n crashes cam: 
                    ###jwc n crashes cam: print("motion_Left", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)
                    ###jwc n crashes cam: return ('id_L: ' + str(servoId_Left) + ' angle_L: ' + str(servoAngle_Left) + '|' + 'id_R: ' + str(servoId_Right) + ' angle_R: ' + str(servoAngle_Right))
                    ###jwc n crashes cam: 
                    ###jwc n crashes cam: time.sleep(timeDuration_Sec_Int)
                    ###jwc n crashes cam: 
                    ###jwc n crashes cam: stop_motors()
                    
                    target_01_Score_Int += 1
                    
                    # draw the bounding 3d-cube of the ArUCo detection
                    #
                    color_Blue_Int = 0
                    color_Green_Int = 255
                    color_Red_Int = 0
                    #                    
                    cv2.line(frame, topLeft, topRight, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, topRight, bottomRight, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomRight, bottomLeft, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomLeft, topLeft, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    #    
                    cv2.line(frame, topLeft_2, topRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, topRight_2, bottomRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomRight_2, bottomLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomLeft_2, topLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    #
                    cv2.line(frame, topLeft, topLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, topRight, topRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomRight, bottomRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomLeft, bottomLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)

                    ###jwc y print("             Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int))
                    print("*** *** Contact: MarkerID: "+ str(markerID) + " | Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int))
                
                if markerID == 2:                
                    ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=120
                    ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=60
                    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=120
                    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=70
                    ###jwc y laggy: print("*** MarkerID: "+ str(markerID))
                    ###jwc o sleep(timeDuration_Sec_Int)
                
                    ###jwc n crashes cam: servoId_Right = 1
                    ###jwc n crashes cam: servoAngle_Right = 45
                    ###jwc n crashes cam: 
                    ###jwc n crashes cam: sc.callback_servo_enable(int(servoId_Right), trueMsg)
                    ###jwc n crashes cam: 
                    ###jwc n crashes cam: angle_Right = sc.msg(int(servoAngle_Right))
                    ###jwc n crashes cam: sc.callback_servo_angle(int(servoId_Right),angle_Right)
                    ###jwc n crashes cam: 
                    ###jwc n crashes cam: print("motion_Right", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)
                    ###jwc n crashes cam: return ('id_L: ' + str(servoId_Left) + ' angle_L: ' + str(servoAngle_Left) + '|' + 'id_R: ' + str(servoId_Right) + ' angle_R: ' + str(servoAngle_Right))
                    ###jwc n crashes cam: 
                    ###jwc n crashes cam: time.sleep(timeDuration_Sec_Int)
                    ###jwc n crashes cam: 
                    ###jwc n crashes cam: stop_motors()
                    
                    target_02_Score_Int += 1
                    
                    # draw the bounding 3d-cube of the ArUCo detection
                    #
                    color_Blue_Int = 255
                    color_Green_Int = 0
                    color_Red_Int = 0
                    #
                    cv2.line(frame, topLeft, topRight, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, topRight, bottomRight, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomRight, bottomLeft, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomLeft, topLeft, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    #    
                    cv2.line(frame, topLeft_2, topRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, topRight_2, bottomRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomRight_2, bottomLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomLeft_2, topLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    #
                    cv2.line(frame, topLeft, topLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, topRight, topRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomRight, bottomRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    cv2.line(frame, bottomLeft, bottomLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                    ###jwc 24-0605-1
                    ###jwc y print("             Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int))
                    print("*** *** Contact: MarkerID: "+ str(markerID) + " | Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int))
                
                ###jwc 24-0605-1620 'needCamera' error: if markerID == 3:                
                ###jwc 24-0605-1620 'needCamera' error:     ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=60
                ###jwc 24-0605-1620 'needCamera' error:     ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=120
                ###jwc 24-0605-1620 'needCamera' error:     ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=80
                ###jwc 24-0605-1620 'needCamera' error:     ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=120
                ###jwc 24-0605-1620 'needCamera' error:     ###jwc y laggy: print("*** MarkerID: "+ str(markerID))
                ###jwc 24-0605-1620 'needCamera' error:     ###jwc o sleep(timeDuration_Sec_Int)
                ###jwc 24-0605-1620 'needCamera' error:     
                ###jwc 24-0605-1620 'needCamera' error:     ###jwc n crashes cam: forward()
                ###jwc 24-0605-1620 'needCamera' error:     ###jwc n crashes cam: 
                ###jwc 24-0605-1620 'needCamera' error:     ###jwc n crashes cam: time.sleep(timeDuration_Sec_Int)
                ###jwc 24-0605-1620 'needCamera' error:     ###jwc n crashes cam: 
                ###jwc 24-0605-1620 'needCamera' error:     ###jwc n crashes cam: stop_motors()
                ###jwc 24-0605-1620 'needCamera' error: 
                ###jwc 24-0605-1620 'needCamera' error:     target_03_Score_Int += 1
                ###jwc 24-0605-1620 'needCamera' error:     
                ###jwc 24-0605-1620 'needCamera' error:     # draw the bounding 3d-cube of the ArUCo detection
                ###jwc 24-0605-1620 'needCamera' error:     #
                ###jwc 24-0605-1620 'needCamera' error:     color_Blue_Int = 0
                ###jwc 24-0605-1620 'needCamera' error:     color_Green_Int = 0
                ###jwc 24-0605-1620 'needCamera' error:     color_Red_Int = 255
                ###jwc 24-0605-1620 'needCamera' error:     #
                ###jwc 24-0605-1620 'needCamera' error:     cv2.line(frame, topLeft, topRight, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1620 'needCamera' error:     cv2.line(frame, topRight, bottomRight, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1620 'needCamera' error:     cv2.line(frame, bottomRight, bottomLeft, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1620 'needCamera' error:     cv2.line(frame, bottomLeft, topLeft, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1620 'needCamera' error:     #    
                ###jwc 24-0605-1620 'needCamera' error:     cv2.line(frame, topLeft_2, topRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1620 'needCamera' error:     cv2.line(frame, topRight_2, bottomRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1620 'needCamera' error:     cv2.line(frame, bottomRight_2, bottomLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1620 'needCamera' error:     cv2.line(frame, bottomLeft_2, topLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1620 'needCamera' error:     #
                ###jwc 24-0605-1620 'needCamera' error:     cv2.line(frame, topLeft, topLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1620 'needCamera' error:     cv2.line(frame, topRight, topRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1620 'needCamera' error:     cv2.line(frame, bottomRight, bottomRight_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1620 'needCamera' error:     cv2.line(frame, bottomLeft, bottomLeft_2, (color_Blue_Int, color_Green_Int, color_Red_Int), 2)
                ###jwc 24-0605-1620 'needCamera' error:     
                ###jwc 24-0605-1620 'needCamera' error:     ###jwc y print("             Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int))
                ###jwc 24-0605-1620 'needCamera' error:     print("*** *** Contact: MarkerID: "+ str(markerID) + " | Score" + " 1: " + str(target_01_Score_Int) + " 2: " + str(target_02_Score_Int) + " 3: " + str(target_03_Score_Int))

                    
                ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=90
                ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=90

        ###jwc o #my camera is placed upside down ._.
        ###jwc o #to get the correct image, we must flip the camera vertically and horizontally
        ###jwc o frame = cv2.flip(frame, -1)
        
        retval, jpg = cv2.imencode('.jpg', frame)
        jpg_as_text = str(base64.b64encode(jpg))
        jpg_as_text = jpg_as_text[2:-1]
        emit('jpg_string', jpg_as_text)
        ###jwc y print("sent a picture. time: " + str(time.time()-prev_t_cam))
        prev_t_cam = time.time()
        ###jwc 24-0520-1300 'needCamera' error: REACHING 50+ FPS, BUT NO VIDEO SEEN, BUT DID CATCH ARUCO MARERKID: socketio.sleep(1/FPS)
        ###jwc y 45fps: socketio.sleep(0.001)
        ###jwc y 35fps: socketio.sleep(0.01)
        ###jwc y 15fps: socketio.sleep(0.05)
        ###jwc y 0.02s = 50fps?
        ###jwc yy: Rp5 try no sleep? : socketio.sleep(0.02)
        ###jwc Rp5: no sleep >> server 43fps but client cannot connect43fps
        ###jwc Rp5 0.001 >> 43fps | 0.005 >> 41 fps | 0.01 >> 35fps/18fps | 0.05 >> 17fps
        ###jwc Rp5 : 0.01 >> hopefully 100fps?, after reboot: sever 55fps / client 55fps but much 'needCamera' fatal error frequent, resort to 0.02s >> 36fps server, 30fps client | 0.04 >> 20fps server, 20 client
        ###jwc ? socketio.sleep(0.02)
        ###jwc ? socketio.sleep(0.04)
        ###jwc ? CAUSE NO VIDEO_STREAM:  socketio.sleep(0.02)
        ###jwc n video but 'need camera': 
        ###jwc yy TYJ 0.1s works but 10fps server, 9fps client | 0.01s 50fps server, 50fps client
        ###jwc yy socketio.sleep(0.1)
        
        ###jwc n socketio.sleep(0.01)
        ###jwc n socketio.sleep(0.05)
        ###jwc y 24-0605-1621 remove and see (w/o 3) NO SCREEN: socketio.sleep(0.1)
        ###jwc n no sleep: no camera and 99fps
        ###jwc n need video but camera: socketio.sleep(0.01) 55fps  (no sleep: 99fps)
        ###jwc n need video but camera: socketio.sleep(0.05) 17fps
        socketio.sleep(0.1)

    
        ###jwc y caused significant lag: cv2.imshow("piCam", frame)
                
        fpsCount()        
            
        if cv2.waitKey(1)==ord('q'):
            break
        
    cv2.destroyAllWindows()



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

@socketio.on('digDown')
def digDown():
    global digAngle
    digAngle = clamp(digAngle - speed)
    s = sc.msg(digAngle)
    sc.callback_servo_angle(DIG_PIN, s)
    print("dig:", digAngle)

@socketio.on('digUp')
def digUp():
    global digAngle
    digAngle = clamp(digAngle + speed)
    s = sc.msg(digAngle)
    sc.callback_servo_angle(DIG_PIN, s)
    print("dig:", digAngle)

###jwc y @socketio.on('armDown')
###jwc y def armDown():
###jwc y     ###jwc o global armAngle
###jwc y     ###jwc o armAngle = clamp(armAngle - speed)
###jwc y     ###jwc o s = sc.msg(armAngle)
###jwc y     ###jwc o sc.callback_servo_angle(ARM_PIN, s)
###jwc y     ###jwc o print("arm", armAngle)
###jwc y 
###jwc y     servoId_Left = 0
###jwc y     servoAngle_Left = 90
###jwc y     
###jwc y     sc.callback_servo_enable(int(servoId_Left), trueMsg)
###jwc y     
###jwc y     angle = sc.msg(int(servoAngle_Left))
###jwc y     sc.callback_servo_angle(int(servoId_Left),angle)
###jwc y     ###jwc o print("arm", servoId_Left, armAngle)
###jwc y     print("arm_Down", servoId_Left, servoAngle_Left)
###jwc y     
###jwc y     ###jwc o return ('id: ' + servoId_Left + ' angle: ' + servoAngle_Left)
###jwc y     return ('id: ' + str(servoId_Left) + ' angle: ' + str(servoAngle_Left))
###jwc y 
###jwc y     ###jwc o def move_servo(servoId_Left, servoAngle_Left):
###jwc y     ###jwc o 	sc.callback_servo_enable(int(servoId_Left), trueMsg)
###jwc y     ###jwc o 	angle = sc.msg(int(servoAngle_Left))
###jwc y     ###jwc o 	sc.callback_servo_angle(int(servoId_Left),angle)
###jwc y     ###jwc o 	return ('id: ' + servoId_Left + ' angle: ' + servoAngle_Left)

###jwc o @socketio.on('turnLeft')
###jwc o def turn_left():
###jwc o     ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(speed))
###jwc o     ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(-1 * speed))
###jwc o     print("turn left received")

@socketio.on('turnLeft')
def turn_Left():
    ###jwc yy ###jwc o global armAngle
    ###jwc yy ###jwc o armAngle = clamp(armAngle - speed)
    ###jwc yy ###jwc o s = sc.msg(armAngle)
    ###jwc yy ###jwc o sc.callback_servo_angle(ARM_PIN, s)
    ###jwc yy ###jwc o print("arm", armAngle)
    ###jwc yy 
    ###jwc yy ###jwc o servoId_Left = 0
    ###jwc yy ###jwc o servoAngle_Left = 45
    ###jwc yy ###jwc o 
    ###jwc yy ###jwc o servoId_Right = 1
    ###jwc yy ###jwc o servoAngle_Right = 45
    ###jwc yy ###jwc o 
    ###jwc yy ###jwc o sc.callback_servo_enable(int(servoId_Left), trueMsg)
    ###jwc yy ###jwc o sc.callback_servo_enable(int(servoId_Right), trueMsg)
    ###jwc yy ###jwc o 
    ###jwc yy ###jwc o angle_Left = sc.msg(int(servoAngle_Left))
    ###jwc yy ###jwc o angle_Right = sc.msg(int(servoAngle_Right))
    ###jwc yy ###jwc o 
    ###jwc yy ###jwc o sc.callback_servo_angle(int(servoId_Left),angle_Left)
    ###jwc yy ###jwc o sc.callback_servo_angle(int(servoId_Right),angle_Right)
    ###jwc yy 
    ###jwc yy ###jwc o print("arm", servoId, armAngle)
    ###jwc yy ###jwc n print("turn_Left", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)
    ###jwc yy ###jwc y print("turn_Left", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)
    ###jwc yy ###jwc yy print("motion_Left", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)
    ###jwc yy ###jwc y print("turn_Left_03")
    ###jwc yy 
    ###jwc yy ###jwc o return ('id: ' + servoId_Left + ' angle: ' + servoAngle_Left)
    ###jwc yy ###jwc yy return ('id_L: ' + str(servoId_Left) + ' angle_L: ' + str(servoAngle_Left) + '|' + 'id_R: ' + str(servoId_Right) + ' angle_R: ' + str(servoAngle_Right))
    ###jwc yy 
    ###jwc yy ###jwc o def move_servo(servoId_Left, servoAngle_Left):
    ###jwc yy ###jwc o 	sc.callback_servo_enable(int(servoId_Left), trueMsg)
    ###jwc yy ###jwc o 	angle = sc.msg(int(servoAngle_Left))
    ###jwc yy ###jwc o 	sc.callback_servo_angle(int(servoId_Left),angle)
    ###jwc yy ###jwc o 	return ('id: ' + servoId_Left + ' angle: ' + servoAngle_Left)

    myMotor.set_drive(L_MTR,FWD,0)
    myMotor.set_drive(R_MTR,FWD,motor_Speed_INT)

    ###jwc withhold from encoder example: # Delay in Seconds: 0.3sec = 300msec
    ###jwc withhold from encoder example: time.sleep(.3)
    
    # Delay in Seconds: 0.05sec = 50msec 
    ###jwc y time.sleep(.05)
    time.sleep(motor_ContinueState_Sec_DECI)

    print  ("* Turn Left: Speed: %d || Count1: %d | Count2: %d" % (motor_Speed_INT, myEncoders.count1, myEncoders.count2))
    return ("* Turn Left")

    
###jwc ported from o: @socketio.on('armUp')
###jwc ported from o: def armUp():
###jwc ported from o:     ###jwc o global armAngle
###jwc ported from o:     ###jwc o armAngle = clamp(armAngle + speed)
###jwc ported from o:     ###jwc o s = sc.msg(armAngle)
###jwc ported from o:     ###jwc o sc.callback_servo_angle(ARM_PIN, s)
###jwc ported from o:     ###jwc o print("arm", armAngle)
###jwc ported from o: 
###jwc ported from o:     servoId_Left = 0
###jwc ported from o:     servoAngle_Left = 0
###jwc ported from o: 
###jwc ported from o:     sc.callback_servo_enable(int(servoId_Left), trueMsg)
###jwc ported from o:     
###jwc ported from o:     angle = sc.msg(int(servoAngle_Left))
###jwc ported from o:     sc.callback_servo_angle(int(servoId_Left),angle)
###jwc ported from o:     ###jwc o print("arm", servoId_Left, armAngle)
###jwc ported from o:     print("arm_Up", servoId_Left, servoAngle_Left)
###jwc ported from o:     
###jwc ported from o:     ###jwc o return ('id: ' + servoId_Left + ' angle: ' + servoAngle_Left)
###jwc ported from o:     return ('id: ' + str(servoId_Left) + ' angle: ' + str(servoAngle_Left))
###jwc ported from o: 
###jwc ported from o:     ###jwc o def move_servo(servoId_Left, servoAngle_Left):
###jwc ported from o:     ###jwc o 	sc.callback_servo_enable(int(servoId_Left), trueMsg)
###jwc ported from o:     ###jwc o 	angle = sc.msg(int(servoAngle_Left))
###jwc ported from o:     ###jwc o 	sc.callback_servo_angle(int(servoId_Left),angle)
###jwc ported from o:     ###jwc o 	return ('id: ' + servoId_Left + ' angle: ' + servoAngle_Left)

###jwc o @socketio.on('turnRight')
###jwc o def turn_right():
###jwc o     ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(-1 * speed))
###jwc o     ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(speed))
###jwc o     print("turn right received")

@socketio.on('turnRight')
def turn_Right():
    ###jwc yy ###jwc o global armAngle
    ###jwc yy ###jwc o armAngle = clamp(armAngle + speed)
    ###jwc yy ###jwc o s = sc.msg(armAngle)
    ###jwc yy ###jwc o sc.callback_servo_angle(ARM_PIN, s)
    ###jwc yy ###jwc o print("arm", armAngle)
    ###jwc yy 
    ###jwc yy ###jwc y servoId_Left = 0
    ###jwc yy ###jwc y servoAngle_Left = 135
    ###jwc yy ###jwc y 
    ###jwc yy ###jwc y servoId_Right = 1
    ###jwc yy ###jwc y servoAngle_Right = 135
    ###jwc yy ###jwc y 
    ###jwc yy ###jwc y sc.callback_servo_enable(int(servoId_Left), trueMsg)
    ###jwc yy ###jwc y sc.callback_servo_enable(int(servoId_Right), trueMsg)
    ###jwc yy ###jwc y 
    ###jwc yy ###jwc y angle_Left = sc.msg(int(servoAngle_Left))
    ###jwc yy ###jwc y angle_Right = sc.msg(int(servoAngle_Right))
    ###jwc yy ###jwc y 
    ###jwc yy ###jwc y sc.callback_servo_angle(int(servoId_Left),angle_Left)
    ###jwc yy ###jwc y sc.callback_servo_angle(int(servoId_Right),angle_Right)
    ###jwc yy 
    ###jwc yy ###jwc o print("arm", servoId, armAngle)
    ###jwc yy ###jwc n print("turn_Left", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)
    ###jwc yy ###jwc y print("turn_Right", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)
    ###jwc yy ###jwc yy print("motion_Right", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)
    ###jwc yy 
    ###jwc yy ###jwc y print("turn_Left_03")
    ###jwc yy 
    ###jwc yy ###jwc o return ('id: ' + servoId_Left + ' angle: ' + servoAngle_Left)
    ###jwc yy ###jwc yy return ('id_L: ' + str(servoId_Left) + ' angle_L: ' + str(servoAngle_Left) + '|' + 'id_R: ' + str(servoId_Right) + ' angle_R: ' + str(servoAngle_Right))
    ###jwc yy 
    ###jwc yy ###jwc o def move_servo(servoId_Left, servoAngle_Left):
    ###jwc yy ###jwc o 	sc.callback_servo_enable(int(servoId_Left), trueMsg)
    ###jwc yy ###jwc o 	angle = sc.msg(int(servoAngle_Left))
    ###jwc yy ###jwc o 	sc.callback_servo_angle(int(servoId_Left),angle)
    ###jwc yy ###jwc o 	return ('id: ' + servoId_Left + ' angle: ' + servoAngle_Left)
   
    myMotor.set_drive(L_MTR,FWD,motor_Speed_INT)
    myMotor.set_drive(R_MTR,FWD,0)

    ###jwc withhold from encoder example: # Delay in Seconds: 0.3sec = 300msec
    ###jwc withhold from encoder example: time.sleep(.3)
    
    # Delay in Seconds: 0.05sec = 50msec 
    ###jwc y time.sleep(.05)
    time.sleep(motor_ContinueState_Sec_DECI)

    print  ("* Turn Right: Speed: %d || Count1: %d | Count2: %d" % (motor_Speed_INT, myEncoders.count1, myEncoders.count2))
    return ("* Turn Right")


@socketio.on('motorsOn')
def motors_on():
    ###jwc o GPIO.output(PIN_I2C6_POWER_ENABLE, GPIO.HIGH)
    print("motor on received")
@socketio.on('motorsOff')
def motors_off():
    ###jwc o GPIO.output(PIN_I2C6_POWER_ENABLE, GPIO.LOW)
    print("motor off received")


@socketio.on('forward')
def forward():
    ###jwc yy ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(speed))
    ###jwc yy ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(speed))
    ###jwc yy ###jwc o print("forward received")
    ###jwc yy 
    ###jwc yy servoId_Left = 0
    ###jwc yy servoAngle_Left = 135
    ###jwc yy 
    ###jwc yy servoId_Right = 1
    ###jwc yy servoAngle_Right = 45
    ###jwc yy 
    ###jwc yy sc.callback_servo_enable(int(servoId_Left), trueMsg)
    ###jwc yy sc.callback_servo_enable(int(servoId_Right), trueMsg)
    ###jwc yy 
    ###jwc yy angle_Left = sc.msg(int(servoAngle_Left))
    ###jwc yy angle_Right = sc.msg(int(servoAngle_Right))
    ###jwc yy 
    ###jwc yy sc.callback_servo_angle(int(servoId_Left),angle_Left)
    ###jwc yy sc.callback_servo_angle(int(servoId_Right),angle_Right)
    ###jwc yy 
    ###jwc yy ###jwc o print("arm", servoId, armAngle)
    ###jwc yy ###jwc n print("turn_Left", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)
    ###jwc yy ###jwc y print("turn_Right", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)
    ###jwc yy print("motion_Forward", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)
    ###jwc yy ###jwc y print("turn_Left_03")
    ###jwc yy 
    ###jwc yy ###jwc o return ('id: ' + servoId_Left + ' angle: ' + servoAngle_Left)
    ###jwc yy return ('id_L: ' + str(servoId_Left) + ' angle_L: ' + str(servoAngle_Left) + '|' + 'id_R: ' + str(servoId_Right) + ' angle_R: ' + str(servoAngle_Right))
    
    myMotor.set_drive(L_MTR,FWD,motor_Speed_INT)
    myMotor.set_drive(R_MTR,FWD,motor_Speed_INT)

    ###jwc withhold from encoder example: # Delay in Seconds: 0.3sec = 300msec
    ###jwc withhold from encoder example: time.sleep(.3)
    
    # Delay in Seconds: 0.05sec = 50msec 
    ###jwc y time.sleep(.05)
    time.sleep(motor_ContinueState_Sec_DECI)

    print  ("* Forward: Speed: %d || Count1: %d | Count2: %d" % (motor_Speed_INT, myEncoders.count1, myEncoders.count2))
    return ("* Forward")


@socketio.on('backward')
def backward():
    ###jwc yy ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(-1 * speed))
    ###jwc yy ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(-1 * speed))
    ###jwc yy ###jwc o print("backward received")
    ###jwc yy 
    ###jwc yy servoId_Left = 0
    ###jwc yy servoAngle_Left = 45
    ###jwc yy 
    ###jwc yy servoId_Right = 1
    ###jwc yy servoAngle_Right = 135    
    ###jwc yy 
    ###jwc yy sc.callback_servo_enable(int(servoId_Left), trueMsg)
    ###jwc yy sc.callback_servo_enable(int(servoId_Right), trueMsg)
    ###jwc yy 
    ###jwc yy angle_Left = sc.msg(int(servoAngle_Left))
    ###jwc yy angle_Right = sc.msg(int(servoAngle_Right))
    ###jwc yy 
    ###jwc yy sc.callback_servo_angle(int(servoId_Left),angle_Left)
    ###jwc yy sc.callback_servo_angle(int(servoId_Right),angle_Right)
    ###jwc yy 
    ###jwc yy ###jwc o print("arm", servoId, armAngle)
    ###jwc yy ###jwc n print("turn_Left", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)
    ###jwc yy ###jwc y print("turn_Right", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)
    ###jwc yy print("motion_Backward", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)
    ###jwc yy ###jwc y print("turn_Left_03")
    ###jwc yy 
    ###jwc yy ###jwc o return ('id: ' + servoId_Left + ' angle: ' + servoAngle_Left)
    ###jwc yy return ('id_L: ' + str(servoId_Left) + ' angle_L: ' + str(servoAngle_Left) + '|' + 'id_R: ' + str(servoId_Right) + ' angle_R: ' + str(servoAngle_Right))

    myMotor.set_drive(L_MTR,FWD,-motor_Speed_INT)
    myMotor.set_drive(R_MTR,FWD,-motor_Speed_INT)

    ###jwc withhold from encoder example: # Delay in Seconds: 0.3sec = 300msec
    ###jwc withhold from encoder example: time.sleep(.3)
    
    # Delay in Seconds: 0.05sec = 50msec 
    ###jwc y time.sleep(.05)
    time.sleep(motor_ContinueState_Sec_DECI)

    print  ("* Backward: Speed: %d || Count1: %d | Count2: %d" % (motor_Speed_INT, myEncoders.count1, myEncoders.count2))
    return ("* Backward")

@socketio.on('stopMotors')
def stop_motors():
    ###jwc yy ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(0))
    ###jwc yy ###jwc o bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(0))
    ###jwc yy 
    ###jwc yy servoId_Left = 0
    ###jwc yy servoAngle_Left = 90
    ###jwc yy sc.callback_servo_enable(int(servoId_Left), trueMsg)
    ###jwc yy angle_Left = sc.msg(int(servoAngle_Left))
    ###jwc yy sc.callback_servo_angle(int(servoId_Left),angle_Left)
    ###jwc yy 
    ###jwc yy 
    ###jwc yy servoId_Right = 1
    ###jwc yy servoAngle_Right = 90
    ###jwc yy sc.callback_servo_enable(int(servoId_Right), trueMsg)
    ###jwc yy angle_Right = sc.msg(int(servoAngle_Right))
    ###jwc yy sc.callback_servo_angle(int(servoId_Right),angle_Right)
    ###jwc yy 
    ###jwc yy ###jwc y print("stop motors received")
    ###jwc yy print("motion_stop", servoId_Left, servoAngle_Left,"|",servoId_Right, servoAngle_Right)

    myMotor.set_drive(L_MTR,FWD,0)
    myMotor.set_drive(R_MTR,FWD,0)

    ###jwc withhold from encoder example: # Delay in Seconds: 0.3sec = 300msec
    ###jwc withhold from encoder example: time.sleep(.3)
    
    # Delay in Seconds: 0.05sec = 50msec 
    ###jwc y time.sleep(.05)
    time.sleep(motor_ContinueState_Sec_DECI)

    print  ("* Stop: Speed: %d || Count1: %d | Count2: %d" % (motor_Speed_INT, myEncoders.count1, myEncoders.count2))
    return ("* Stop")

@socketio.on('setSpeed')
def set_speed(data):
    global speed
    speed = int(data)
    print("Speed:", speed)


@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"]) # "my error event"
    print(request.event["args"])    # (data,)


#FLASK SERVING
#serve the webpage when a client connects to IP:5000
@app.route('/')
def home():
    return render_template('index.html')


#RUN THE APP
if __name__ == '__main__':
    print("ready for clients: Port = 5000")
    ###jwc o socketio.run(app, host='0.0.0.0', port=5000)
    
    ###jwc y socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    
    ###jwc n serve( app, host='0.0.0.0', port=5000, url_scheme='https', threads=100 )
        
    ###jwc n socketio = SocketIO(app, cors_allowed_origins="*") 
    ###jwc n socketio = SocketIO(app, cors_allowed_origins=['http://127.0.0.1:5500'])     

    ###jwc y socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    ###jwc   socketio.run(app, host='10.78.25.75', port=5000, debug=True)
    ###jwc y socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    ###jwc y socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)


#PROGRAM CLEAN UP
GPIO.cleanup()

myMotor.disable()
###jwc y         sys.exit(0)

###jwc o lidar.stop()
###jwc o lidar.disconnect()
