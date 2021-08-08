import smbus2 as smbus
import time
bus = smbus.SMBus(6)
DEVICE_ADDRESS = 0x53

bus.write_i2c_block_data(DEVICE_ADDRESS,3,[1,1,0,0,0,0,0,0])
bus.write_i2c_block_data(DEVICE_ADDRESS,4,[1,1,0,0,0,0,0,0])
time.sleep(1)
bus.write_i2c_block_data(DEVICE_ADDRESS,3,[0,0,0,0,0,0,0,0])
bus.write_i2c_block_data(DEVICE_ADDRESS,4,[0,0,0,0,0,0,0,0])
for i in range(10):
    print(bus.read_i2c_block_data(DEVICE_ADDRESS,i,8))
