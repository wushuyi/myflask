# -*- coding: utf-8 -*-
__author__ = 'wushuyi'
from flask.ext.admin.form import BaseForm
from wtforms import fields
from wtforms import widgets
from wtforms.compat import text_type
from wtforms.validators import StopValidation
from flask.ext.security.utils import encrypt_password


class MyPasswordField(fields.Field):
    widget = widgets.TextInput()

    def process_data(self, value):
        self._oldData = value
        self.data = '*****'

    def pre_validate(self, form):
        no_change = '*****'
        if form.data['password'] == no_change:
            self.data = self._oldData
        else:
            self.data = encrypt_password(form.data['password'])

    def _value(self):
        return text_type(self.data) if self.data is not None else ''

# class MyForm(BaseForm):
#     first_name = fields.StringField('用户名')
#     active = fields.BooleanField('激活')
#     password = MyPasswordField('密码')
#     roles = fields.StringField('权限')
