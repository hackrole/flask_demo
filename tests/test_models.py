# -*- coding: utf-8 -*-
# pylint: disable=no-member,redefined-outer-name,unused-argument

import pytest

from redq import models


@pytest.fixture()
def db(app):
    return app.config.db


@pytest.fixture(autouse=True)
def clean_db(db):
    for table in db.metadata.sorted_tables:
        db.engine.execute(table.delete())


def test_user(app, db):
    user = models.User()
    user.username = 'test1'
    user.email = 'test1@gmail.com'
    user.password = '123456'

    db.session.add(user)
    db.session.commit()
