# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os

from autonomie.views.admin import (
    AdminIndexView,
    BASE_URL,
)
from autonomie.views.admin.tools import BaseAdminIndexView


USERDATAS_URL = os.path.join(BASE_URL, 'userdatas')


class UserDatasIndexView(BaseAdminIndexView):
    route_name = USERDATAS_URL
    title = u"Module Gestion sociale"
    description = u"Module de gestion des données sociales : Configurer les \
typologies des données, les modèles de documents"


def includeme(config):
    config.add_route(USERDATAS_URL, USERDATAS_URL)
    config.add_admin_view(UserDatasIndexView, parent=AdminIndexView)
    config.include('.options')
    config.include('.templates')
