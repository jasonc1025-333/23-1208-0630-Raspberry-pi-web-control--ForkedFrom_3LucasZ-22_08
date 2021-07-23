#! /usr/bin/env python
from flask import Flask, render_template, request
import int_to_byte
import smbus
import math
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
motorsEnabled = False
PIN_I2C6_POWER_ENABLE = 17
bus = smbus.SMBus(3)
DEVICE_ADDRESS = 0x53
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_I2C6_POWER_ENABLE, GPIO.OUT)
time.sleep(0.1) #important


@app.route("/", methods=["GET","POST"])
def home():
    global motorsEnabled
    if request.method == "POST":
        motorsEnabled = not motorsEnabled
    if motorsEnabled:
        GPIO.output(PIN_I2C6_POWER_ENABLE, GPIO.HIGH)
    else:
        GPIO.output(PIN_I2C6_POWER_ENABLE, GPIO.LOW)
  
    return render_template('index.html', motorsEnabled=motorsEnabled)


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
   