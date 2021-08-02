#IMPORTS
from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
import time

#SETUP
#set up app
app = Flask(__name__)
socketio = SocketIO(app)

#LISTENERS
@socketio.on('connect')
def connect():
    print('A client connected.')


@socketio.on('disconnect')
def disconnect():
    print('A client disconnected.')

array = [0]*360
@socketio.on('server')
def send_continuous():
    while True:
        ms = int(1000 * time.time())
        emit('ms', ms)
        socketio.sleep(0)


#FLASK SERVING
@app.route('/')
def home():
    return render_template('client.html')


#RUN APP
if __name__ == '__main__':
    print("ready for clients!")
    socketio.run(app, host='0.0.0.0', port=5000)