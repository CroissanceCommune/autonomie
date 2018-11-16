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

EXPENSE_INFO_MESSAGE=u"""
<h4>Variables utilisables dans les gabarits de libellés</h4>\
    <p>Il est possible de personaliser les libellés comptables à l'aide d'un gabarit. Plusieurs variables sont disponibles :</p>\
    <ul>\
    <li><code>{beneficiaire}</code> : nom/prénoms de la personne ayant avancé les frais</li>\
    <li><code>{beneficiaire_LASTNAME}</code> : nom, en capitales, de la personne ayant avancé les frais</li>\
    <li>\
        <code>{expense_date}</code> : date de la note de dépense, qu'il est posisble de formatter de différentes manières :\
        <ul>\
        <li><code>{expense_date:%-m %Y}</code> : produira <code>6 2017</code> pour Juin 2017</li>\
        <li><code>{expense_date:%-m/%Y}</code> : produira <code>6/2017</code> pour Juin 2017</li>\
        <li><code>{expense_date:%m/%Y}</code> : produira <code>06/2017</code> pour Juin 2017</li>\
        </ul>\
    </li>\
    </ul>
    <p>NB : Penser à séparer les variables, par exemple par des espaces, sous peine de libellés peu lisibles.</p>\
    """


class ExpenseAccountingView(BaseConfigView):
    title = u"Export comptable des notes de dépense"
    route_name = EXPENSE_ACCOUNTING_URL
    keys = (
        'bookentry_expense_label_template',
        "code_journal_ndf",
        "compte_cg_ndf",
    )
    schema = get_config_schema(keys)
    validation_msg = u"L'export comptable des notes de dépense a bien été \
configuré"
    redirect_route_name = EXPENSE_URL
    info_message = EXPENSE_INFO_MESSAGE


class ExpensePaymentAccountingView(BaseConfigView):
    title = u"Export comptable des décaissements \
(paiement des notes de dépense)"
    route_name = EXPENSE_PAYMENT_ACCOUNTING_URL
    keys = (
        'bookentry_expense_payment_main_label_template',
        'bookentry_expense_payment_waiver_label_template',
        "code_journal_waiver_ndf",
        "compte_cg_waiver_ndf",
        "code_tva_ndf",
    )
    schema = get_config_schema(keys)
    validation_msg = u"L'export comptable des décaissements a bien été \
configuré"
    redirect_route_name = EXPENSE_URL
    info_message = EXPENSE_INFO_MESSAGE


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
