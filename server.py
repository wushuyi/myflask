# -*- coding: utf-8 -*-
__author__ = 'wushuyi'
from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from myapp import app, register_all

app.config['DEBUG'] = False

register_all()

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
