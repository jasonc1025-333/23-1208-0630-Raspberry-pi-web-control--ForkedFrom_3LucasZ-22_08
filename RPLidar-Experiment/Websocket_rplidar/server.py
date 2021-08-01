#IMPORTS
from flask import Flask, request, render_template
from flask_socketio import SocketIO
import os
from math import floor
from adafruit_rplidar import RPLidar

#SETUP
#set up app
app = Flask(__name__)
socketio = SocketIO(app)

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)


#LISTENERS
@socketio.on('connect')
def connect():
    print('A client connected.')


@socketio.on('disconnect')
def disconnect():
    print('A client disconnected.')


@socketio.on('needLidar')
def send_lidar():
    try:
        #get the most recent scan
        for scan in lidar.iter_measurements(): 
            #scan has 4 properties: new_scan, quality, angle, distance
            print(scan[2]) 
            print(scan[3])
    except KeyboardInterrupt:
        print('Stopping.')
    lidar.stop()
    lidar.disconnect()


#FLASK SERVING
@app.route('/')
def home():
    return render_template('index.html')


#RUN APP
if __name__ == '__main__':
    print("ready for clients!")
    socketio.run(app, host='0.0.0.0', port=5000)