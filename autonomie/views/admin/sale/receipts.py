# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os
from autonomie.forms.admin import get_config_schema
from autonomie.views.admin.tools import (
    get_model_admin_view,
    BaseConfigView,
    BaseAdminIndexView,
)
from autonomie.models.payments import (
    BankAccount,
)
from autonomie.views.admin.sale import (
    SaleIndexView,
    SALE_URL,
)

RECEIPT_URL = os.path.join(SALE_URL, "receipts")
RECEIPT_CONFIG_URL = os.path.join(RECEIPT_URL, "config")


class ReceiptIndexView(BaseAdminIndexView):
    title = u"Configuration comptable des encaissements"
    description = u"Configurer les différents comptes analytiques liés aux \
encaissements"
    route_name = RECEIPT_URL


class MainReceiptConfig(BaseConfigView):
    title = u"Informations générales"
    route_name = RECEIPT_CONFIG_URL

    keys = (
        'receipts_active_tva_module',
        'bookentry_payment_label_template',
    )
    schema = get_config_schema(keys)
    validation_msg = u"L'export comptable des encaissement a bien été \
configuré"
    info_message = u"""\
<p>\
  Configurer l'export des encaissements (le code journal\
  utilisé est celui de la banque associé à chaque encaissement)\
</p>\
<h3>Libellés d'écritures comptables</h3>\
    <p>Il est possible de les personaliser à l'aide d'un gabarit. Plusieurs variables sont disponibles :</p>\
    <ul>\
    <li><code>{invoice.customer.label}</code> : le nom du client émetteur du paiement</li>\
    <li><code>{company.name}</code> : le nom de l'enseigne destinataire du paiement</li>\
    </ul>\
"""


def add_routes(config):
    config.add_route(RECEIPT_URL, RECEIPT_URL)
    config.add_route(RECEIPT_CONFIG_URL, RECEIPT_CONFIG_URL)


def add_views(config):
    config.add_admin_view(
        ReceiptIndexView,
        parent=SaleIndexView,
    )
    config.add_admin_view(
        MainReceiptConfig,
        parent=ReceiptIndexView,
    )

    view = get_model_admin_view(BankAccount, r_path=RECEIPT_URL)
    config.add_route(view.route_name, view.route_name)
    config.add_admin_view(view, parent=ReceiptIndexView)


def includeme(config):
    """
    Add views for payments configuration
    """
    add_routes(config)
    add_views(config)
