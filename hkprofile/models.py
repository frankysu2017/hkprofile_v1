#!/usr/bin/env python3
# coding=utf-8
# hkprofile/models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

columns = {'id': '序号', 'cn_name': '中文名', 'en_name': '英文名', 'picture': '照片', 'gender': '性别', 'birthdate': '出生日期',
           'id_num': '身份证号', 'permit_num': '回乡证/通行证号', 'passport': '护照号',
           'home_address': '住宅地址', 'post_address': '邮寄地址', 'company_address': '办公地址', 'bank_account': '银行账号',
           'party_tag': '党派', 'occupation': '职业',
           'private_phone': '私人电话', 'office_phone': '办公电话', 'fax': '传真号码', 'other_number': '其他号码',
           'email': '电子邮件', 'internet_account': '网络账号', 'home_page': '个人网址',
           'family': '家庭情况', 'hobby': '兴趣爱好', 'experience': '个人经历', 'event': '重大事件', 'stain': '污点劣迹'}


class Person_info(db.Model):
    __tablename__ = 'person_info'

    col_names = list(columns.keys())
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    cn_name = db.Column(db.String(255))
    en_name = db.Column(db.String(255))
    picture = db.Column(db.LargeBinary)
    gender = db.Column(db.String(32))
    birthdate = db.Column(db.Date)
    id_num = db.Column(db.String(64))
    permit_num = db.Column(db.String(64))
    passport = db.Column(db.String(64))
    home_address = db.Column(db.String(255))
    port_address = db.Column(db.String(255))
    company_address = db.Column(db.String(255))
    bank_account = db.Column(db.String(64))
    party_tag = db.Column(db.String(255))
    occupation = db.Column(db.String(64))
    private_phone = db.Column(db.String(255))
    office_phone = db.Column(db.String(255))
    fax = db.Column(db.String(255))
    other_number = db.Column(db.String(255))
    email = db.Column(db.String(255))
    internet_account = db.Column(db.String(255))
    home_page = db.Column(db.String(255))
    family = db.Column(db.Text)
    hobby = db.Column(db.Text)
    experience = db.Column(db.Text)
    event = db.Column(db.Text)
    stain = db.Column(db.Text)

    def __init__(self, id):
        self.cn_name = id

    '''
    def __repr__(self):
        profile_dict = {'id': self.id, 'cn_name': self.cn_name, 'en_name': self.en_name}
        return str(profile_dict)
    '''