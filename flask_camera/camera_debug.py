from picamera import PiCamera
import time
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def home():
    camera = PiCamera()
    camera.resolution = (300, 300)
    camera.start_preview()
    time.sleep(2)
    return 'hello'


def capture():
    camera.capture('static/picture.jpg')


if __name__ == "__main__":
    #will run on: http://192.168.1.162:8080/
    app.run(host='0.0.0.0', port=8080, debug=True)
