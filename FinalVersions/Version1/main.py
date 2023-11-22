#IMPORTS
#websocket and flask
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit, send


#video stream
import cv2
import base64



# jwc RpOs Bullseye
#
from picamera2 import Picamera2

# jwc Aruco
# Aruco Markers
import imutils
import argparse
import sys



#motor control
import RPi.GPIO as GPIO
import smbus2 as smbus
###jwc o from Modules.utils import int_to_byte_array
###jwc o from time import sleep
import time


###jwc o #rplidar
###jwc o import os
###jwc o from math import floor
###jwc o from adafruit_rplidar import RPLidar


#other
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



#SETUP
#set up app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)



# jwc RpOs Bullseye
#
###jwc o #camera setup
###jwc o camera = cv2.VideoCapture(0)
###jwc o time.sleep(1)
###jwc o camera.set(3, 64)
###jwc o camera.set(4, 64)

FPS = 10
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
piCam.preview_configuration.controls.FrameRate=90
piCam.preview_configuration.align()


framecount = 0
prevMillis = 0
def fpsCount():
    global prevMillis
    global framecount
    millis = int(round(time.time() * 1000))
    framecount += 1
    if millis - prevMillis > 1000:
        print(framecount)
        prevMillis = millis 
        framecount = 0
        

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

# jwc Provide time to stabilize
###jwc o time.sleep(2.0)
time.sleep(2.0)


###jwc o motor setup
###jwc o IN_I2C6_POWER_ENABLE = 17
###jwc o us = smbus.SMBus(1)
###jwc o EVICE_ADDRESS = 0x53
###jwc o PIO.setmode(GPIO.BCM)
###jwc o ime.sleep(0.1) #important
###jwc o PIO.setup(PIN_I2C6_POWER_ENABLE, GPIO.OUT)
###jwc o ime.sleep(0.1) #important
###jwc o peed = 50

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
    
                # draw the bounding box of the ArUCo detection
                cv2.line(frame, topLeft, topRight, (0, 255, 0), 2)
                cv2.line(frame, topRight, bottomRight, (0, 255, 0), 2)
                cv2.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
                cv2.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

                # compute and draw the center (x, y)-coordinates of the
                # ArUco marker
                cX = int((topLeft[0] + bottomRight[0]) / 2.0)
                cY = int((topLeft[1] + bottomRight[1]) / 2.0)
                cv2.circle(frame, (cX, cY), 4, (0, 0, 255), -1)

                # draw the ArUco marker ID on the frame
                cv2.putText(frame, str(markerID),
                    (topLeft[0], topLeft[1] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
                
                # jwc 3, 2, 1
                timeDuration = 1
                
                if markerID == 0:                
                    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=120
                    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=120
                    print("*** MarkerID: "+ str(markerID))
                    ###jwc o sleep(timeDuration)
                    time.sleep(timeDuration)
                if markerID == 1:                
                    ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=60
                    ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=60
                    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=70
                    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=70
                    print("*** MarkerID: "+ str(markerID))
                    ###jwc o sleep(timeDuration)
                    time.sleep(timeDuration)
                if markerID == 2:                
                    ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=120
                    ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=60
                    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=120
                    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=70
                    print("*** MarkerID: "+ str(markerID))
                    ###jwc o sleep(timeDuration)
                    time.sleep(timeDuration)
                if markerID == 3:                
                    ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=60
                    ###servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=120
                    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=80
                    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=120
                    print("*** MarkerID: "+ str(markerID))
                    ###jwc o sleep(timeDuration)
                    time.sleep(timeDuration)
                if markerID == 4:                
                    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=90
                    ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=90
                    print("*** MarkerID: "+ str(markerID))
                    ###jwc o sleep(timeDuration)
                    time.sleep(timeDuration)


                ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorLeft].angle=90
                ###jwc o servoKit_Object.servo[servoKit_Pca9685_Pin_MotorRight].angle=90

        ###jwc o #my camera is placed upside down ._.
        ###jwc o #to get the correct image, we must flip the camera vertically and horizontally
        ###jwc o frame = cv2.flip(frame, -1)
        
        retval, jpg = cv2.imencode('.jpg', frame)
        jpg_as_text = str(base64.b64encode(jpg))
        jpg_as_text = jpg_as_text[2:-1]
        emit('jpg_string', jpg_as_text)
        print("sent a picture. time: " + str(time.time()-prev_t_cam))
        prev_t_cam = time.time()
        socketio.sleep(1/FPS)
        
    
        cv2.imshow("piCam", frame)
                
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


@socketio.on('motorsOn')
def motors_on():
    ###jwc o GPIO.output(PIN_I2C6_POWER_ENABLE, GPIO.HIGH)
    print("motor on received")


@socketio.on('motorsOff')
def motors_off():
    ###jwc o GPIO.output(PIN_I2C6_POWER_ENABLE, GPIO.LOW)
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