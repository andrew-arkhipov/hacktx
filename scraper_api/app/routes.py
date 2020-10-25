from app import app 
from flask import render_template

@app.route('/')
def home():
    return 'hello world'


@app.route('/enterInfo')
def enter_info():
    return render_template('enterInfo.html')


