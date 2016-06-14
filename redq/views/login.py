# -*- coding: utf-8 -*-
# pylint: disable=bare-except

import json

from flask import abort
from flask import request
# from flask import session
from flask.views import MethodView

from redq import models
from redq import rules
from redq import renderer
from redq.views import blue_app


@blue_app.route('/login', methods=['POST'])
def login():
    data = request.json
    try:
        username = data['username']
        password = data['password']
    except:
        return "params required", 400

    user = rules.auth(username, password)
    token_obj = rules.generate_token(user)

    return json.dumps({'token': token_obj.token})


@blue_app.route('/logout', methods=['POST'])
def logout():
    data = request.json

    try:
        token = data['token']
    except KeyError:
        abort(400, "params required")

    rules.del_token_or_404(token)
    return 'no-content', 204


class TokenListView(MethodView):
    methods = ['get', 'post', 'head', 'option']
    decorators = ['login_required']

    def get(self):
        pass

    def post(self):
        pass


class TokenView(MethodView):
    methods = ['get', 'delete', 'head', 'option']
    decorators = ['login_required']

    def get(self, uid):
        pass

    def delete(self, uid):
        pass


def register():
    mobile = request.args.get('mobile')
    pwd = request.args.get('pwd')

    is_registered = rules.is_registered(mobile)

    return 'is_register: %s, pwd: %s' % (is_registered, pwd)


def active_register():
    pass


class UserListView(MethodView):
    methods = ['get', 'head', 'post']
    decorators = ['admin_required']

    def get(self):
        user_list = rules.get_user_list()

        return renderer.render_user_list(user_list)


    def post(self):
        data = request.data
        user = models.User(**data)

        try:
            models.db.session.add(user)
            models.db.session.commit()
        # pylint: disable=broad-except
        except Exception:
            # pylint: disable=no-member
            models.db.session.rollback()
            abort(400, 'save user error')

        return renderer.render_user(user)


class UserView(MethodView):
    methods = ['get', 'post']
    decorators = ['admin_required']

    def get(self, uid):
        pass

    def post(self, uid):
        pass

    def put(self, uid):
        pass
