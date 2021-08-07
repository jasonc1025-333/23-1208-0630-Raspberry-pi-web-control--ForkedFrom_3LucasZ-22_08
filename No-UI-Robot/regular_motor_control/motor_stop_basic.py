#! /usr/bin/env python
import smbus2 as smbus
import math
import RPi.GPIO as GPIO
import time
from textwrap import wrap

PIN_I2C6_POWER_ENABLE = 17

bus = smbus.SMBus(3)      #this is I2C6 on the pi4 for some reason
DEVICE_ADDRESS = 0x53

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_I2C6_POWER_ENABLE, GPIO.OUT)
GPIO.output(PIN_I2C6_POWER_ENABLE, GPIO.LOW)
time.sleep(0.1)
GPIO.cleanup()