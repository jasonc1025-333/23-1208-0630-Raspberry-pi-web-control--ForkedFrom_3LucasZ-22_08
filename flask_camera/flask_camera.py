import os
from flask import Flask, render_template, request
import time
from picamera import PiCamera

app = Flask(__name__)
camera = PiCamera()
camera.resolution = (200, 200)
camera.start_preview()
time.sleep(2)

# prevent Google Chrome Caching
uniqueID = '0'


def newPicture():
    global uniqueID
    uniqueID = str(time.time())
    filename = uniqueID + '.jpg'
    camera.capture(filename)


@app.route("/", methods=["GET","POST"])
def home():
    newPicture()
    filename = uniqueID + '.jpg'
    image = '../static/' + filename
    return render_template('camera_index.html', image=image)


if __name__ == "__main__":
    #will run on: http://192.168.1.162:8080/
    for filename in os.listdir('static/'):
        os.remove('static/' + filename)
    app.run(host='0.0.0.0', port=8080, debug=True)
    
        