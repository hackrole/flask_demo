# -*- coding: utf-8 -*-


def render_user_list(user_list):
    result = [render_user(user) for user in user_list]

    return {
        'page': 'no-page',
        'total': len(user_list),
        'data': result
    }


def render_user(user):
    return {
        'id': user.id,
        'username': user.name,
        'email': user.email,
        'mobile': user.mobile,
        'level': user.profile.level,
        'register_ip': user.register_ip,
        'register_time': user.register_time,
        'last_login_time': user.last_login_time,
        'status': user.status,
        'perms': user.all_perms,
        'group': user.all_group,
    }
