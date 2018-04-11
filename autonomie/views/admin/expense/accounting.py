# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2015 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
import os
from autonomie.views.admin.tools import (
    BaseConfigView,
)
from autonomie.forms.admin import (
    get_config_schema,
)
from autonomie.views.admin.expense import (
    EXPENSE_URL,
    ExpenseIndexView,
)


EXPENSE_ACCOUNTING_URL = os.path.join(EXPENSE_URL, 'accounting')
EXPENSE_PAYMENT_ACCOUNTING_URL = os.path.join(EXPENSE_URL, 'payment_accounting')


class ExpenseAccountingView(BaseConfigView):
    title = u"Export comptable des notes de dépense"
    route_name = EXPENSE_ACCOUNTING_URL
    keys = (
        "code_journal_ndf",
        "compte_cg_ndf",
    )
    schema = get_config_schema(keys)
    validation_msg = u"L'export comptable des notes de dépense a bien été \
configuré"
    redirect_route_name = EXPENSE_URL


class ExpensePaymentAccountingView(BaseConfigView):
    title = u"Export comptable des décaissements \
(paiement des notes de dépense)"
    route_name = EXPENSE_PAYMENT_ACCOUNTING_URL
    keys = (
        "code_journal_waiver_ndf",
        "compte_cg_waiver_ndf",
        "code_tva_ndf",
    )
    schema = get_config_schema(keys)
    validation_msg = u"L'export comptable des décaissements a bien été \
configuré"
    redirect_route_name = EXPENSE_URL


def includeme(config):
    config.add_route(EXPENSE_ACCOUNTING_URL, EXPENSE_ACCOUNTING_URL)
    config.add_route(
        EXPENSE_PAYMENT_ACCOUNTING_URL, EXPENSE_PAYMENT_ACCOUNTING_URL
    )
    config.add_admin_view(
        ExpenseAccountingView,
        parent=ExpenseIndexView,
    )
    config.add_admin_view(
        ExpensePaymentAccountingView,
        parent=ExpenseIndexView,
    )
