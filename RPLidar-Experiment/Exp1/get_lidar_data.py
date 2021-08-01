import os
from math import floor
from adafruit_rplidar import RPLidar


# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)

# used to scale data to fit on the screen
max_distance = 0

def process_data(data):
    print(data)

scan_data = [0]*360

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