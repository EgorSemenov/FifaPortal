# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for,jsonify

from app import app


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')


@app.route('/goto', methods=['POST'])
def to_filter():
    if request.method == 'POST':
        print(request.form)
        print(request.form['to_filter'])
        if request.form['to_filter'] == "Player search":
            return redirect(url_for('filter'))
    return redirect(url_for('filter'))


@app.route('/filter')
def filter():
    return render_template('filter.html')


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        result = (
            request.form.get('firstname'),
            request.form.get('lastname'),
            request.form.get('nation'),
            request.form.get('club'),
            request.form.get('weight'),
            request.form.get('height'),
            request.form.get('rating'),
            request.form.get('foot')
        )
        return render_template('result.html', result=result)
    return render_template('result.html')
