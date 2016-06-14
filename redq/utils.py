# -*- coding: utf-8 -*-

import uuid
import hashlib


def hash_pwd(password):
    u""" 密码hash """
    hash_obj = hashlib.sha1(password)
    return hash_obj.hexdigest()


def generate_token():
    u""" 生成唯一token """
    return str(uuid.uuid4())
