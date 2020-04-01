#!/usr/bin/env python3
# coding=utf-8
# hkprofile/controllers/profiles.py

import ast

from flask import Blueprint, render_template, request,url_for, redirect
from datetime import datetime
from sqlalchemy import or_

from models import db, PersonInfo, Avatar
from forms import QueryForm

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


@query.route('/', methods=['GET', 'POST'])
@query.route('/index', methods=['GET', 'POST'])
def index():
    form = QueryForm()
    if request.method == 'POST':
        query_str = form.name.data
        p = PersonInfo.query.filter(or_(
            PersonInfo.cn_name.like('%{}%'.format(query_str)),
            PersonInfo.en_name.like('%{}%'.format(query_str)),
            PersonInfo.gender.like('%{}%'.format(query_str)),
            PersonInfo.id_num.like('%{}%'.format(query_str)),
            PersonInfo.permit_num.like('%{}%'.format(query_str)),
            PersonInfo.passport.like('%{}%'.format(query_str)),
            PersonInfo.home_address.like('%{}%'.format(query_str)),
            PersonInfo.post_address.like('%{}%'.format(query_str)),
            PersonInfo.company_address.like('%{}%'.format(query_str)),
            PersonInfo.bank_account.like('%{}%'.format(query_str)),
            PersonInfo.party_tag.like('%{}%'.format(query_str)),
            PersonInfo.occupation.like('%{}%'.format(query_str)),
            PersonInfo.private_phone.like('%{}%'.format(query_str)),
            PersonInfo.office_phone.like('%{}%'.format(query_str)),
            PersonInfo.fax.like('%{}%'.format(query_str)),
            PersonInfo.other_number.like('%{}%'.format(query_str)),
            PersonInfo.email.like('%{}%'.format(query_str)),
            PersonInfo.internet_account.like('%{}%'.format(query_str)),
            PersonInfo.home_page.like('%{}%'.format(query_str)),
            PersonInfo.family.like('%{}%'.format(query_str)),
            PersonInfo.hobby.like('%{}%'.format(query_str)),
            PersonInfo.experience.like('%{}%'.format(query_str)),
            PersonInfo.event.like('%{}%'.format(query_str)),
            PersonInfo.stain.like('%{}%'.format(query_str))
        )).all()

        return render_template('list.html', data=p)
    else:
        return render_template('index.html', form=form)


@query.route('/list')
def person_list():
    p_list = PersonInfo.query.all()
    return render_template('list.html', data=p_list)


@query.route('/insert', methods=['POST', 'GET'])
def insert():
    if request.method == 'POST':
        if request.form['birthdate']:
            b_date = datetime.strptime(request.form['birthdate'], '%m/%d/%Y')
        else:
            b_date = None
        p = PersonInfo(
            cn_name=request.form['cn_name'], en_name=request.form['en_name'], gender=request.form['gender'],
            birthdate=b_date, id_num=request.form['id_num'], permit_num=request.form['permit_num'],
            passport=request.form['passport'], home_address=request.form['home_address'],
            post_address=request.form['post_address'], company_address=request.form['company_address'],
            party_tag=request.form['party'], occupation=request.form['occupation'], private_phone=request.form['private_phone'],
            office_phone=request.form['company_phone'], fax=request.form['fax'], email=request.form['email'],
            internet_account=request.form['internet_account'], home_page=request.form['homepage'],
            bank_account=request.form['bank_account'], other_number=request.form['other_number'],
            family=request.form['family'], hobby=request.form['hobby'], experience=request.form['experience'],
            event=request.form['event'], stain=request.form['stain']
        )
        if request.form['picture']:
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
    PersonInfo.query.filter(PersonInfo.party_tag is None).update({'party_tag': ''})
    p_list = db.session.query(PersonInfo.party_tag, db.func.count('*').label('c')).group_by(PersonInfo.party_tag).all()
    return render_template('party.html', party_list=p_list)


@query.route('/party/<partyname>')
def party_member(partyname):
    if partyname == ' mysmwtsngzdgtd':
        party_members = PersonInfo.query.filter(or_(PersonInfo.party_tag is None, PersonInfo.party_tag == '')).all()
    else:
        party_members = PersonInfo.query.filter(PersonInfo.party_tag == partyname.lstrip()).all()
    return render_template('list.html', data=party_members)


@query.route('/occupation')
def occupation_list():
    PersonInfo.query.filter(PersonInfo.occupation is None).update({'occupation': ''})
    o_list = db.session.query(PersonInfo.occupation, db.func.count('*').label('c')).group_by(PersonInfo.occupation).all()
    return render_template('occupation.html', occu_list=o_list)


@query.route('/occupation/<occupationname>')
def occupation_member(occupationname):
    if occupationname == ' mysmwtsngzdgtd':
        occu_members = PersonInfo.query.filter(or_(PersonInfo.occupation is None, PersonInfo.occupation == '')).all()
    else:
        occu_members = PersonInfo.query.filter(PersonInfo.occupation == occupationname.lstrip()).all()
    return render_template('list.html', data=occu_members)


@query.route('/tags', methods=['POST', 'GET'])
def tags():
    PersonInfo.query.filter(PersonInfo.party_tag is None).update({'party_tag': ''})
    p_list = []
    for item in db.session.query(PersonInfo.party_tag).distinct().all():
        if item.party_tag:
            p_list.append({'party_tag': item.party_tag})
        else:
            p_list.append({'party_tag': "党派未录入"})
    if request.method == 'POST':
        checked_list = [x.strip() for x in request.form.getlist('partytags')]
        for item in p_list:
            if item['party_tag'] in checked_list:
                item['flag'] = "checked"
            else:
                item['flag'] = ""
        persons = []
        for tag in checked_list:
            tag = tag
            if tag == '党派未录入':
                persons.extend(PersonInfo.query.filter(or_(PersonInfo.party_tag is None, PersonInfo.party_tag == '')).all())
            else:
                persons.extend(PersonInfo.query.filter(PersonInfo.party_tag == tag).all())
        return render_template('tags.html', party_list=p_list, data=persons)
    else:
        return render_template('tags.html', party_list=p_list)


@profile.route('/<int:person_id>')
def detail(person_id=0):
    p = PersonInfo.query.get(person_id)
    return render_template('profile.html', p=p)


@profile.route('/edit/<int:person_id>', methods=['POST', 'GET'])
def edit(person_id=0):
    p = PersonInfo.query.get(person_id)
    if request.method == 'POST':
        if request.form['birthdate']:
            b_date = datetime.strptime(request.form['birthdate'], '%m/%d/%Y')
        else:
            b_date = None
        p.cn_name = request.form['cn_name']
        p.en_name = request.form['en_name']
        p.gender = request.form['gender']
        p.birthdate = b_date
        p.id_num = request.form['id_num']
        p.permit_num = request.form['permit_num']
        p.passport = request.form['passport']
        p.home_address = request.form['home_address']
        p.post_address = request.form['post_address']
        p.company_address = request.form['company_address']
        p.party_tag = request.form['party']
        p.occupation = request.form['occupation']
        p.private_phone = request.form['private_phone']
        p.office_phone = request.form['company_phone']
        p.fax = request.form['fax']
        p.email = request.form['email']
        p.internet_account = request.form['internet_account']
        p.home_page = request.form['homepage']
        p.bank_account = request.form['bank_account']
        p.other_number = request.form['other_number']
        p.family = request.form['family']
        p.hobby = request.form['hobby']
        p.experience = request.form['experience']
        p.event = request.form['event']
        p.stain = request.form['stain']
        if request.form['picture']:
            for item in request.form['picture'].split('\n'):
                avt = Avatar(item)
                p.avatar.append(avt)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('profile.detail', person_id=person_id))
    else:
        if p.birthdate:
            timestring = datetime.strftime(p.birthdate, '%m/%d/%Y')
        else:
            timestring = ''
        return render_template('edit.html', t=timestring, p=p)


@profile.route('/avatar/<int:person_id>', methods=['POST', 'GET'])
def avatar_edit(person_id):
    p = PersonInfo.query.get(person_id)
    if request.method == 'POST':
        a=Avatar.query.get(int(request.form['del_id']))
        db.session.delete(a)
        db.session.commit()
        return render_template('gallery.html', p=p)
    else:
        return render_template('gallery.html', p=p)
