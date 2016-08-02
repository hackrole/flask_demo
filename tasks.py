# -*- coding: utf-8 -*-
# pylint: disable=import-error

import os

from pony import orm
from invoke import task, run


@task
def penv():
    u"""set pip_conf env"""
    base_dir = os.path.dirname(os.path.realpath(__file__))
    pip_conf_fp = os.path.join(base_dir, 'pip.conf')

    os.environ['PIP_CONFIG_FILE'] = pip_conf_fp


@task(penv)
def dep(dev=True):
    u"""install pip depedance"""
    run("pip install -r requirements.txt")

    if dev is True:
        run("pip install -r dev_requirements.txt")


@task
def build_bower():
    u"""build bower deps"""
    run("mkdir -p redq/static/vender/bootstrap")
    run("mkdir -p redq/static/vender/jquery")

    # cp bootstrap
    run('cp -r bower_components/bootstrap/dist/* redq/static/vender/bootstrap/')
    # cp jquery
    run('cp -r bower_components/jquery/dist/* redq/static/vender/jquery')


@task
def clean_db():
    u"""remove dev db"""
    run("rm tmp/data-dev.sqlite")


@task
def create_db():
    u"""create dev db"""
    run("python manage.py create_tables")


@task(pre=[clean_db, create_db])
def db():
    u"""recreate dev db"""
    pass


@task
def sqlall(fp="tmp/create_tables.sql"):
    u""" generate create table schema """
    run("python manage.py sqlall -f %s" % fp)
    run("cat %s" % fp)


@task
def fixture():
    from redq import rules
    from redq import application

    with orm.db_session:
        for i in range(10):
            rules.create_mock_user(index=i)

    run("python manage.py create_admin admin 123456")
