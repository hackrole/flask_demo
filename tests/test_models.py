# -*- coding: utf-8 -*-
# pylint: disable=no-member,redefined-outer-name,unused-argument,import-error

# import pytest
from pony import orm

# from redq import models
from redq import pony_models


# @pytest.fixture()
# def db(app):
#     return app.config.db


# @pytest.fixture(autouse=True)
# def clean_db(db):
#     for table in db.metadata.sorted_tables:
#         db.engine.execute(table.delete())


# def test_user(app, db):
#     user = models.User()
#     user.username = 'test1'
#     user.email = 'test1@gmail.com'
#     user.password = '123456'

#     db.session.add(user)
#     db.session.commit()


@orm.db_session
def test_pony_model():
    u = pony_models.User(username='user1', email='user1@bigsec.com',
                         mobile='183214123')
    u.password = '123456'
    pony_models.UserProfile(user=u, level=1, company_name='bigsec.com')
    orm.commit()

    us = orm.select(u for u in pony_models.User)[:]

    us.show()

    for i in range(2, 20):
        un = 'user' + str(i)
        u = pony_models.User(username=un, email='user1@bigsec.com',
                             mobile='183214123')
        u.password = '123456'
        pony_models.UserProfile(user=u, level=1, company_name='bigsec.com')
    orm.commit()

    us = pony_models.User.select().page(1, pagesize=2)
    us.show()

    us = pony_models.User.select().page(2, pagesize=5)
    us.show()
    orm.show(us[2].profile)
    print us[2].profile.company_name
