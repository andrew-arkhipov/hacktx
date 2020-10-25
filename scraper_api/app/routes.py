from app import app 
from flask import render_template, request
from app.utils import scraper

@app.route('/')
def home():
    return render_template("landing.html")


@app.route('/enterInfo')
def enter_info():
    return render_template('enterInfo.html')


@app.route('/processInfo')
def process_info():
    if request.method == 'POST':
        user_json = request.get_json()
        location = user_json["location"]
        family_number = user_json["family_number"]
        income = user_json["income"]

















