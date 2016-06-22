# -*- coding: utf-8 -*-
# pylint: disable=import-error

import time
import uuid
import hashlib

from pony import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db = orm.Database()


# 用户状态
USER_STATUS = {
    # 禁用
    'disable': -2,
    # 未激活
    'deactive': -1,
    # 正常
    'normal': 1,
}

# 用户级别
CUSTOMER_LEVEL = {
    # 测试
    "test": 1,
    # 普通
    "normal": 2,
    # 公司
    "company": 3,
    # vip
    "vip": 4,
}

QUERY_COUNT_UNLIMIT = -1
QUEYR_TIME_UNLIMIT = -1

# 权限
PERMISSON_NAMES = [
    ('online_query', u"实时检测"),
    ('online_bluk_detect', u"在线批量检测"),
    ('display_detail', u"显示详细字段"),
    ('offline_query', u"手机实时检测"),
    ("offline_bluk_detect", u"离线批量检测")
]


class User(db.Entity, UserMixin):

    _table_ = 'user'

    username = orm.Required(str, 80, unique=True)
    email = orm.Optional(str, 128)
    mobile = orm.Optional(str, 20)
    pwd = orm.Optional(str, 128)
    permissions = orm.Set('Permission')
    is_admin = orm.Required(bool, default=False)
    profile = orm.Optional('UserProfile', cascade_delete=True)
    api_history = orm.Optional('QueryHistory', cascade_delete=True)
    token = orm.Set('Token', cascade_delete=True)
    status = orm.Required(int, default=USER_STATUS['deactive'])

    def __repr__(self):
        return '<User: %s>' % self.username

    def is_active(self):
        return self.status == USER_STATUS['normal']

    def get_id(self):
        return self.id

    @property
    def password(self):
        raise Exception("not allow for this.")

    @password.setter
    def password(self, password):
        self.pwd = generate_password_hash(password)

    def verify_password(self, password):
        u""" 校验密码 """
        return check_password_hash(self.pwd, password)


class Permission(db.Entity):
    _table_ = 'permission'

    user = orm.Set('User')
    name = orm.Required(str, 40, unique=True)


class UserProfile(db.Entity):

    _table_ = 'user_profile'

    user = orm.Required(User)
    level = orm.Required(int, size=8, default=1)
    company_name = orm.Required(str, 40)
    current_query_count = orm.Required(int, size=8, default=-1)
    query_timeout = orm.Required(int, size=8, default=-1)
    register_ip = orm.Optional(str, 40)
    last_login = orm.Optional(int)


class QueryHistory(db.Entity):
    _table = 'api_query_history'

    user = orm.Required(User)
    query_time = orm.Required(int, default=time.time)


def _gen_token():
    gen = str(uuid.uuid4())
    return hashlib.sha1(gen).hexdigest()


class Token(db.Entity):

    _tabel_ = 'token'

    user = orm.Required(User)
    token = orm.Required(str, 128, default=_gen_token)
