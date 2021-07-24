from flask import Flask, render_template
from flask_socketio import SocketIO
import int_to_byte
import smbus
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
socketio = SocketIO(app)

PIN_I2C6_POWER_ENABLE = 17
bus = smbus.SMBus(3)
DEVICE_ADDRESS = 0x53
GPIO.setmode(GPIO.BCM)
time.sleep(0.1) #important
GPIO.setup(PIN_I2C6_POWER_ENABLE, GPIO.OUT)
time.sleep(0.1) #important


@app.route("/")
def home():
    return render_template('client.html')


@socketio.on('connect')
def connect():
    print('A client connected.')

@socketio.on('disconnect')
def disconnect():
    print('A client disconnected.')

@socketio.on('message')
def handle_message(data):
    if (data) == 'motorOn':
        print("motor on received")
        GPIO.output(PIN_I2C6_POWER_ENABLE, GPIO.HIGH)
    elif (data) == 'motorOff':
        print("motor off received")
        GPIO.output(PIN_I2C6_POWER_ENABLE, GPIO.LOW)
    elif (data) == 'left':
        print("turn left received")
        bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(50))
        bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(-50))
        time.sleep(0.1)
    elif (data) == 'right':
        print("turn right received")
        bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(-50))
        bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(50))
        time.sleep(0.1)
    elif (data) == 'forward':
        print("go forward received")
        bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(50))
        bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(50))
        time.sleep(0.1)
    elif (data) == 'backward':
        print("go backward received")
        bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(-50))
        bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(-50))
        time.sleep(0.1)

    bus.write_i2c_block_data(DEVICE_ADDRESS,3,int_to_byte.int_to_byte_array(0))
    bus.write_i2c_block_data(DEVICE_ADDRESS,4,int_to_byte.int_to_byte_array(0))


if __name__ == '__main__':
    socketio.run(app)