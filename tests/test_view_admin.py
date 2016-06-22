# -*- coding: utf-8 -*-
# pylint: disable=no-member,import-error

# import json

import pytest
from flask import url_for
from flask_login import current_user

from redq import models


@pytest.fixture
def one_admin():
    admin = models.User(username='test1', is_admin=True,
                        status=models.USER_STATUS['normal'])
    admin.password = '123456'

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
        assert response.location.endswith('/admin/user_list')


class TestLoutout(object):

    def test_ok(self, client, one_admin):
        # login with the client
        assert current_user.is_anonymous()
        url = url_for('view.admin_login')
        data = {
            'username': one_admin.username,
            'password': '123456',
        }
        response = client.post(url, data=data)
        assert response.status_code == 302
        assert not current_user.is_anonymous()

        # login user
        url = url_for('view.admin_logout')

        response = client.post(url)

        assert response.status_code == 302
        assert response.location.endswith('/admin/login')


class TestCreateUser(object):

    def test_ok(self, client, one_admin):
        # login with the client
        assert current_user.is_anonymous()
        url = url_for('view.admin_login')
        data = {
            'username': one_admin.username,
            'password': '123456',
        }
        response = client.post(url, data=data)
        assert response.status_code == 302
        assert not current_user.is_anonymous()

        url = url_for('view.create_user')
        data = {
            'username': 'user1',
            'email': 'user1@bigsec.com',
            'company_name': 'bigsec',
            'total_count': -1,
            'expire_time': -1,
            'rate_limit': -1,
            'allow_bulk_detect': 'y',
            'allow_excel_detect': 'y',
            'allow_voip_detect': 'y',
            'allow_detail_display': 'y',
            'allow_vote_define': 'y',
            'allow_data_push': 'y',
        }

        response = client.post(url, data=data)

        assert response.status_code == 302
        pytest.fail("not correct")


def user_list(client):
    response = client.get(url_for('view.get_user_list'))

    assert response.status_code == 200


def user_detail(client):
    response = client.get(url_for('view.get_user_detail', uid=1))

    assert response.status_code == 200
