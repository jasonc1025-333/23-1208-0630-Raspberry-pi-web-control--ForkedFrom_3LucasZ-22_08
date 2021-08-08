import smbus2 as smbus
import int_to_byte

bus = smbus.SMBus(6)
DEVICE_ADDRESS = 0x53

print(smbus.i2c_msg.read(DEVICE_ADDRESS, 64))