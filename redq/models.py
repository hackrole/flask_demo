# -*- coding: utf-8 -*-

from flask import current_app


# db config
db = current_app.config.db


# 用户级别
CUSTOMER_LEVEL = [
    (1, u"测试"),
    (2, u"普通"),
    (3, u"企业"),
    (4, u"VIP"),
]

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


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, doc="user id")
    username = db.Column(db.String(80), unique=True,
                         doc="username for login. need be unique")
    email = db.Column(db.String(128), unique=True, doc="email")
    mobile = db.Column(db.String(128), unique=True, doc="mobile")
    company_name = db.Column(db.String(128, doc=u"公司名"))
    level = db.Column(db.ChoiceType(CUSTOMER_LEVEL), doc=u"级别")
    register_ip = db.Column(db.String(64), doc=u"注册ip")
    last_login = db.Column(db.Intger, doc=u"注册时间戳")

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class UserCount(db.Model):
    u"""用户计数"""
    user = db.Column(db.String)
    ip_query_used_count = db.Column(db.Intger, doc=u"已用查询次数")
    ip_query_total_count = db.Column(db.Integer, default=QUERY_COUNT_UNLIMIT,
                                     doc=u"总查询次数")
    ip_query_expire_time = db.Column(db.Integer, default=QUEYR_TIME_UNLIMIT,
                                     doc=u"查询过期时间")


class UserPermission(db.Model):
    user = db.Column(db.String(128), doc="用户id")
    perm_name = db.Column(db.String(128), choices=PERMISSON_NAMES,
                          doc=u"权限名")
    perm_value = db.Column(db.Boolean, default=False, doc=u"权限值")
