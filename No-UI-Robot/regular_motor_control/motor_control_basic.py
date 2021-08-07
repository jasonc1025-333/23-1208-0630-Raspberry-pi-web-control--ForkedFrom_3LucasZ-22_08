import smbus2 as smbus
import math
import RPi.GPIO as GPIO
import time
from textwrap import wrap
import int_to_byte

PIN_I2C6_POWER_ENABLE = 17

bus = smbus.SMBus(1)      #this is I2C6 on the pi4 for some reason
DEVICE_ADDRESS = 0x50

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_I2C6_POWER_ENABLE, GPIO.OUT)
time.sleep(0.1) #EXTREMELY important
GPIO.output(PIN_I2C6_POWER_ENABLE, GPIO.HIGH)
time.sleep(0.1) #EXTREMELY important
bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(30))
bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(30))
time.sleep(1)
bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(0))
bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(0))
time.sleep(1)
GPIO.output(PIN_I2C6_POWER_ENABLE, GPIO.LOW)
time.sleep(1)
GPIO.cleanup()

