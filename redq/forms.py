# -*- coding: utf-8 -*-
# pylint: disable=import-error,too-few-public-methods,no-member
# pylint: disable=unused-import

from flask_wtf import Form
from flask_login import login_user
from pony import orm
from wtforms import ValidationError
from wtforms.validators import DataRequired
from wtforms import (StringField, PasswordField, BooleanField,
                     IntegerField, SubmitField)

from redq import pony_models as models
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


class CreateUserForm(Form):
    username = StringField(label=u"用户名", validators=[DataRequired()])
    email = StringField(label=u"邮箱", validators=[DataRequired()])
    company_name = StringField(label=u"公司名", validators=[DataRequired()])
    total_count = IntegerField(label=u"可用次数", validators=[DataRequired()])
    expire_time = IntegerField(label=u"过期时间", validators=[DataRequired()])
    rate_limit = IntegerField(label=u"频率限制", validators=[DataRequired()])
    allow_bulk_detect = BooleanField(label=u"批量检测", validators=[DataRequired()])
    allow_excel_detect = BooleanField(label=u"Excel检测")
    allow_voip_detect = BooleanField(label=u"深度检测")
    allow_detail_display = BooleanField(label=u"显示字段")
    allow_vote_define = BooleanField(label=u"自定义权重")
    allow_data_push = BooleanField(label=u"黑名单写入")
    submit = SubmitField(label=u"创建")

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
        # rate_limit = self.rate_limit.data

        user = models.User(username=username, email=email,)
        user.password = password

        models.UserProfile(user=user, company_name=company_name)

        models.UserCount(user=user, ip_query_used_count=0,
                         ip_query_total_count=total_count,
                         ip_query_expire_time=expire_time)

        return True


class UpdateUserForm(Form):
    total_count = IntegerField(label=u"可用次数")
    expire_time = IntegerField(label=u"过期时间")
    rate_limit = IntegerField(label=u"频率限制")
    allow_bulk_detect = BooleanField(label=u"批量检测", validators=[DataRequired()])
    allow_excel_detect = BooleanField(label=u"Excel检测")
    allow_voip_detect = BooleanField(label=u"深度检测")
    allow_detail_display = BooleanField(label=u"显示字段")
    allow_vote_define = BooleanField(label=u"自定义权重")
    allow_data_push = BooleanField(label=u"黑名单写入")
    used_voip_count = BooleanField(label=u"已用voip次数")
    submit = SubmitField(label=u"创建")
