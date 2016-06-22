# -*- coding: utf-8 -*-
# pylint: disable=no-init,too-few-public-methods

import os


basedir = os.path.abspath(os.path.dirname(__file__))
updir = os.path.dirname(basedir)


class BaseConfig(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    # pony orm config
    PONY_CREATE_DB = True
    PONY_CREATE_TABLES = True
    PONY_DATABASE_TYPE = 'sqlite'
    PONY_SQLITE_FILE = ':memory:'

    # celery config
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    # mail config
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')


class DevConfig(BaseConfig):
    DEBUG = True
    TESTING = False

    # pony orm config
    PONY_SQLITE_FILE = os.path.join(updir, 'tmp/data-dev.sqlite')


class TestConfig(BaseConfig):
    DEBUG = False
    TESTING = True

    # disable csrf token check
    WTF_CSRF_ENABLED = False


class ProdConfig(BaseConfig):
    DEBUG = False
    TESTING = False

    # todo pony orm config
