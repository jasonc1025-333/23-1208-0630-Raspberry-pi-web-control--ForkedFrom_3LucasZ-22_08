import smbus2 as smbus
import time
bus = smbus.SMBus(1)
DEVICE_ADDRESS = 0x53
for i in range(0, 10):
    bus.write_i2c_block_data(DEVICE_ADDRESS,4,[1,1,0,0,0,0,0,0])
    time.sleep(1)
    bus.write_i2c_block_data(DEVICE_ADDRESS,4,[0,0,0,0,0,0,0,0])