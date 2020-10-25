from app import app 
from flask import render_template, request, redirect, url_for, session, make_response, jsonify
from app.utils import recommendations

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
        session['furniture_data'] = user_json
        resp = make_response(jsonify({'redirect':'/show_furniture'}))
        return resp

@app.route('/show_furniture')
def show_furniture():
    furniture_json = session['furniture_data']
    data = get_recommendations(furniture_json)
    return render_template('furniture.html', data=data)

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


















