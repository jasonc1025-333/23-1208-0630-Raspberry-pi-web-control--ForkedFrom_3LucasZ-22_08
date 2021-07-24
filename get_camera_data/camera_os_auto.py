import os
from flask import Flask, render_template, request

app = Flask(__name__)
picNum = 0


def newPicture():
    global picNum
    picNum += 1
    cmd = 'raspistill -o static/picture' + str(picNum) + '.jpg'
    os.system(cmd)


@app.route("/", methods=["GET","POST"])
def home():
    newPicture()
    image = 'static/picture' + str(picNum) + '.jpg'
    return "<img src=image>"


if __name__ == "__main__":
    #will run on: http://192.168.1.162:8080/
    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
    except KeyboardInterrupt:
        for filename in os.listdir('static/'):
            os.remove('static/' + filename)