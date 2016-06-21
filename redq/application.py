# -*- coding: utf-8 -*-
# pylint: disable=import-error, global-statement

import importlib

from flask import Flask
from celery import Celery
from flask_login import LoginManager

from redq import rules
from redq.models import db
from redq.views import blue_app
from redq.views import hello


# gloabl celery obj
celery = None


def dy_load_attr(attr_path):
    u"""
    动态加载模块的attr. example:
        >>> dy_load_att('redq.config.DevConfig')
    """
    mod_name, attr_name = attr_path.rsplit('.', 1)
    mod = importlib.import_module(mod_name)

    return getattr(mod, attr_name)


def create_app(config):
    app = Flask(__name__)
    # 初始化配置和app
    config_cls = dy_load_attr(config)
    app.config.from_object(config_cls)

    # import models define
    db.init_app(app)
    app.config.db = db

    # deal celery
    # you need import views local cause this!!!
    global celery
    celery = make_celery(app)

    # add login support
    login_manager = LoginManager()
    login_manager.session_protected = "strong"
    login_manager.login_view = 'view.admin_login'
    login_manager.user_callback = rules.get_user_by_id
    login_manager.init_app(app)

    # register url route
    from redq.views import login as _
    from redq.views import admin as _
    app.register_blueprint(blue_app)
    app.add_url_rule('/hello', 'hello', hello.hello)

    return app


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    # deal app context with celery
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kw):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kw)

    celery.Task = ContextTask
    return celery
