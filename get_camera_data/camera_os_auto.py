import os
from flask import Flask, render_template, request
import time

app = Flask(__name__)
uniqueID = '0'


def newPicture():
    global uniqueID
    uniqueID = str(time.time())
    cmd = 'raspistill -o static/picture' + uniqueID + '.jpg'
    os.system(cmd)


@app.route("/", methods=["GET","POST"])
def home():
    newPicture()
    image = '../static/picture' + uniqueID + '.jpg'
    return render_template('camera_index.html', image=image)


if __name__ == "__main__":
    #will run on: http://192.168.1.162:8080/
    for filename in os.listdir('static/'):
        os.remove('static/' + filename)
    app.run(host='0.0.0.0', port=8080, debug=True)
    
        