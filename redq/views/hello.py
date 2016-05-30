# -*- coding: utf-8 -*-

from flask import request, session


def hello():
    print request
    print session
    return 'hello world'
