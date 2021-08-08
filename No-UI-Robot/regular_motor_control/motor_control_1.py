import smbus2 as smbus
import time
bus = smbus.SMBus(1)
DEVICE_ADDRESS = 0x53
bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(2))
time.sleep(1)
bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(0))