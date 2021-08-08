import smbus2 as smbus
import RPi.GPIO as GPIO
import time
import int_to_byte

PIN_I2C6_POWER_ENABLE = 17

bus = smbus.SMBus(6)
DEVICE_ADDRESS = 0x53

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_I2C6_POWER_ENABLE, GPIO.OUT)
time.sleep(0.1)
GPIO.output(PIN_I2C6_POWER_ENABLE, GPIO.HIGH)
time.sleep(0.1)

bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(30))
bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(30))
time.sleep(3)
bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(0))
bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(0))