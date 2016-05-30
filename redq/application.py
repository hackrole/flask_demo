# -*- coding: utf-8 -*-

import importlib

from flask import Flask

from redq.views import hello


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
    app = config_cls.init_app(app)

    # register url route
    app.add_url_rule('/hello', 'hello', hello.hello)

    return app
