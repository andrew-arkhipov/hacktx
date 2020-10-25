from app import app 
from flask import render_template, request
from app.utils import scraper

@app.route('/')
def home():
    return render_template("landing.html")


@app.route('/enterInfo')
def enter_info():
    return render_template('enterInfo.html')


@app.route('/furniture_class', methods=['GET', 'POST'])
def get_furniture():
    if request.method == 'POST':
        user_json = request.get_json()
        furniture_array = user_json["elements"]
        city = user_json["city"]
        zip_code = user_json["zip_code"]

        print(user_json)
        return render_template('landing.html')

@app.route('/job_class', methods=['GET', 'POST'])
def get_jobs():
    if request.method == 'POST':
        pass


@app.route('/housing_class', methods=['GET', 'POST'])
def get_housing():
    if request.method == 'POST':
        pass

@app.route('/getAll', methods=['GET', 'POST'])
def get_all():
    if request.method == 'POST':
        pass


















