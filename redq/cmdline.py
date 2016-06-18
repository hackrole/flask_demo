# -*- coding: utf-8 -*-
# pylint: disable=broad-except,no-member

import os
import logging
import traceback

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

# add create admin user command
@manager.command
@manager.option('-n', '--name', help="admin username")
@manager.option('-p', '--password', help="password")
def create_admin(name, password):
    from redq.models import User, USER_STATUS

    admin = User(username=name, is_admin=True, status=USER_STATUS['normal'])
    admin.password = password

    try:
        db.session.add(admin)
        db.session.commit()
    except Exception:
        # rollback
        db.session.rollback()
        # logging error
        err_msg = traceback.format_exc()
        logging.warning(err_msg)


