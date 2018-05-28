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
from autonomie.models.user.user import User
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
        disable_attribute='login',
        perm_context_attribute="login",
        perm='view.login',
    ),
)
UserMenu.add(
    AttrMenuItem(
        name="companies",
        label=u'Entreprises',
        route_name=u'/users/{id}/companies',
        icon=u'fa fa-building',
        disable_attribute='companies',
        perm='list.company',
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

        if isinstance(context, User):
            self.current_user_object = context
        elif hasattr(context, 'user'):
            self.current_user_object = context.user
        elif hasattr(context, 'userdatas'):
            self.current_user_object = context.userdatas.user
        else:
            raise KeyError(u"Can't retrieve the associated user object, \
                           current context : %s" % context)

    @property
    def usermenu(self):
        UserMenu.set_current(self.current_user_object)
        return UserMenu


def includeme(config):
    config.add_layout(
        UserLayout,
        template='autonomie:templates/layouts/user.mako',
        name='user'
)