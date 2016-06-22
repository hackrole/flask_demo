# -*- coding: utf-8 -*-

from redq.application import app


celery = app.celery


@celery.task
def hello():
    return 'hello world'


@celery.task
def is_debug():
    return app.debug
