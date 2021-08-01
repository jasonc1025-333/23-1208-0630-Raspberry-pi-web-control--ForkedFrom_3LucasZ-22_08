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
sentLidar = False

#LISTENERS
@socketio.on('connect')
def connect():
    print('A client connected.')


@socketio.on('disconnect')
def disconnect():
    print('A client disconnected.')

#360 element array of distances
scan_data = [0]*360
@socketio.on('needLidar')
def send_lidar():
    global sentLidar
    if sentLidar == False:
        sentLidar = True
        try:
            while True:
                #get the most recent scans from scan generator
                for scan in lidar.iter_scans(5): 
                    #scan has array of points
                    #each point has 3 properties: quality, angle, distance
                    for (_, angle, distance) in scan:
                        #ensure accessing index in range
                        scan_data[min([359, floor(angle)])] = distance
                    #send all clients scan_data array
                    #print(scan_data)
                    socketio.emit("scanData", scan_data)
                    socketio.sleep(0)
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