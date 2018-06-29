# -*- coding: utf-8 -*-
# * Authors:
#       * Delalande Jocelyn
from __future__ import unicode_literals
"""
Admin view for accounting software related settings
"""

import logging
import os

from autonomie.forms.admin import get_config_schema
from autonomie.views.admin.sale.numbers import NUMBERING_CONFIG_URL
from autonomie.views.admin.sale.accounting import (
    ACCOUNTING_CONFIG_URL,
    SaleAccountingCustomView,
)
from autonomie.views.admin.sale.receipts import RECEIPT_CONFIG_URL
from autonomie.views.admin.expense.accounting import (
    EXPENSE_ACCOUNTING_URL,
    EXPENSE_PAYMENT_ACCOUNTING_URL,
)

from autonomie.views.admin.accounting import (
    AccountingIndexView,
    ACCOUNTING_URL,
)
from autonomie.views.admin.tools import BaseConfigView
NUMBERING_CONFIG_URL

logger = logging.getLogger(__name__)


BASE_URL = os.path.join(ACCOUNTING_URL, "accounting_software")


class AccountingSoftwareView(BaseConfigView):
    title = "Logiciel de comptabilité"
    description = (
        "Configurer le format d'échanges de données avec "
        "le logiciel de comptabilité."
    )
    route_name = BASE_URL

    validation_msg = u"Les informations ont bien été enregistrées"
    keys = (
        'accounting_label_maxlength',
    )
    schema = get_config_schema(keys)

    @property
    def info_message(self):
        return """
D'autres paramètres liés au logiciel de comptabilité sont disponible dans autonomie :
<ul>
    <li>Les numéros de facture dans <a href={}>Module ventes → Numérotation des factures</a></li>\
    <li>Les différents libellés d'écritures comptables :\
    <ul>\
      <li><a href="{}">Module Notes de dépenses → Export comptable des notes de dépense</a></li>\
      <li><a href="{}">Module Notes de dépenses →  Export comptable des décaissements </a></li>\
      <li><a href="{}">Module Ventes → Configuration comptable du module Vente →  Configuration des informations générales et des modules prédéfinis</a></li>\
      <li><a href="{}">Module Ventes → Configuration comptable du module Vente → Modules de contribution personnalisés</a></li>\
      <li><a href="{}">Module Ventes → Configuration comptable des encaissements → Informations générales</a></li>\
    </ul>\
    </li>\
</ul>\
""".format(*[
        self.request.route_path(i) for i in [
            NUMBERING_CONFIG_URL,
            EXPENSE_ACCOUNTING_URL,
            EXPENSE_PAYMENT_ACCOUNTING_URL,
            ACCOUNTING_CONFIG_URL,
            SaleAccountingCustomView.route_name,
            RECEIPT_CONFIG_URL,
        ]])

def add_routes(config):
    """
    Add the routes related to the current module
    """
    config.add_route(BASE_URL, BASE_URL)


def add_views(config):
    """
    Add views defined in this module
    """
    config.add_admin_view(
        AccountingSoftwareView,
        parent=AccountingIndexView,
    )


def includeme(config):
    add_routes(config)
    add_views(config)
