import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, GPIO.LOW)
time.sleep(0.1)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, GPIO.LOW)
time.sleep(0.1)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, GPIO.LOW)
time.sleep(0.1)
GPIO.cleanup()