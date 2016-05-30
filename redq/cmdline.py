# -*- coding: utf-8 -*-

import os

# pylint: disable=import-error
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from redq.application import create_app


def main():
    u"""
    cmdline主入口
    :important: 需要先配置 APP_CONFIG环境变量
    """
    # init app first from environment
    config = os.environ.get('APP_CONFIG', 'redq.config.DevConfig')
    app = create_app(config)

    # init cmd manager and add config options
    manager = Manager(app)

    # add migrate command
    # pylint: disable=unused-variable
    migrate = Migrate(app, app.config.db)
    manager.add_command('db', MigrateCommand)

    # run the cmdline
    manager.run()
