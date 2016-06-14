# -*- coding: utf-8 -*-

import pytest
from selenium import webdriver


@pytest.fixture
def browser(request):
    driver = webdriver.Firefox()

    request.addfinalizer(driver.quit)

    return driver


def fts_admin_login(browserm, app):
    pass


def test_um_api(app):
    pass
