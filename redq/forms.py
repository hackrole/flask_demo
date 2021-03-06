# -*- coding: utf-8 -*-
# pylint: disable=import-error,too-few-public-methods,no-member
# pylint: disable=unused-import,unsubscriptable-object
# pylint: disable=attribute-defined-outside-init

from flask_wtf import Form
from flask_login import login_user
from pony import orm
from wtforms import ValidationError
from wtforms.validators import DataRequired
from wtforms import (StringField, PasswordField, BooleanField,
                     IntegerField, SubmitField, HiddenField)

from redq import models
from redq import rules


class LoginForm(Form):
    username = StringField(label=u'用户名', validators=[DataRequired()])
    password = PasswordField(label=u'密码', validators=[DataRequired()])
    submit = SubmitField(label=u"登录")

    @orm.db_session
    def validate(self, *args):
        if not super(LoginForm, self).validate(*args):
            return False

        # 验证并登录用户
        username = self.username.data
        password = self.password.data

        user = models.User.get(username=username)
        # pylint: disable=attribute-defined-outside-init
        if user is None:
            self._errors = {'username': ['username error!']}
            return False
        if not user.verify_password(password):
            self._errors = {'password': ['password error!']}
            return False
        if not user.is_active() or not user.is_admin:
            self._errors = {'username': ['invalid login!']}
            return False

        login_user(user)
        return True


class PermMixin(object):
    u"""user permission mixix"""
    allow_bulk_detect = BooleanField(label=u"批量检测", validators=[DataRequired()])
    allow_excel_detect = BooleanField(label=u"Excel检测")
    allow_voip_detect = BooleanField(label=u"深度检测")
    allow_detail_display = BooleanField(label=u"显示字段")
    allow_vote_define = BooleanField(label=u"自定义权重")
    allow_data_push = BooleanField(label=u"黑名单写入")

    def create_perm(self, user):
        u""" create user permssions """
        perms = [('allow_bulk_detect', self.allow_bulk_detect.data),
                 ('allow_excel_detect', self.allow_excel_detect.data),
                 ('allow_voip_detect', self.allow_voip_detect.data),
                 ('allow_detail_display', self.allow_detail_display.data),
                 ('allow_vote_define', self.allow_vote_define.data),
                 ('allow_data_push', self.allow_data_push.data)]
        for perm_name, value in perms:
            rules.create_user_perm(user, perm_name, value)


class CreateUserForm(Form, PermMixin):
    username = StringField(label=u"用户名", validators=[DataRequired()])
    email = StringField(label=u"邮箱", validators=[DataRequired()])
    company_name = StringField(label=u"公司名", validators=[DataRequired()])
    total_count = IntegerField(label=u"可用次数", validators=[DataRequired()])
    expire_time = IntegerField(label=u"过期时间", validators=[DataRequired()])
    # rate_limit = IntegerField(label=u"频率限制", validators=[DataRequired()])
    submit = SubmitField(label=u"创建")

    def validate_username(self, field):
        return not models.User.exists(username=field.data)

    @orm.db_session
    def validate(self, *args):
        if not super(CreateUserForm, self).validate(*args):
            return False

        # 验证并登录用户
        username = self.username.data
        password = '123456'
        email = self.email.data
        company_name = self.company_name.data
        total_count = self.total_count.data
        expire_time = self.total_count.data

        user = models.User(username=username, email=email,)
        user.password = password

        models.UserProfile(user=user, company_name=company_name,
                           current_query_count=total_count,
                           query_timeout=expire_time,)
        # create user permission
        self.create_perm(user)

        return True


class UpdateUserForm(Form, PermMixin):
    uid = HiddenField(label=u"用户id", required=True)
    total_count = IntegerField(label=u"可用次数")
    expire_time = IntegerField(label=u"过期时间")
    rate_limit = IntegerField(label=u"频率限制")
    # used_voip_count = BooleanField(label=u"已用voip次数")
    submit = SubmitField(label=u"创建")

    def __init__(self, uid, *args, **kw):
        super(UpdateUserForm, self).__init__(*args, **kw)
        self.uid.default = uid

    @orm.db_session
    def validate(self, *args):
        if not super(UpdateUserForm, self).validate(*args):
            return False

        try:
            user = models.User[self.uid.data]
        except orm.ObjectNotFound:
            self._errors = {'uid': [u'用户不存在']}
            return False

        total_count = self.total_count.data
        expire_time = self.expire_time.data
        # rate_limit = self.rate_limit.data

        user.total_count = total_count
        user.expire_time = expire_time

        # create user permission
        self.create_perm(user)

        return True


# XXX not finish
class ActiveUserForm(Form):
    u"""active user form"""
    uid = HiddenField(label=u"用户id", validators=[DataRequired()])
