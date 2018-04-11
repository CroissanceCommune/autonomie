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


EXPENSE_URL = os.path.join(BASE_URL, 'expenses')


class ExpenseIndexView(BaseAdminIndexView):
    route_name = EXPENSE_URL
    title = u"Module Notes de dépenses"
    description = u"Configurer les types de dépenses, les exports comptables"


def includeme(config):
    config.add_route(EXPENSE_URL, EXPENSE_URL)
    config.add_admin_view(ExpenseIndexView, parent=AdminIndexView)
    config.include('.types')
    config.include('.accounting')
