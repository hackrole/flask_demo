# -*- coding: utf-8 -*-
# pylint: disable=import-error

import os

import pytest
from pony import orm



@pytest.fixture(scope="session", autouse=True)
def app(request):
    # use env to control app init.
    os.environ['APP_CONFIG'] = 'redq.config.TestConfig'
    from redq import application

    app = application.app

    # create app context
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.yield_fixture(autouse=True)
def transaction():
    with orm.db_session:
        yield
        orm.rollback()
