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

@socketio.on('message')
def handle_message(data):
    if (data) == 'motorOn':
        print("motor on received")
    elif (data) == 'motorOff':
        print("motor off received")
    elif (data) == 'left':
        print("turn left received")
    elif (data) == 'right':
        print("turn right received")
    elif (data) == 'forward':
        print("go forward received")
    elif (data) == 'backward':
        print("go backward received")
    else:
        print("Speed:",int(data))


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port='8080')