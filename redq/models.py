# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods,import-error
# pylint: disable=too-many-instance-attributes,no-member

import uuid
import hashlib

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import validates
from werkzeug.security import generate_password_hash, check_password_hash


# db config
db = SQLAlchemy()


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


user_group = db.Table(
    'user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, doc="user id")
    username = db.Column(db.String(80), unique=True,
                         doc="username for login. need be unique")
    email = db.Column(db.String(128), unique=True, doc="email")
    mobile = db.Column(db.String(128), unique=True, doc="mobile")
    pwd = db.Column(db.String(128), doc="password")
    groups = db.relationship('Group', secondary="user_group",
                             backref=db.backref("users"), doc='group')
    permissions = db.relationship('UserPermission', backref="user",
                                  doc='permissions')
    is_admin = db.Column(db.Boolean, default=False, doc="admin flag")
    profile = db.relationship('UserProfile', backref='user',
                              doc="profile message")
    token = db.relationship('Token', backref='user', doc='token list')
    register_ip = db.Column(db.String(20), doc="register ip")
    register_time = db.Column(db.Integer, doc="register time")
    last_login_time = db.Column(db.Integer, doc="last login time")
    status = db.Column(db.Integer, default=USER_STATUS['normal'], doc="状态")

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

    @property
    def group_perms(self):
        perms = []
        for gp in self.groups:
            perm = [p.perm_name for p in gp.permissions]
            perms.extend(perm)

        return perms

    @property
    def all_perms(self):
        perms = [p.perm_name for p in self.permissions]
        return perms.extends(self.group_perms)

    @property
    def all_group(self):
        return [g.name for g in self.groups]


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, doc="group_id")
    name = db.Column(db.String(40), doc="name")
    permissions = db.relationship('GroupPermission',
                                  backref="group",
                                  doc='permissions')


class UserPermission(db.Model):
    __tablename__ = 'user_permission'

    id = db.Column(db.Integer, primary_key=True, doc="user permission id")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), doc="用户id")
    perm_name = db.Column(db.String(128), doc=u"权限名")


class GroupPermission(db.Model):
    __tablename__ = 'group_permission'

    id = db.Column(db.Integer, primary_key=True, doc='group perm id')
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), doc="group id")
    perm_name = db.Column(db.String(128), doc="权限名")


def _gen_token():
    gen = str(uuid.uuid4())
    return hashlib.sha1(gen).hexdigest()


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), doc='user id')
    token = db.Column(db.String(128), nullable=False,
                      default=_gen_token, unique=True, doc='token')


class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    id = db.Column(db.Integer, primary_key=True, doc="user profile id")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        doc="用户id")
    company_name = db.Column(db.String(128), doc=u"公司名")
    level = db.Column(db.Integer, doc=u"级别")
    register_ip = db.Column(db.String(64), doc=u"注册ip")
    last_login = db.Column(db.Integer, doc=u"注册时间戳")

    def __repr__(self):
        return '<User %r>' % self.username

    @validates('level')
    def validate_level(self, _, address):
        assert address in CUSTOMER_LEVEL.values()


class UserCount(db.Model):
    u"""用户计数"""
    __tablename__ = 'user_count'

    id = db.Column(db.Integer, primary_key=True, doc="user count id")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        doc="用户id")
    ip_query_used_count = db.Column(db.Integer, doc=u"已用查询次数")
    ip_query_total_count = db.Column(db.Integer, default=QUERY_COUNT_UNLIMIT,
                                     doc=u"总查询次数")
    ip_query_expire_time = db.Column(db.Integer, default=QUEYR_TIME_UNLIMIT,
                                     doc=u"查询过期时间")
