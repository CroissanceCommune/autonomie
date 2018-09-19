# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;

import logging
import colander
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
from autonomie.views.user.routes import (
    USER_ITEM_URL,
    USER_LOGIN_URL,
    USER_ACCOUNTING_URL,
)

logger = logging.getLogger(__name__)


def deferred_enterprise_label(item, kw):
    """
    Collect a custom label for the "Entreprises" menu entry using binding
    parameters
    """
    current_user = kw['current_user']
    if current_user.companies:
        label = u"Entreprises <span class='badge'>{}</span>".format(
            len(current_user.companies)
        )
    else:
        label = u"<em>Entreprises</em> <span class='badge badge-alert'>0</span>"
    return label


def deferred_login_label(item, kw):
    """
    Custom deferred label for the login sidebar entry
    """
    current_user = kw['current_user']
    if current_user.login:
        return u"Identifiants"
    else:
        return u"<em>Identifiants</em>"


def deferred_accounting_show_perm(item, kw):
    request = kw['request']
    current_user = kw['current_user']
    if current_user.login:
        return request.has_permission('admin_treasury')
    else:
        return False


UserMenu = Menu(name="usermenu")

UserMenu.add(
    MenuItem(
        name="user",
        label=u'Compte utilisateur',
        route_name=USER_ITEM_URL,
        icon=u'fa fa-user-o',
        perm='view.user',
    )
)
UserMenu.add(
    AttrMenuItem(
        name="login",
        label=deferred_login_label,
        route_name=USER_LOGIN_URL,
        icon=u'fa fa-lock',
        disable_attribute='login',
        perm_context_attribute="login",
        perm='view.login',
    ),
)
UserMenu.add(
    AttrMenuItem(
        name="accounting",
        label=u"Informations comptables",
        route_name=USER_ACCOUNTING_URL,
        icon=u'fa fa-money',
        perm=deferred_accounting_show_perm
    )
)
UserMenu.add(
    AttrMenuItem(
        name="companies",
        label=deferred_enterprise_label,
        title=u"Entreprises associées à ce compte",
        route_name=u'/users/{id}/companies',
        icon=u'fa fa-building',
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
        UserMenu.bind(current_user=self.current_user_object)
        return UserMenu


def includeme(config):
    config.add_layout(
        UserLayout,
        template='autonomie:templates/layouts/user.mako',
        name='user'
    )
