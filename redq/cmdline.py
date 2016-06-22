# -*- coding: utf-8 -*-
# pylint: disable=broad-except,import-error

import os

from pony import orm
from flask_script import Manager, Shell

from redq.application import app, db


manager = Manager(app)

# add shell cmd
def _make_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=_make_context))

# add create admin user command
@manager.command
@manager.option('-n', '--name', help="admin username")
@manager.option('-p', '--password', help="password")
def create_admin(name, password):
    from redq.models import User, USER_STATUS

    with orm.db_session:
        admin = User(username=name, is_admin=True, status=USER_STATUS['normal'])
        admin.password = password
        orm.commit()


@manager.command
def create_tables():
    u"""create pony tables"""
    db.create_tables()


@manager.command
def drop_tables():
    u"""drop pony tables"""
    db.drop_tables()
