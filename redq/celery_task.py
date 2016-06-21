# -*- coding: utf-8 -*-

from redq.application import celery
from redq.cmdline import app


@celery.task
def hello():
    return 'hello world'


@celery.task
def is_debug():
    return app.debug
