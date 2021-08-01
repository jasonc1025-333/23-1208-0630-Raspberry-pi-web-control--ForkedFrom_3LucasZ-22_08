import os
from math import floor
from adafruit_rplidar import RPLidar


# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME, timeout=3)

try:
    #get the most recent scan with infinite scan generator
    for scan in lidar.iter_measurements(5): 
        #scan has 4 properties: new_scan, quality, angle, distance
        print(scan[2]) 
        print(scan[3])

except KeyboardInterrupt:
    print('Stopping.')

lidar.stop()
lidar.disconnect()