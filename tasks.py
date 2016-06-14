# -*- coding: utf-8 -*-

import os
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
