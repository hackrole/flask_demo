# -*- coding: utf-8 -*-
# pylint: disable=unused-argument,no-member

import json

import pytest
from flask import url_for

from redq import models


@pytest.fixture
def one_user(session, request):
    user = models.User()
    user.username = 'test-1'
    user.password = '123456'
    session.add(user)
    session.commit()

    def teardown():
        session.delete(user)
        session.commit()

    request.addfinalizer(teardown)
    return user


@pytest.fixture
def one_token(session, one_user, request):
    token = models.Token()
    token.user = one_user
    session.add(token)
    session.commit()

    def teardown():
        session.delete(token)
        session.commit()

    request.addfinalizer(teardown)
    return token


def test_hello(client):
    response = client.get(url_for('hello'))

    assert response.status_code == 200
    assert response.data == 'hello world'


class TestLogin(object):

    def test_login_get_405(self, client):
        response = client.get(url_for('view.login'))

        assert response.status_code == 405

    def test_login_param_required(self, client):
        data = json.dumps({'username': 'test-me'})
        response = client.post(url_for('view.login'), data=data)

        assert response.status_code == 400
        assert response.data == 'params required'

    def test_login_username_not_exists_401(self, client):
        headers = {'content-type': 'application/json'}
        data = json.dumps({'username': 'not-exists', 'password': '123456'})

        response = client.post(url_for('view.login'), data=data, headers=headers)

        assert response.status_code == 401

    def test_login_password_error_401(self, client):
        headers = {'content-type': 'application/json'}
        data = json.dumps({'username': 'test1', 'password': '123456'})

        response = client.post(url_for('view.login'), data=data, headers=headers)

        assert response.status_code == 401

    # pylint: disable=unused-argument
    def test_login_ok(self, client, one_user):
        headers = {'content-type': 'application/json'}
        data = json.dumps({'username': 'test-1', 'password': '123456'})

        response = client.post(url_for('view.login'), data=data, headers=headers)

        assert response.status_code == 200
        dut = response.json

        assert 'token' in dut
        assert len(dut['token']) == 40


class TestLogout(object):

    def test_param_required(self, client, one_user, one_token):
        headers = {'content-type': 'application/json'}
        data = json.dumps({})

        response = client.post(url_for('view.logout'), data=data, headers=headers)

        assert response.status_code == 400

    def test_token_404(self, client, one_user, one_token):
        headers = {'content-type': 'application/json'}
        data = json.dumps({'token': 'no-token'})

        response = client.post(url_for('view.logout'), data=data, headers=headers)

        assert response.status_code == 404

    def test_token_204(self, client, one_user, one_token):
        headers = {'content-type': 'application/json'}
        data = json.dumps({'token': one_token.token})

        response = client.post(url_for('view.logout'), data=data, headers=headers)

        assert response.status_code == 204
        assert models.Token.query.count() == 0
