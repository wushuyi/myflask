# -*- coding: utf-8 -*-
__author__ = 'wushuyi'
from flask import request, session
from flask.ext.babelex import Babel

babel = Babel()


@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'zh_Hans_CN')


def register(app):
    babel.init_app(app)
