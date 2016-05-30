# -*- coding: utf-8 -*-

import pytest

from redq import models


db = models.db


def test_user(app):
    user = models.User('hello', 'hello@mail.com')
    pytest.set_trace()
    db.session.add(user)
    db.session.commit()
