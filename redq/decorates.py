# -*- coding: utf-8 -*-
# pylint: disable=unused-argument

import functools


def login_required(func):

    @functools.wraps(func)
    def _wrap(*args, **kw):
        pass

    return _wrap


def admin_required(func):

    @functools.wraps(func)
    def _wrap(*args, **kw):
        pass

    return _wrap


def perm_required(perms):
    u"""权限检查"""

    def _wrap(func):

        @functools.wraps(func)
        def __wrap(*args, **kw):
            pass

        return __wrap

    return _wrap
