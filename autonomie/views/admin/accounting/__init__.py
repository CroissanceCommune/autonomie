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


ACCOUNTING_URL = os.path.join(BASE_URL, 'accounting')


class AccountingIndexView(BaseAdminIndexView):
    route_name = ACCOUNTING_URL
    title = u"Module Comptabilité"
    description = u"Configurer les tableaux de bord (trésorerie, \
comptes de résultat) et les paramètres liés au logiciel de comptabilité."


def includeme(config):
    config.add_route(ACCOUNTING_URL, ACCOUNTING_URL)
    config.add_admin_view(AccountingIndexView, parent=AdminIndexView)
    config.include('.accounting_software')
    config.include('.treasury_measures')
    config.include('.income_statement_measures')
