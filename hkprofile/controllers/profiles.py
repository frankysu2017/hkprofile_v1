#!/usr/bin/env python3
# coding=utf-8
# hkprofile/controllers/profiles.py

import ast

from flask import Blueprint, render_template, request,url_for, redirect
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from datetime import datetime

from models import db, PersonInfo, Avatar


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
def detail(person_id=0):
    p = PersonInfo.query.get(person_id)
    return render_template('profile.html', p=p)


@query.route('/', methods=['GET', 'POST'])
@query.route('/index', methods=['GET', 'POST'])
def index():
    form = QueryForm()
    if request.method == 'POST':
        query_str = form.name.data
        p = PersonInfo.query.filter(PersonInfo.cn_name.like('%{}%'.format(query_str))).all()

        return render_template('profile_new.html', p=p[0])
    else:
        return render_template('index.html', form=form)


@query.route('/list')
def person_list():
    p_list = PersonInfo.query.all()
    return render_template('list.html', p_list=p_list)


@query.route('/insert',methods=['POST', 'GET'])
def insert():
    if request.method == 'POST':
        p = PersonInfo(
            cn_name=request.form['cn_name'], en_name=request.form['en_name'], gender=request.form['gender'],
            birthdate=datetime.strptime(request.form['birthdate'], '%m/%d/%Y'), id_num=request.form['id_num'],
            permit_num=request.form['permit_num'], passport=request.form['passport'], home_address=request.form['home_address'],
            post_address=request.form['post_address'], company_address=request.form['company_address'],
            party_tag=request.form['party'], occupation=request.form['occupation'], private_phone=request.form['private_phone'],
            office_phone=request.form['company_phone'], fax=request.form['fax'], email=request.form['email'],
            internet_account=request.form['internet_account'], home_page=request.form['homepage'],
            bank_account=request.form['bank_account'], other_number=request.form['other_number'],
            family=request.form['family'], hobby=request.form['hobby'], experience=request.form['experience'],
            event=request.form['event'], stain=request.form['stain']
        )
        for item in request.form['picture'].split('\n'):
            avt = Avatar(item)
            p.avatar.append(avt)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('profile.detail', person_id=p.id))
    else:
        return render_template('insert.html')


@query.route('/party')
def party_list():
    party_list = db.session.query(PersonInfo.party_tag, db.func.count('*')).group_by(PersonInfo.party_tag).all()
    return render_template('party.html', data=party_list)


@query.route('/party/<partyname>')
def party_member(partyname):
    party_members = db.session.query(PersonInfo.party_tag=partyname).all()