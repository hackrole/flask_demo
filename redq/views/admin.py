# -*- coding: utf-8 -*-

import json

from redq import rules
from redq.views import blue_app


@blue_app.route('/admin/user_list', methods=['GET', 'POST'])
def get_user_list():
    user_list = rules.get_user_info_list()

    return json.dumps(user_list)


@blue_app.route('/admin/user_list/<int:uid>')
def get_user_detail(uid):
    user = rules.get_user_info(uid)

    return json.dumps(user)
