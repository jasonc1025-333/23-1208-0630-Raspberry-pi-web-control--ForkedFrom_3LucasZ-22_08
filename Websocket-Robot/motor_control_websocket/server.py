#library imports
from flask import Flask, render_template
from flask_socketio import SocketIO
import Modules.motor_controller as motors


#app setup
app = Flask(__name__)
socketio = SocketIO(app)


#motor setup
motorController = motors.MotorController()
speed = 1


#serve controls page
@app.route("/")
def home():
    return render_template('client.html')


@socketio.on('connect')
def connect():
    print('A client connected.')

@socketio.on('disconnect')
def disconnect():
    print('A client disconnected.')


@socketio.on('motorsOn')
def motors_on():
    motorController.on()
    print("motor on received")


@socketio.on('motorsOff')
def motors_off():
    motorController.off()
    print("motor off received")


@socketio.on('turnLeft')
def turn_left():
    motorController.set_to(speed, -1 * speed)
    print("turn left received")


@socketio.on('turnRight')
def turn_right():
    motorController.set_to(-1 * speed, speed)
    print("turn right received")


@socketio.on('forward')
def forward():
    motorController.set_to(speed, speed)
    print("forward received")

@socketio.on('backward')
def backward():
    motorController.set_to(-1 * speed, -1 * speed)
    print("backward received")


@socketio.on('stopMotors')
def stop_motors():
    motorController.set_to(0, 0)
    print("stopp motors received")


@socketio.on('setSpeed')
def set_speed(data):
    global speed
    speed = int(data)
    print("Speed:", speed)


if __name__ == '__main__':
    print("Ready for clients!")
    print("Running on: <Server IP Address>:5000")
    socketio.run(app, host='0.0.0.0', port='5000')