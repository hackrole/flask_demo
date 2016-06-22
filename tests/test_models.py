# -*- coding: utf-8 -*-
# pylint: disable=no-member,redefined-outer-name,unused-argument,import-error
# pylint: disable=unsubscriptable-object

import pytest
from pony import orm

from redq import rules
from redq import models


@pytest.yield_fixture
def two_user():
    users = []
    for i in range(2):
        user = rules.create_mock_user(index=i)
        users.append(user)

    orm.commit()
    yield users

    for user in users:
        user.delete()

    orm.commit()


class TestPonyModel(object):

    def test_get_by_id(self, two_user):
        first, second = two_user

        assert models.User[first.id].username == first.username
        assert models.User[second.id].username == second.username

        assert models.User.get(username=first.username) == first
        assert models.User.get(username=second.username) == second

        assert models.User.get(username='not-exists') is None

        start_err_msg = "Multiple objects were found."
        with pytest.raises(orm.MultipleObjectsFoundError) as exc_info:
            models.User.get(is_admin=False)

        assert exc_info.value.message.startswith(start_err_msg)

    def test_select_and_filter(self, two_user):
        first, second = two_user

        assert list(models.User.select()) == [first, second]
        assert list(models.User.select().order_by(orm.desc(models.User.id))) == [second, first]
        assert models.User.select().first() == first
        assert models.User.select().filter(username=second.username).first() == second

        lmb = lambda u: u.is_admin is False and u.username == second.username
        assert models.User.select(lmb).first() == second
        lcom = (u for u in models.User if u.is_admin is False and u.username == second.username)
        assert orm.select(lcom).first() == second

    def test_page(self, two_user):
        first, second = two_user

        assert models.User.select().page(1) == two_user
        assert models.User.select().page(1, pagesize=1) == [first]
        assert models.User.select().page(2, pagesize=1) == [second]
        assert models.User.select().page(3, pagesize=1) == []
        assert models.User.select().page(3, pagesize=2) == []

        err_msg = "Parameter 'start' of slice object cannot be negative"
        with pytest.raises(TypeError) as exec_info:
            models.User.select().page(0, pagesize=2)
        assert exec_info.value.message == err_msg

        with pytest.raises(TypeError) as exec_info:
            models.User.select().page(-1, pagesize=2)
        assert exec_info.value.message == err_msg

    def test_relation(self, two_user):
        first, second = two_user

        assert first.profile.company_name == 'bigsec'
        assert second.permissions.count() == 0
        assert hasattr(second.permissions, 'add')
        assert hasattr(second.permissions, 'select')
        assert hasattr(second.permissions, 'filter')
        assert hasattr(second.permissions, 'page')


class TestUser(object):

    def test_password_get_set(self):
        pass

    def test_password_check(self):
        pass

    def test_active(self):
        pass

    def test_delete_cacs_profile(self):
        pass
