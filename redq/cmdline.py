# -*- coding: utf-8 -*-

import os

# pylint: disable=import-error
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from redq.application import create_app, db


config = os.environ.get('APP_CONFIG', 'redq.config.DevConfig')
app = create_app(config)
manager = Manager(app)


def _make_context():
    return dict(app=app, db=db)

# add migrate cmd
Migrate(app, db)
manager.add_command('db', MigrateCommand)

# add shell cmd
manager.add_command('shell', Shell(make_context=_make_context))
