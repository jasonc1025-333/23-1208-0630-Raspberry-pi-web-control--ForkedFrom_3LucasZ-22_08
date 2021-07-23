from picamera import PiCamera
from time import sleep
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    newPicture()
    return "<img src='static/picture.jpg'>"

camera = PiCamera()
def newPicture():
    camera.start_preview()
    sleep(2)
    camera.capture('/static/picture.jpg')
    camera.stop_preview()

if __name__ == "__main__":
    #will run on: http://192.168.1.162:8080/
    app.run(host='0.0.0.0', port=8080, debug=True)