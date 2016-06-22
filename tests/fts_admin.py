# -*- coding: utf-8 -*-

import pytest
from flask import url_for

from redq import models


@pytest.fixture
def one_admin():
    admin = models.User(username='admin1', is_admin=True,
                        status=models.USER_STATUS['normal'])
    admin.password = '123456'

    return admin


@pytest.mark.usefixtures('live_server')
def test_login(browser):
    u""" test admin login with fts """
    login_url = url_for('view.admin_login', _external=True)
    browser.visit(login_url)

    assert browser.is_text_present('login form')

    browser.fill('username', 'error')
    browser.fill('password', 'error')
    browser.find_by_id('submit').click()
