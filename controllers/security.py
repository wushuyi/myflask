# -*- coding: utf-8 -*-
__author__ = 'wushuyi'

from flask import Blueprint, abort, redirect, url_for, request, \
    render_template, session
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    current_user
from flask.ext.babelex import Babel
from model import db
from model.security import User, Role
import flask_admin
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from wtforms.validators import required
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op
from model.link_redis import strictredis
from flask_admin.contrib import rediscli
from forms.user_from import MyPasswordField
from flask_admin.helpers import get_form_data

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app=None, datastore=user_datastore)
babel = Babel()

security_page = Blueprint('security_page ', __name__,
                          template_folder='templates')


@babel.localeselector
def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'zh_Hans_CN')


class MyModelView(sqla.ModelView):
    def is_accessible(self):
        if not current_user.is_active() or not current_user.is_authenticated():
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated():
                abort(403)
            else:
                return redirect(url_for('security.login', next=request.url))


class RoleModelView(MyModelView):
    column_display_pk = True
    can_view_details = True
    column_searchable_list = ['name', ]


class UserModelView(MyModelView):
    can_view_details = True
    column_exclude_list = ['password', 'confirmed_at', 'last_name', 'last_login_ip', 'last_login_at']
    column_searchable_list = ['first_name', 'email']
    column_filters = ['email', ]

    column_labels = {
        'id': 'ID',
        'first_name': '用户名',
        'last_name': '昵称',
        'email': '电子邮箱',
        'password': '密码',
        'active': '激活状态',
        'confirmed_at': '认证时间',
        'last_login_at': '最后登录时间',
        'current_login_at': '现在登录时间',
        'last_login_ip': '最后登录IP',
        'current_login_ip': '现在登录IP',
        'login_count': '登录次数',
        'roles': '权限'
    }

    form_columns = (
        'first_name',
        'last_name',
        'email',
        'password',
        'active',
        'roles',
    )

    form_args = {
        'first_name': {
            'validators': [required(message='必须填写!')]
        },
        'password': {
            'validators': [required(message='必须填写!')]
        },
        'email': {
            'validators': [required(message='必须填写!')]
        }
    }

    column_default_sort = 'id'
    column_display_pk = True
    page_size = 10

    column_formatters = {
        'password': lambda v, c, m, p: '*****'
    }

    def edit_form(self, obj=None):
        Form = self.scaffold_form()

        class MyForm(Form):
            password = MyPasswordField('密码')

        return MyForm(get_form_data(), obj=obj)


path = op.join(op.dirname(__file__), '../static')

admin = flask_admin.Admin(
    name='Admin',
    base_template='my_master.html',
    template_mode='bootstrap3'
)

admin.add_view(FileAdmin(path, '/static/', name='文件管理'))
admin.add_view(RoleModelView(Role, db.session, name='角色'))
admin.add_view(UserModelView(User, db.session, name='用户'))
admin.add_view(rediscli.RedisCli(strictredis, name='Redis管理'))


# Views
@security_page.route('/')
def home():
    return render_template('index.html')


def register(app):
    db.init_app(app)
    babel.init_app(app)
    security.init_app(app)
    admin.init_app(app)

    @app.context_processor
    def security_context_processor():
        return dict(
            admin_base_template=admin.base_template,
            admin_view=admin.index_view,
            h=admin_helpers,
        )

    app.register_blueprint(security_page)
