#! /usr/bin/env python
import smbus
import math
import RPi.GPIO as GPIO
import time
from textwrap import wrap

PIN_I2C6_POWER_ENABLE = 17

bus = smbus.SMBus(3)      #this is I2C6 on the pi4 for some reason
DEVICE_ADDRESS = 0x53


def int_to_byte_array(num):
   if num < 0:
      hexStr = hex((1<<32) + num)
   else:
      hexStr = hex(num)
   hexStr = hexStr.rstrip("L")      #sometimes the hex conversion adds a 'L' to the end. Remove it

   padded = str.format('{:08X}',int(hexStr,16))   #pad out to 8 hex characters
   padded = wrap(padded,2)                     #split into pairs of hex chars ie bytes

   array = [0,0,0,0]
   for x in range(4):
      array[x] = int(padded[x],16)

   array.reverse()      #reverse the list. We will send LSB first
   return array

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_I2C6_POWER_ENABLE, GPIO.OUT)
GPIO.output(PIN_I2C6_POWER_ENABLE, GPIO.HIGH)
time.sleep(0.1)
bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte_array(10))
bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte_array(10))
time.sleep(3)
GPIO.cleanup()

