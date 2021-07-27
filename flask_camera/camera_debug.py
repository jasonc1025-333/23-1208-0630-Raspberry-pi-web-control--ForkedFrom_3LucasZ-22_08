from flask import Flask, render_template
import time
from picamera import PiCamera


app = Flask(__name__)


@app.route("/")
def home():
    capture()
    return '<img src=static/picture.jpg>'


def capture():
    camera.capture('static/picture.jpg')


if __name__ == "__main__":
    #will run on: http://192.168.1.162:8080/
    app.run(host='0.0.0.0', port=8080, debug=True)

    
    global camera = PiCamera()
    camera.resolution = (300, 300)
    camera.start_preview()
    sleep(2)
    print('Ready for clients')
