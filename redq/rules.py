# -*- coding: utf-8 -*-
# pylint: disable=no-member

from flask import abort

from redq import utils
from redq import models


_SESSION = models.db.session


def is_registered(mobile):
    u"""检测手机号是否已注册"""
    user = models.User.query.filter_by(mobile=mobile).first()

    if user is not None:
        return True

    return False


def generate_token(user):
    u"""登录token,允许多点登录"""
    token = models.Token(user_id=user.id)
    _SESSION.add(token)
    _SESSION.commit()

    return token


def del_token_or_404(token):
    u"""通过token获取token_obj"""
    token_obj = models.Token.query.filter_by(token=token).first()
    if token_obj is None:
        abort(404, "not found")

    _SESSION.delete(token_obj)
    _SESSION.commit()

    return True


def auth(username, password):
    u""" 验证登录用户 """
    user = models.User.query.filter_by(username=username).first()
    if user is None:
        abort(401, "auth failed")

    hash_pwd = utils.hash_pwd(password)
    if user.pwd != hash_pwd:
        abort(401, "auth failed")

    return user


def get_user_list():
    u""" 获取用户列表 """
    user_list = models.User.query.filter(is_admin=False).all()

    return user_list


def get_user_info_list():
    u"""获取用户列表，包含用户详细信息"""
    U = models.User
    UP = models.UserProfile

    user_list = U.query.join(UP, UP.user_id == U.id).filter(U.is_admin is False).all()

    return user_list


def get_user_info(uid):
    u"""获取用户详情"""
    U = models.User
    UP = models.UserProfile

    user_list = U.query.join(UP, UP.user_id == U.id).filter(
        U.is_admin is False).filter(U.id == uid).first()

    return user_list


def get_current_user():
    u"""获取当前用户，类tornado:get_current_user"""
    pass
