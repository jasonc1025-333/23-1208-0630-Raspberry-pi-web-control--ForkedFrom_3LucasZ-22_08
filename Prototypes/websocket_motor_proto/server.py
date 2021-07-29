from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


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
    print("motor on received")

@socketio.on('motorsOff')
def motors_off():
    print("motor off received")

@socketio.on('turnLeft')
def turn_left():
    print("turn left received")

@socketio.on('turnRight')
def turn_right():
    print("turn right received")

@socketio.on('forward')
def forward():
    print("forward received")

@socketio.on('backward')
def backward():
    print("backward received")

@socketio.on('setSpeed')
def set_speed(speed):
    print("Speed:", int(speed))


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')