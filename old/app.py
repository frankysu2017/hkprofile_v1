#!/usr/bin/env python3
# coding=utf-8

from gevent import monkey
import os
from flask import Flask
from flask import request, redirect, url_for
from flask_wtf import FlaskForm
from flask import render_template
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from wtforms import SubmitField, StringField
from flask_bootstrap import Bootstrap
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from db_conn import get_db
from datetime import timedelta
from gevent import pywsgi


monkey.patch_all()


app = Flask(__name__, static_url_path="/static",
            static_folder="static",
            template_folder="templates"
            )

app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()
app.config['SECRET_KEY'] = 'I have a dream that one day...'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)
bootstrap = Bootstrap(app)

app.send_file_max_age_default = timedelta(seconds=1)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class UploadForm(FlaskForm):
    photo = FileField(validators=[
        FileAllowed(photos, u'只能上传图片！'),
        FileRequired(u'文件未选择！')])
    submit = SubmitField(u'上传')


class QueryForm(FlaskForm):
    name = StringField('Input the Query String here:', validators=[DataRequired()])
    submit = SubmitField('嗖嗖嗖！')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    db = get_db()
    cur = db.cursor()
    form = QueryForm()
    #if form.validate_on_submit():
    query_str = form.name.data
    sql_str = "SELECT * FROM person where cn_name like '%{q}%' or en_name like '%{q}%' or gender like '%{q}%' or " \
              "birthdate like '%{q}%' or id_num like '%{q}%' or permit_num like '%{q}%' or passort like '%{q}%' or " \
              "home_address like '%{q}%' or post_address like '%{q}%' or company_address like '%{q}%' or party like '%{q}%' or " \
              "occupation like '%{q}%' or private_phone like '%{q}%' or company_phone like '%{q}%' or fax like '%{q}%' or " \
              "email like '%{q}%' or internet_account like '%{q}%' or homepage like '%{q}%' or bank_account like '%{q}%' or " \
              "other_number like '%{q}%' or family like '%{q}%' or hobby like '%{q}%' or experience like '%{q}%' or " \
              "event like '%{q}%' or stain like '%{q}%';".format(q=query_str)

    result = cur.execute(sql_str).fetchall()
    if result:
        return render_template('list.html', form=form, data=result)
    else:
        return render_template('index.html', form=form, result=None)


@app.route('/list')
def list():
    db = get_db()
    cur = db.cursor()
    data = cur.execute('SELECT * FROM person ORDER BY id').fetchall()
    return render_template('list.html', data=data)


@app.route('/profile/<int:id>')
def profile(id):
    db = get_db()
    cur = db.cursor()
    data = cur.execute('SELECT * from person where id = ?', (id, )).fetchall()
    data = [x for x in data[0]]
    if data[3]:
        data[3] = data[3].split('\n')[:-1]
    data = tuple(data)
    return render_template('profile.html', data=data)


@app.route('/occupation')
def occupation():
    db = get_db()
    cur = db.cursor()
    data = cur.execute('SELECT occupation, count(*) from person group by occupation').fetchall()
    return render_template('occupation.html', data=data)


@app.route('/list/occupation/<occupation>')
def listoccupation(occupation):
    db = get_db()
    cur = db.cursor()
    if occupation == ' mysmwtsngzdgtd':
        data = cur.execute('SELECT * FROM person where occupation="" or occupation is NULL ').fetchall()
    else:
        data = cur.execute('SELECT * FROM person where occupation=?', (occupation.lstrip(),)).fetchall()
    return render_template('list.html', data=data)


@app.route('/party')
def party():
    db = get_db()
    cur = db.cursor()
    data = cur.execute('SELECT party, count(*) from person group by party').fetchall()
    return render_template('party.html', data=data)


@app.route('/list/party/<party>')
def listparty(party):
    db = get_db()
    cur = db.cursor()
    if party == ' mysmwtsngzdgtd':
        data = cur.execute('SELECT * FROM person where party="" or occupation is NULL ').fetchall()
    else:
        data = cur.execute('SELECT * FROM person where party=?', (party.lstrip(),)).fetchall()
    return render_template('list.html', data=data)


@app.route('/insert')
@app.route('/insert',  methods=['POST'])
def insert():
    if request.method == 'POST':
        cn_name = request.form['cn_name']
        en_name = request.form['en_name']
        picture = request.form['picture']
        gender = request.form['gender']
        birthdate = request.form['birthdate']
        id_num = request.form['id_num']
        permit_num = request.form['permit_num']
        passport = request.form['passport']
        home_address = request.form['home_address']
        post_address = request.form['post_address']
        company_address = request.form['company_address']
        party = request.form['party']
        occupation = request.form['occupation']
        private_phone = request.form['private_phone']
        company_phone = request.form['company_phone']
        fax = request.form['fax']
        email = request.form['email']
        internet_account = request.form['internet_account']
        homepage = request.form['homepage']
        bank_account = request.form['bank_account']
        other_number = request.form['other_number']
        family = request.form['family']
        hobby = request.form['hobby']
        experience = request.form['experience']
        event = request.form['event']
        stain = request.form['stain']
        db = get_db()
        cur = db.cursor()
        cur.execute(
            'INSERT INTO person (cn_name, en_name, picture, gender, birthdate, id_num, permit_num, passort, home_address, '
            'post_address, company_address, party, occupation, private_phone, company_phone, fax, email, '
            'internet_account, homepage, bank_account, other_number, family, hobby, experience, event, stain) VALUES '
            '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (cn_name, en_name, picture, gender, birthdate, id_num, permit_num, passport, home_address, post_address, company_address, party, occupation, private_phone, company_phone, fax, email, internet_account, homepage, bank_account, other_number, family, hobby, experience, event, stain)
        )
        db.commit()
        idn = cur.execute('select max(id) from person').fetchall()[0]
        return redirect(url_for('profile', id=idn[0]))
    else:
        return render_template('insert.html')


@app.route('/edit/<int:id>')
@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    if request.method == 'POST':
        cn_name = request.form['cn_name']
        en_name = request.form['en_name']
        picture = request.form['picture']
        gender = request.form['gender']
        birthdate = request.form['birthdate']
        id_num = request.form['id_num']
        permit_num = request.form['permit_num']
        passort = request.form['passport']
        home_address = request.form['home_address']
        post_address = request.form['post_address']
        company_address = request.form['company_address']
        party = request.form['party']
        occupation = request.form['occupation']
        private_phone = request.form['private_phone']
        company_phone = request.form['company_phone']
        fax = request.form['fax']
        email = request.form['email']
        internet_account = request.form['internet_account']
        homepage = request.form['homepage']
        bank_account = request.form['bank_account']
        other_number = request.form['other_number']
        family = request.form['family']
        hobby = request.form['hobby']
        experience = request.form['experience']
        event = request.form['event']
        stain = request.form['stain']
        db = get_db()
        cur = db.cursor()
        if picture:
            cur.execute(
                "UPDATE person SET cn_name=?, en_name=?, picture=?||'\n'||picture, gender=?, birthdate=?, id_num=?, permit_num=?, passort=?, home_address=?, post_address=?, company_address=?, party=?, occupation=?, private_phone=?, company_phone=?, fax=?, email=?, internet_account=?, homepage=?, bank_account=?, other_number=?, family=?, hobby=?, experience=?, event=?, stain=? WHERE id = ?",
                (cn_name, en_name, picture, gender, birthdate, id_num, permit_num, passort, home_address, post_address, company_address, party, occupation, private_phone, company_phone, fax, email, internet_account, homepage, bank_account, other_number, family, hobby, experience, event, stain, id)
            )
        else:
            cur.execute(
                "UPDATE person SET cn_name=?, en_name=?, gender=?, birthdate=?, id_num=?, permit_num=?, passort=?, home_address=?, post_address=?, company_address=?, party=?, occupation=?, private_phone=?, company_phone=?, fax=?, email=?, internet_account=?, homepage=?, bank_account=?, other_number=?, family=?, hobby=?, experience=?, event=?, stain=? WHERE id = ?",
                (cn_name, en_name, gender, birthdate, id_num, permit_num, passort, home_address, post_address, company_address, party, occupation, private_phone, company_phone, fax, email, internet_account, homepage, bank_account, other_number, family, hobby, experience, event, stain, id)
            )
        db.commit()
        return redirect(url_for('profile', id=id))
    else:
        db = get_db()
        cur = db.cursor()
        data = cur.execute('SELECT * FROM person WHERE id = ?', (id,)).fetchone()
        print(data[23])
        data = [x for x in data]
        if data[3]:
            data[3] = data[3].split('\n')
        data = tuple(data)
        return render_template('edit.html', data=data)


@app.route('/delete/<int:id>')
def delete(id):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        'DELETE FROM person WHERE id = ?', (id,)
    )
    db.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.debug = True
    app.run(host='127.0.0.1', port='80')

    #server = pywsgi.WSGIServer(('0.0.0.0', 80), app)
    #server.serve_forever()
