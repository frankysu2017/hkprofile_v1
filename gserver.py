#!/usr/bin/env python3
# coding=utf-8
# ./profiles.py

from gevent.pywsgi import WSGIServer
from hkprofile import create_app

app = create_app('hkprofile.config.ProdConfig')

server = WSGIServer(('', 80), app)
server.serve_forever()