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


SALE_URL = os.path.join(BASE_URL, 'sales')


class SaleIndexView(BaseAdminIndexView):
    route_name = SALE_URL
    title = u"Module Ventes"
    description = u"Configurer les mentions des devis et factures, les \
unités de prestation ..."


def includeme(config):
    config.add_route(SALE_URL, SALE_URL)
    config.add_admin_view(SaleIndexView, parent=AdminIndexView)
    config.include('.forms')
    config.include('.mentions')
    config.include('.pdf')
    config.include('.business_cycle')
    config.include('.accounting')
    config.include('.tva')
    config.include('.receipts')
    config.include('.numbers')
