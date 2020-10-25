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
        resp = make_response(jsonify({'redirect':'/furniture_show'}))
        return resp

@app.route('/job_class', methods=['GET', 'POST'])
def get_jobs():
    if request.method == 'POST':
        user_json = request.get_json()
        session['job_data'] = user_json 
        resp = make_response(jsonify({'redirect':'/jobs_show'}))
        return resp 

@app.route('/housing_class', methods=['GET', 'POST'])
def get_housing():
    if request.method == 'POST':
        user_json = request.get_json()
        session['housing_data'] = user_json 
        resp = make_response(jsonify({'redirect':'/housing_show'}))
        return resp

@app.route('/jobs_show')
def show_jobs():
    job_json = session['job_data']
    data = recommendations.get_job_recommendations(job_json)
    return render_template('jobs.html', data=data)

@app.route('/housing_show')
def show_housing():
    house_json = session['housing_data']
    data = recommendations.get_housing_recommendations(house_json)
    return render_template('housing.html', data=data)

@app.route('/furniture_show')
def show_furniture():
    furniture_json = session['furniture_data']
    data = recommendations.get_recommendations(furniture_json)
    print(data)
    return render_template('furniture.html', data=data)




















