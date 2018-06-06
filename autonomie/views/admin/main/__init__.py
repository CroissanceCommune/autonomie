# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import os

from autonomie.views.admin import (
    AdminIndexView,
    BASE_URL as BASE_ROUTE,
)
from autonomie.views.admin.tools import BaseAdminIndexView

MAIN_ROUTE = os.path.join(BASE_ROUTE, 'main')


class MainIndexView(BaseAdminIndexView):
    route_name = MAIN_ROUTE
    title = u"Configuration générale"
    description = u"Configurer les informations générales (message d'accueil, \
types de fichier, e-mail de contact)"


def includeme(config):
    config.add_route(MAIN_ROUTE, MAIN_ROUTE)
    config.add_admin_view(MainIndexView, parent=AdminIndexView)
    config.include(".site")
    config.include('.file_types')
    config.include('.contact')
