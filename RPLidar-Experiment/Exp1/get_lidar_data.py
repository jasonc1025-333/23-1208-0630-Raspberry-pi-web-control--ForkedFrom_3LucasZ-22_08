from math import floor
from adafruit_rplidar import RPLidar

# Setup RPLidar
PORT_NAME='/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)

max_distance = 0

scan_data = [0]*360

try: 
    print(lidar.info)
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[floor(angle)] = distance
        print(scan_data)

except KeyboardInterrupt:
    print('Stopping.')

lidar.stop()
lidar.disconnect()