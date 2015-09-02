# -*- coding: utf-8 -*-
__author__ = 'wushuyi'
from flask import abort, redirect, request, url_for
from flask.ext.security import current_user
from flask_admin.contrib import sqla
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib import rediscli
from wtforms.validators import required
from flask_admin.helpers import get_form_data
from forms.user_from import MyPasswordField
from wtforms.fields import TextAreaField, HiddenField


class ViewAuthMixin(object):
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


class MyModelView(ViewAuthMixin, sqla.ModelView):
    pass


class MyFileAdmin(ViewAuthMixin, FileAdmin):
    pass


class MyRedisCli(ViewAuthMixin, rediscli.RedisCli):
    pass


class RoleModelView(MyModelView):
    column_default_sort = 'id'
    column_display_pk = True
    page_size = 10
    can_view_details = True
    column_searchable_list = ['name', ]

    column_labels = {
        'id': 'ID',
        'name': '权限',
        'description': '介绍',
        'users': '用户'
    }

    form_args = {
        'name': {
            'validators': [required(message='必须填写!')]
        }
    }


class UserModelView(MyModelView):
    column_default_sort = 'id'
    column_display_pk = True
    page_size = 10
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

    column_formatters = {
        'password': lambda v, c, m, p: '*****'
    }

    def edit_form(self, obj=None):
        Form = self.scaffold_form()

        class MyForm(Form):
            password = MyPasswordField('密码')

        return MyForm(get_form_data(), obj=obj)


class BlogPostModelView(MyModelView):
    column_default_sort = 'id'
    column_display_pk = True
    page_size = 10
    can_view_details = True
    column_list = ['id', 'title', 'uri_path', 'classify']
    column_searchable_list = ['title', ]
    column_filters = ['title', 'content', 'classify.name']
    column_labels = {
        'id': 'ID',
        'uri_path': '路径',
        'title': '标题',
        'content': '内容',
        'markdown': 'Markdown',
        'classify.name': '归类',
        'classify': '归类',
    }
    form_columns = (
        'title',
        'markdown',
        'classify',
        'uri_path',
    )
    form_args = {
        'title': {
            'validators': [required(message='必须填写!')]
        },
        'markdown': {
            'validators': [required(message='必须填写!')]
        },
        'classify': {
            'validators': [required(message='必须填写!')]
        },
        'uri_path': {
            'validators': [required(message='必须填写!')]
        },
    }

    create_template = 'admin/create_post.html'
    edit_template = 'admin/edit_post.html'

    def create_form(self, obj=None):
        Form = self.scaffold_form()

        class MyForm(Form):
            markdown = TextAreaField('Markdown')
            content = HiddenField('内容')

        return MyForm(get_form_data(), obj=obj)

    def edit_form(self, obj=None):
        Form = self.scaffold_form()

        class MyForm(Form):
            markdown = TextAreaField('Markdown')
            content = HiddenField('内容')

        return MyForm(get_form_data(), obj=obj)

        # @expose('/new/', methods=('GET', 'POST'))
        # def create_view(self):
        #     return self.render('admin/add_post.html')


class BlogClassifyModelView(MyModelView):
    column_default_sort = 'id'
    column_display_pk = True
    page_size = 10
    can_view_details = True
    column_labels = {
        'id': 'ID',
        'uri_path': '路径',
        'name': '名称',
        'blogposts': '文章',
    }
    column_list = ['id', 'name', 'uri_path']
    column_searchable_list = ['name', ]
    column_filters = ['name', 'uri_path']
    form_columns = (
        'name',
        'uri_path',
        'blogposts',
    )
