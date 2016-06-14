# -*- coding: utf-8 -*-

import json

from flask import request
from flask import redirect
from flask import render_template

from redq import rules
from redq import decorates
from redq.views import blue_app


@blue_app.route('/admin/user_list', methods=['GET', 'POST'])
def get_user_list():
    user_list = rules.get_user_info_list()

    return render_template('user_list.html', user_list=user_list)


@blue_app.route('/admin/user_list/<int:uid>')
def get_user_detail(uid):
    user = rules.get_user_info(uid)

    return json.dumps(user)


@blue_app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        import pytest;pytest.set_trace()
        username = request.form['username']
        password = request.form['password']

        if username == 'me':
            return redirect('/admin/index')

    return render_template('login.html')


@blue_app.route('/admin/index')
@decorates.admin_required
@decorates.auth.login_required
def index():
    return render_template('index.html')
