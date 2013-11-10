#!/usr/bin/env python

from flask import Flask, render_template, url_for
# url_for('static', filename='service_status.json')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__=="__main__":
    port = 5000
    app.debug = True
    app.run( port=port )
