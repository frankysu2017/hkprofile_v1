#!/usr/bin/env python3
# coding=utf-8
# hkprofile/forms.py


from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class QueryForm(FlaskForm):
    name = StringField('Input the Query String here:', validators=[DataRequired()])
    submit = SubmitField('嗖嗖嗖！')