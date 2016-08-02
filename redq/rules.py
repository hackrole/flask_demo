# -*- coding: utf-8 -*-
# pylint: disable=no-member,import-error,unsubscriptable-object

from pony import orm
from flask import abort

from redq import models



@orm.db_session
def is_registered(mobile):
    u"""检测手机号是否已注册"""
    user = models.User.get(mobile=mobile)

    if user is not None:
        return True

    return False


@orm.db_session
def generate_token(user):
    u"""登录token,允许多点登录"""
    token = models.Token(user=user)

    return token


@orm.db_session
def del_token_or_404(token):
    u"""通过token获取token_obj"""
    token_obj = models.Token.get(token=token)
    if token_obj is None:
        abort(404, "not found")

    token_obj.delete()

    return True


@orm.db_session
def auth(username, password):
    u""" 验证登录用户 """
    user = models.User.get(username=username)
    if user is None:
        abort(401, "auth failed")

    if not user.verify_password(password):
        abort(401, "auth failed")

    return user


@orm.db_session
def get_user_list():
    u""" 获取用户列表 """
    user_list = models.User.select(is_admin=False)[:]

    return user_list


@orm.db_session
def get_user_by_id(user_id):
    u""" 通过uid获取user """
    user_id = int(user_id)
    try:
        user = models.User[user_id]
    except orm.ObjectNotFound:
        user = None

    return user


@orm.db_session
def get_user_info_list():
    u"""获取用户列表，包含用户详细信息"""
    user_list = orm.select(u for u in models.User if u.is_admin is False)[:]

    return user_list


@orm.db_session
def get_user_info(uid):
    u"""获取用户详情"""
    user_list = models.User.get[uid]

    return user_list


def get_current_user():
    u"""获取当前用户，类tornado:get_current_user"""
    pass


def create_mock_user(index=None, username=None):
    u"""创建mock user, 方便测试和调试用"""
    if index is not None:
        username = 'user_%s' % index

    user = models.User(username=username, status=models.USER_STATUS['normal'])
    user.password = '123456'

    models.UserProfile(user=user, company_name='bigsec')

    return user


@orm.db_session
def create_user_perm(user, perm_name, value):
    u"""创建用户权限"""
    if not value:
        return

    models.UserPermission(user=user, name=perm_name)


@orm.db_session
def toggle_active(user, is_active):
    if is_active:
        user.status = models.USER_STATUS['normal']
    else:
        user.status = models.USER_STATUS['disable']

    return user
