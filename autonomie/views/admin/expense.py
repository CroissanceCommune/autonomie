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
from autonomie.views.admin.tools import (
    get_model_admin_view,
    BaseConfigView,
)
from autonomie.forms.admin import (
    get_config_schema,
)
from autonomie.models.expense import (
    ExpenseType,
    ExpenseKmType,
    ExpenseTelType,
)

(
    type_admin_class,
    TYPE_ROUTE,
    TYPE_TMPL,
) = get_model_admin_view(
    ExpenseType,
    r_path="admin_expense",
)
(
    kmtype_admin_class,
    KMTYPE_ROUTE,
    KMTYPE_TMPL,
) = get_model_admin_view(
    ExpenseKmType,
    r_path="admin_expense",
)
(
    teltype_admin_class,
    TELTYPE_ROUTE,
    TELTYPE_TTELPL,
) = get_model_admin_view(
    ExpenseTelType,
    r_path="admin_expense",
)


class AdminExpense(BaseConfigView):
    title = u"Export comptable des notes de dépense"
    keys = (
        "code_journal_ndf",
        "compte_cg_ndf",
    )
    schema = get_config_schema(keys)
    validation_msg = u"L'export comptable des notes de dépense a bien été \
configuré"
    redirect_path = "admin_expense"


class AdminExpensePaymentExport(BaseConfigView):
    title = u"Export comptable des décaissements \
(paiement des notes de dépense)"
    keys = (
        "code_journal_waiver_ndf",
        "compte_cg_waiver_ndf",
        "code_tva_ndf",
    )
    schema = get_config_schema(keys)
    validation_msg = u"L'export comptable des décaissements a bien été \
configuré"
    redirect_path = "admin_expense"


class AdminType(type_admin_class):
    def query_items(self):
        return self.factory.query().filter(
            self.factory.type == 'expense'
        ).filter(self.factory.active == True).all()


class AdminKmType(kmtype_admin_class):
    def query_items(self):
        return self.factory.query().filter(self.factory.active == True).all()


class AdminTelType(teltype_admin_class):
    def query_items(self):
        return self.factory.query().filter(self.factory.active == True).all()


def admin_expense_index_view(request):
    menus = []
    for label, route, icon, description in (
        (u"Retour", "admin_index", "fa fa-step-backward", ''),
        (
            u"Configuration des types de dépenses",
            "admin_expense_type",
            "",
            u"Configuration des types de dépenses proposés dans l'interface \
ainsi que des informations comptables associées",
        ),
        (
            u"Configuration des types de dépénses kilométriques",
            "admin_expense_km_type",
            "",
            u"Configuration des types de dépenses liées aux déplacements \
proposés dans l'interface ainsi que des informations comptables associées",
        ),
        (
            u"Configuration des types de dépenses téléphoniques",
            "admin_expense_tel_type",
            "",
            u"Configuration des types de dépenses téléphoniques \
proposés dans l'interface ainsi que des informations comptables associées",
        ),
        (
            u"Configuration des exports comptables",
            "admin_expense_treasury",
            "",
            u"Configuration des informations spécifiques à l'export des \
notes de dépense",
        ),
        (
            u"Configuration comptable des décaissements (paiements \
des notes de dépense)",
            "admin_expense_payment",
            "",
            u"Configuration des informations spécifiques à l'export des \
décaissements (abandons de créance, code tva ...)",
        ),
    ):
        menus.append(
            dict(label=label, path=route, icon=icon, title=description)
        )
    return dict(title=u"Configuration du module Notes de dépense", menus=menus)


def includeme(config):
    config.add_route("admin_expense", "admin/expenses")
    config.add_route("admin_expense_payment", "admin/expense_payments")
    config.add_view(
        AdminExpensePaymentExport,
        route_name="admin_expense_payment",
        renderer="admin/main.mako",
        permission="admin",
    )
    config.add_route("admin_expense_treasury", "admin/expenses/treasury")
    config.add_view(
        admin_expense_index_view,
        route_name="admin_expense",
        renderer="admin/index.mako",
        permission="admin",
    )
    config.add_view(
        AdminExpense,
        route_name="admin_expense_treasury",
        renderer="admin/main.mako",
        permission="admin",
    )
    for route, tmpl, view_class in (
        (TYPE_ROUTE, TYPE_TMPL, AdminType,),
        (KMTYPE_ROUTE, TYPE_TMPL, AdminKmType,),
        (TELTYPE_ROUTE, TYPE_TMPL, AdminTelType,),
    ):
        config.add_route(route, "admin/expenses/" + route)
        config.add_view(
            view_class,
            route_name=route,
            renderer=tmpl,
            permission="admin",
        )
