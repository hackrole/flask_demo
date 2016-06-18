# -*- coding: utf-8 -*-
# pylint: disable=unused-argument,no-member,import-error

import functools

from flask import g
from flask import url_for
from flask import redirect
from flask_login import current_user
from flask_httpauth import HTTPTokenAuth

from redq import models


auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    token_obj = models.Token.query.filter(token=token).first()

    if token_obj is None:
        return False

    g.user = token_obj.user
    return True


def api_admin_required(func):

    @functools.wraps(func)
    def _wrap(*args, **kw):
        if not g.user.is_admin:
            return "denied", 403

        return func(*args, **kw)

    return _wrap


def admin_required(func):

    @functools.wraps(func)
    def _wrap(*args, **kw):
        if not current_user.is_admin:
            return redirect(url_for('views.admin_login'))

        return func(*args, **kw)

    return _wrap


def perm_required(perms):
    u"""权限检查"""

    def _wrap(func):

        @functools.wraps(func)
        def __wrap(*args, **kw):
            pass

        return __wrap

    return _wrap
