# -*- coding: utf-8 -*-
# pylint: disable=no-member

# import json

import pytest
from flask import url_for

from redq import models


def login(client, user):
    url = url_for('view.admin_login')
    data = {
        'username': user.username,
        'password': '123456',
    }
    response = client.post(url, data=data)
    assert response.status_code == 302


@pytest.fixture
def one_admin(request):
    db = models.db

    admin = models.User(username='test1', is_admin=True,
                        status=models.USER_STATUS['normal'])
    admin.password = '123456'

    db.session.add(admin)
    db.session.commit()

    def tear():
        db.session.delete(admin)
        db.session.commit()

    request.addfinalizer(tear)
    return admin


class TestAdminLogin(object):

    def test_login_page(self, client):
        response = client.get(url_for('view.admin_login'))

        assert response.status_code == 200

        assert 'login form' in response.data
        assert 'id="username"' in response.data
        assert 'id="password"' in response.data
        assert '<ul class="error">' not in response.data

    def test_login_form_fail(self, client):
        url = url_for('view.admin_login')
        data = {
            'username': 'not-me',
            'password': '123456',
        }

        response = client.post(url, data=data)

        assert response.status_code == 200
        assert 'login form' in response.data
        assert 'id="username"' in response.data
        assert 'id="password"' in response.data
        assert 'class="errors"' in response.data

    def test_login_form_ok(self, client, one_admin):
        url = url_for('view.admin_login')
        data = {
            'username': one_admin.username,
            'password': '123456',
        }

        response = client.post(url, data=data)

        assert response.status_code == 302
        assert response.location.endswith('/admin/index')


class TestLoutout(object):

    def test_ok(self, client, one_admin):
        # login user
        url = url_for('view.admin_logout')

        response = client.post(url)

        assert response.status_code == 302
        assert response.location.endswith('/admin/login')


def user_list(client):
    response = client.get(url_for('view.get_user_list'))

    assert response.status_code == 200


def user_detail(client):
    response = client.get(url_for('view.get_user_detail', uid=1))

    assert response.status_code == 200
