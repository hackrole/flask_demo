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
