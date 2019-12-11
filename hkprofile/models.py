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


class PersonInfo(db.Model):
    __tablename__ = 'person_info'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    picture = db.Column(db.LargeBinary)
    birthdate = db.Column(db.Date)
    for key in list(columns.keys())[1:3]+list(columns.keys())[4:5] + list(columns.keys())[6:22]:
        exec("%s = db.Column(db.String(255))" % key)
    for key in list(columns.keys())[22:]:
        exec("%s = db.Column(db.Text)" % key)

    '''
    cn_name = db.Column(db.String(255))
    en_name = db.Column(db.String(255))
    gender = db.Column(db.String(32))
    id_num = db.Column(db.String(64))
    permit_num = db.Column(db.String(64))
    passport = db.Column(db.String(64))
    home_address = db.Column(db.String(255))
    post_address = db.Column(db.String(255))
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
    '''

    def __init__(self, id, cn_name=None, en_name=None, picture=None, gender=None, birthdate=None, id_num=None,
                 permit_num=None, passport=None, home_address=None, post_address=None, company_address=None,
                 bank_account=None, party_tag=None, occupation=None, private_phone=None, office_phone=None,
                 fax=None, other_number=None, email=None, internet_account=None, home_page=None,
                 family=None, hobby=None, experience=None, event=None, stain=None):
        self.id = id
        self.cn_name = cn_name
        self.en_name = en_name
        self.picture = picture
        self.gender = gender
        self.birthdate = birthdate
        self.id_num = id_num
        self.permit_num = permit_num
        self.passport = passport
        self.home_address = home_address
        self.post_address = post_address
        self.company_address = company_address
        self.bank_account = bank_account
        self.party_tag = party_tag
        self.occupation = occupation
        self.private_phone = private_phone
        self.office_phone = office_phone
        self.fax = fax
        self.other_number = other_number
        self.email = email
        self.internet_account = internet_account
        self.home_page = home_page
        self.family = family
        self.hobby = hobby
        self.experience = experience
        self.event = event
        self.stain = stain

    def __repr__(self):
        profile_dict = {
            'id': self.id, 'cn_name': self.cn_name, 'en_name': self.en_name, 'picture': self.picture,
            'gender': self.gender, 'birthdate': self.birthdate, 'id_num': self.id_num,
            'permit_num': self.permit_num, 'passport': self.passport, 'home_address': self.home_address,
            'post_address': self.post_address, 'company_address': self.company_address,
            'bank_account': self.bank_account, 'party_tag': self.party_tag, 'occupation': self.occupation,
            'private_phone': self.private_phone, 'office_phone': self.office_phone, 'fax': self.fax,
            'other_number': self.other_number, 'email': self.email, 'internet_account': self.internet_account,
            'home_page': self.home_page, 'family': self.family, 'hobby': self.hobby,
            'experience': self.experience, 'event': self.event, 'stain': self.stain
        }
        return str(profile_dict)
