# -*- coding: utf-8 -*-

import pytest
from redq import application


@pytest.fixture
def app():
    return application.create_app('testing')
