# -*- coding: utf-8 -*-
__author__ = 'wushuyi'
import flask_admin
from flask_admin import helpers as admin_helpers
import os.path as path
from model.link_redis import strictredis
from model.blog import BlogClassify, BlogPost
from model import db
from model.security import User, Role
from view.admin import BlogPostModelView, BlogClassifyModelView, \
    RoleModelView, UserModelView, MyFileAdmin, MyRedisCli

admin = flask_admin.Admin(
    name='Admin',
    base_template='my_master.html',
    template_mode='bootstrap3'
)
admin.add_view(BlogPostModelView(BlogPost, db.session, name='文章管理'))
admin.add_view(BlogClassifyModelView(BlogClassify, db.session, name='归类管理'))
admin.add_view(RoleModelView(Role, db.session, name='角色管理'))
admin.add_view(UserModelView(User, db.session, name='用户管理'))
path = path.join(path.dirname(__file__), '../static')
admin.add_view(MyFileAdmin(path, '/static/', name='文件管理'))
admin.add_view(MyRedisCli(strictredis, name='Redis管理'))


def register(app):
    if not hasattr(app, 'extensions'):
        app.extensions = {}
    if not hasattr(app.extensions, 'sqlalchemy'):
        db.init_app(app)
    admin.init_app(app)


def export_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
    )
