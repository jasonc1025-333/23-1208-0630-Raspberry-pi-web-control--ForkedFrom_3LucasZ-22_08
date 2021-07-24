from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (300, 300)
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture('static/picture.jpg')