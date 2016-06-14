# -*- coding: utf-8 -*-

import pytest

from redq import application
from redq.models import db as _db


@pytest.fixture(scope="session")
def app(request):
    app = application.create_app('redq.config.TestConfig')

    # create app context
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="function", autouse=True)
def db(app, request):

    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """ create a new database session for a test."""
    session = db.session

    def teardown():
        session.rollback()
        session.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
