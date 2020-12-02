# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, jsonify

from app import app
from utils import EsControler
from utils import Const


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
        l = []
        rf = request.form
        couple_name_atr_val(Const.NAME, rf.get('firstname') + ' ' + rf.get('lastname'), l)
        couple_name_atr_val(Const.NATION, rf.get('nation'), l)
        couple_name_atr_val(Const.CLUB, rf.get('club'), l)
        couple_name_atr_val(Const.WEIGHT, rf.get('weight'), l)
        couple_name_atr_val(Const.HEIGHT, rf.get('height'), l)
        couple_name_atr_val(Const.RATING, rf.get('rating'), l)
        couple_name_atr_val(Const.FOOT, rf.get('foot'), l)
        r_form = dict(l)
        res = EsControler.search_player(r_form)
        return render_template('result.html', result=res)
    return render_template('result.html')


def __if_not_none__(r):
    if r:
        return 1
    return 0


def couple_name_atr_val(const, r, l):
    if __if_not_none__(r):
        l.append((const, r))
