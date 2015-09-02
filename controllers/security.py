# -*- coding: utf-8 -*-
__author__ = 'wushuyi'

from flask import Blueprint, render_template
from flask.ext.security import Security, SQLAlchemyUserDatastore
from model import db
from model.security import User, Role
from controllers.admin import export_processor

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app=None, datastore=user_datastore)

security_page = Blueprint('security_page ', __name__,
                          template_folder='templates')

# Views
@security_page.route('/')
def home():
    return render_template('index.html')


def register(app):
    if not hasattr(app, 'extensions'):
        app.extensions = {}
    if not hasattr(app.extensions, 'sqlalchemy'):
        db.init_app(app)

    security.init_app(app)

    @app.context_processor
    def security_context_processor():
        print(export_processor())
        return export_processor()

    app.register_blueprint(security_page)
