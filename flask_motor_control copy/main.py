#! /usr/bin/env python
from flask import Flask, render_template, request

app = Flask(__name__)
motorsEnabled = False


@app.route("/", methods=["GET","POST"])
def home():
    global motorsEnabled
    if request.method == "POST":
        action = request.form['action']
        if action == 'motorOn':
            motorsEnabled = True
        elif action == 'motorOff':
            motorsEnabled = False
  
    return render_template('index.html', motorsEnabled=motorsEnabled)


if __name__ == "__main__":
    #will run on: http://192.168.1.162:8080/
    app.run(host='0.0.0.0', port=8080, debug=True)
