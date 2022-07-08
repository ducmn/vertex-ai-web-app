import os
from flask import Flask, render_template, request, redirect, url_for
from flask import json as fJson

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'static'

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/', methods = ['POST'])
def upload_file():
   uploaded_file = request.files['file']
   if uploaded_file.filename != '':
      uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], uploaded_file.filename))
   return redirect(url_for('index'))