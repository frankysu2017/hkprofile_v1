#!/usr/bin/env python3
# coding=utf-8
# hkprofile/controllers/profiles.py

from flask import Blueprint, render_template, request,url_for, redirect
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

from models import db, PersonInfo


class QueryForm(FlaskForm):
    name = StringField('Input the Query String here:', validators=[DataRequired()])
    submit = SubmitField('嗖嗖嗖！')


profile = Blueprint(
    'profile',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/profile'
)

query = Blueprint(
    'query',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/'
)


@profile.route('/<int:person_id>')
@profile.route('/')
def pro_id(person_id=0):
    return render_template('profile_new.html', id=person_id)


@query.route('/', methods=['GET', 'POST'])
@query.route('/index', methods=['GET', 'POST'])
def index():
    form = QueryForm()
    if request.method == 'POST':
        query_str = int(form.name.data)
        p = PersonInfo.query.get(query_str)
        return render_template('profile_new.html', id=p)
    else:
        return render_template('index.html', form=form)