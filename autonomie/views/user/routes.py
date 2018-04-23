# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os


USER_URL = "/users"
USER_ITEM_URL = os.path.join(USER_URL, '{id}')
USER_MYACCOUNT_URL = os.path.join(USER_ITEM_URL, 'myaccount')
USER_ITEM_EDIT_URL = os.path.join(USER_ITEM_URL, 'edit')
USER_LOGIN_URL = os.path.join(USER_ITEM_URL, "login")
USER_LOGIN_EDIT_URL = os.path.join(USER_LOGIN_URL, "edit")
USER_LOGIN_SET_PASSWORD_URL = os.path.join(USER_LOGIN_URL, "set_password")

LOGIN_URL = "/logins"
LOGIN_ITEM_URL = os.path.join(LOGIN_URL, "{id}")
LOGIN_EDIT_URL = os.path.join(LOGIN_ITEM_URL, "edit")
LOGIN_SET_PASSWORD_URL = os.path.join(LOGIN_ITEM_URL, "set_password")


def includeme(config):
    config.add_route(USER_URL, USER_URL)
    config.add_route(LOGIN_URL, LOGIN_URL)
    for route in (
        USER_ITEM_URL, USER_MYACCOUNT_URL, USER_ITEM_EDIT_URL, USER_LOGIN_URL,
        USER_LOGIN_EDIT_URL, USER_LOGIN_SET_PASSWORD_URL
    ):
        config.add_route(route, route, traverse="/users/{id}")

    for route in LOGIN_ITEM_URL, LOGIN_EDIT_URL, LOGIN_SET_PASSWORD_URL:
        config.add_route(route, route, traverse="/logins/{id}")
