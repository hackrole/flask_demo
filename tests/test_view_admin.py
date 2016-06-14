# -*- coding: utf-8 -*-
# pylint: disable=no-member

# import json

import pytest
from flask import url_for

# from redq import models


@pytest.fixture
def two_user_with_profile():
    pass


def test_user_list(client):
    response = client.get(url_for('view.get_user_list'))

    assert response.status_code == 200


def test_user_detail(client):
    response = client.get(url_for('view.get_user_detail', uid=1))

    assert response.status_code == 200
