#!/usr/bin/env python3
# coding=utf-8
# hkprofile/__init__.py


from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap

from .models import db
from .controllers.profiles import profile, query

bootstrap = Bootstrap()


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    bootstrap.init_app(app)
    app.register_blueprint(profile)
    app.register_blueprint(query)

    @app.route('/')
    def index():
        return redirect(url_for('query.index'))

    return app
