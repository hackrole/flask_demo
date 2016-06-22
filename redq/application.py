# -*- coding: utf-8 -*-
# pylint: disable=import-error, global-statement

import os
import importlib

from flask import Flask
from celery import Celery
from flask_login import LoginManager

from redq import rules
from redq.models import db
from redq.views import blue_app
from redq.views import hello


def dy_load_attr(attr_path):
    u"""
    动态加载模块的attr. example:
        >>> dy_load_att('redq.config.DevConfig')
    """
    mod_name, attr_name = attr_path.rsplit('.', 1)
    mod = importlib.import_module(mod_name)

    return getattr(mod, attr_name)


def create_app():
    # get config from env
    config = os.environ.get('APP_CONFIG', 'redq.config.DevConfig')

    app = Flask(__name__)
    # 初始化配置和app
    config_cls = dy_load_attr(config)
    app.config.from_object(config_cls)

    # import models define
    bind_pony_db(app, db)
    app.config.db = db

    # deal celery
    # you need import views local cause this!!!
    celery = make_celery(app)
    app.celery = celery

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


def bind_pony_db(app, db):
    u""" bind pony db """
    config = app.config
    create_db = config.get('PONY_CREATE_DB', False)
    create_tables = config.get('PONY_CREATE_TABLES', False)

    pony_type = config.get('PONY_DATABASE_TYPE')
    if pony_type == 'sqlite':
        sqlite_path = config.get('PONY_SQLITE_FILE')
        db.bind(pony_type, sqlite_path, create_db=create_db)
    elif pony_type == 'mysql':
        mysql_host = config.get('PONY_MYSQL_HOST')
        mysql_port = config.get('PONY_MYSQL_PORT')
        mysql_user = config.get('PONY_MYSQL_USER')
        mysql_pwd = config.get("PONY_MYSQL_PASSWORD")
        mysql_db = config.get('PONY_MYSQL_DB')
        db.bind(pony_type, host=mysql_host, port=mysql_port,
                user=mysql_user, passwd=mysql_pwd, db=mysql_db,
                create_db=create_db)

    db.generate_mapping(create_tables=create_tables)
    return db


app = create_app()
