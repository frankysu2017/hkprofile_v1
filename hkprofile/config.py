#!/usr/bin/env python3
# coding=utf-8
# hkprofile/config.py

from os import path


class Config(object):
    SECRET_KEY = 'I HAVE A DREAM THAT ONE DAY...'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(path.pardir, 'database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

