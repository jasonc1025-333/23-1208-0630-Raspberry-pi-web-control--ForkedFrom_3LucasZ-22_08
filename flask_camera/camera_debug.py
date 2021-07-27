from flask import Flask, render_template
import time
from picamera import PiCamera


app = Flask(__name__)


@app.route("/")
def home():
    return "HELLO WORLD"


if __name__ == "__main__":
    #will run on: http://192.168.1.162:8080/
    app.run(host='0.0.0.0', port=8080, debug=True)

    try:
        camera = PiCamera()
        camera.resolution = (300, 300)
    finally:
        print("Done")
