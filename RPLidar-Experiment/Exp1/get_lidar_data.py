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
#    print(lidar.get_info())
    for scan in lidar.iter_measurements():
        print(scan[0])
        print(scan[1])

except KeyboardInterrupt:
    print('Stopping.')
lidar.stop()
lidar.disconnect()