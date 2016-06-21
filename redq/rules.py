# -*- coding: utf-8 -*-
# pylint: disable=no-member,import-error

from pony import orm
from flask import abort

from redq import pony_models as models



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
    token = models.Token(user_id=user.id)

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

    if not user.check_password_hash(password):
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
    import pytest;pytest.set_trace()
    user_id = int(user_id)
    return models.User.get[user_id]


@orm.db_session
def get_user_info_list():
    u"""获取用户列表，包含用户详细信息"""
    user_list = models.User.select(is_admin=False)[:]

    return user_list


def get_user_info(uid):
    u"""获取用户详情"""
    user_list = models.User.get(id=uid)

    return user_list


def get_current_user():
    u"""获取当前用户，类tornado:get_current_user"""
    pass
