#!/usr/bin/env python3
# coding=utf-8
# manage.py

import os
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from hkprofile import create_app
from hkprofile.models import db, PersonInfo


env = os.environ.get('HKPROFILE_ENV', 'dev')
app = create_app('hkprofile.config.{}Config'.format(env.capitalize()))

migrate = Migrate(app, db)


manager = Manager(app)
manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, PersonInfo=PersonInfo)


if __name__ == '__main__':
    manager.run()
