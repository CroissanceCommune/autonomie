# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;

import logging

import pkg_resources
from autonomie.resources import (
    user_resources,
)
from autonomie.utils.menu import (
    MenuItem,
    AttrMenuItem,
    Menu,
)

logger = logging.getLogger(__name__)


UserMenu = Menu(name="usermenu")

UserMenu.add(
    MenuItem(
        name="user",
        label=u'Compte utilisateur',
        route_name=u'/users/{id}',
        icon=u'fa fa-user-o',
        perm='view.user',
    )
)
UserMenu.add(
    AttrMenuItem(
        name="login",
        label=u'Identifiants',
        route_name=u'/users/{id}/login',
        icon=u'fa fa-lock',
        model_attribute='login',
        perm='view.login',
    ),
)
UserMenu.add(
    AttrMenuItem(
        name="companies",
        label=u'Entreprises',
        route_name=u'/users/{id}/companies',
        icon=u'fa fa-building',
        model_attribute='companies',
        perm='view.companies',
    ),
)


class UserLayout(object):
    """
    Layout for user related pages

    Provide the main page structure for user view
    """
    autonomie_version = pkg_resources.get_distribution('autonomie').version

    def __init__(self, context, request):
        user_resources.need()

    @property
    def usermenu(self):
        return UserMenu


def includeme(config):
    config.add_layout(
        UserLayout,
        template='autonomie:templates/layouts/user.mako',
        name='user'
    )
