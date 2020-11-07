# -*- coding: utf-8 -*-
from flask import render_template

from app import app


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/top_raiting', methods=["GET"])
def top_rait():
    pass
