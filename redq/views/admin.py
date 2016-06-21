# -*- coding: utf-8 -*-
# pylint: disable=import-error

import json

from flask import url_for
# from flask import request
from flask import redirect
from flask import render_template
from flask_login import logout_user, login_required

from redq import rules
from redq import forms
from redq import decorates
from redq.views import blue_app


@blue_app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('view.get_user_list'))

    return render_template('login.html', form=form)


@blue_app.route('/admin/logout', methods=['POST'])
@login_required
def admin_logout():
    u""" admin登出 """
    logout_user()
    return redirect(url_for('view.admin_login'))


@blue_app.route('/admin/index')
@login_required
def index():
    return render_template('index.html')


@blue_app.route('/admin/user_list', methods=['GET', 'POST'])
@login_required
def get_user_list():
    user_list = rules.get_user_info_list()

    return render_template('user_list.html', user_list=user_list)


@blue_app.route('/admin/user_list/<int:uid>')
@decorates.admin_required
@login_required
def get_user_detail(uid):
    user = rules.get_user_info(uid)

    return json.dumps(user)


@blue_app.route('/admin/create_user', methods=['GET', 'POST'])
@decorates.admin_required
@login_required
def create_user():
    import pytest;pytest.set_trace()
    form = forms.CreateUserForm()
    if form.validate_on_submit():
        return redirect(url_for('view.get_user_list'))

    return render_template('create_user.html', form=form)


@blue_app.route('/admin/update_user', methods=['GET', 'POST'])
@decorates.admin_required
@login_required
def update_user():
    form = forms.UpdateUserForm()
    if form.validate_on_submit():
        # form.save()
        return redirect(url_for('admin.get_user_list'))

    return render_template('update_user.html', form=form)


@blue_app.route('/admin/active_user', methods=['POST'])
@decorates.admin_required
@login_required
def active_user():
    pass
