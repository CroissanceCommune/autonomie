# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2016 Croissance Commune
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
"""
Configuration générale du module vente:

    Mise en forme des PDFs
    Unité de prestation
"""
import logging
import functools
from sqlalchemy import desc

from autonomie.models.base import DBSESSION
from autonomie.views.admin.tools import (
    get_model_admin_view,
    BaseConfigView,
    make_enter_point_view,
)
from autonomie.forms.admin import (
    get_config_schema,
    tva_form_validator,
    get_sequence_model_admin,
)

from autonomie.models.task import (
    TaskMention,
    WorkUnit,
    PaymentMode,
    PaymentConditions,
    BankAccount,
)
from autonomie.models.tva import (
    Tva,
)
from autonomie.models.treasury import CustomInvoiceBookEntryModule

logger = logging.getLogger(__name__)

(
    mention_admin_class,
    mention_route,
    mention_tmpl,
) = get_model_admin_view(
    TaskMention,
    r_path="admin_vente",
)

(
    work_unit_admin_class,
    work_unit_route,
    work_unit_tmpl,
) = get_model_admin_view(
    WorkUnit,
    r_path="admin_vente",
)

(
    payment_mode_admin_class,
    payment_mode_route,
    payment_mode_tmpl,
) = get_model_admin_view(
    PaymentMode,
    r_path="admin_vente",
)

(
    payment_condition_admin_class,
    payment_condition_route,
    payment_condition_tmpl,
) = get_model_admin_view(
    PaymentConditions,
    r_path="admin_vente",
)

(
    tva_admin_class,
    tva_admin_route,
    tva_admin_tmpl,
) = get_model_admin_view(
    Tva,
    r_path="admin_vente",
)

(
    custom_treasury_admin_class,
    custom_treasury_admin_route,
    custom_treasury_admin_tmpl,
) = get_model_admin_view(
    CustomInvoiceBookEntryModule,
    r_path='admin_vente_treasury',
)


class WorkUnitAdmin(work_unit_admin_class):
    title = u"Configuration des unités de prestation"
    disable = False
    description = u"Les unités de prestation proposées lors de la création \
d'un devis/d'une facture"


class TaskMentionAdmin(mention_admin_class):
    title = u"Configuration des mentions facultatives des devis/factures"
    description = u"Des mentions facultatives que les entrepreneurs peuvent \
faire figurer dans leurs devis/factures"
    widget_options = {'min_len': 0}


class PaymentModeAdmin(payment_mode_admin_class):
    title = u"Configuration des modes de paiement"
    disable = False
    description = u"Les conditions que les entrepreneurs peuvent sélectionner \
lors de la création d'un devis/d'une facture"


class PaymentConditionAdmin(payment_condition_admin_class):
    title = u"Configuration des conditions de paiement"
    description = u"Les modes de paiement que l'on peut sélectionner pour \
enregistrer le paiement d'un devis/ d'une facture"


class AdminVenteTreasuryMain(BaseConfigView):
    """
        Cae information configuration
    """
    title = u"Configuration des informations générales et des \
modules prédéfinis"
    description = u"Configuration du code journal et des modules génériques \
(Export des factures, module contribution à la CAE, CGSCOP, RG, RG Interne)"
    redirect_path = "admin_vente_treasury"
    validation_msg = u"Les informations ont bien été enregistrées"
    keys = (
        'code_journal',
        'numero_analytique',
        'compte_frais_annexes',
        'compte_cg_banque',
        'compte_rrr',
        'compte_cg_tva_rrr',
        'code_tva_rrr',
        'compte_cg_contribution',
        "contribution_cae",
        'compte_rg_interne',
        "taux_rg_interne",
        'compte_rg_externe',
        "taux_rg_client",
        'sage_facturation_not_used',
        "sage_contribution",
        'sage_rginterne',
        'sage_rgclient',
    )
    schema = get_config_schema(keys)


class AdminVenteTreasuryCustom(custom_treasury_admin_class):
    title = u"Configuration des modules de contribution personnalisés"
    description = u"Ajouter des modules de contribution personnalisés aux \
exports de factures"
    widget_options = {
        'add_subitem_text_template': u"Ajouter un module de contribution \
personnalisé",
        "orderable": False,
    }

    def query_items(self):
        return self.factory.query().filter(self.factory.active == True).all()


class MainReceiptsConfig(BaseConfigView):
    title = u"Informations générales"
    keys = (
        'receipts_active_tva_module',
    )
    schema = get_config_schema(keys)
    validation_msg = u"L'export comptable des encaissement a bien été \
configuré"
    message = u"Configurer l'export des encaissements (le code journal \
utilisé est celui de la banque associé à chaque encaissement)"
    redirect_path = "admin_receipts"


class AdminTva(tva_admin_class):
    title = u"Configuration comptable des produits et TVA collectés"
    description = u"Taux de TVA, codes produit et codes analytiques associés"
    widget_options = {'add_subitem_text_template': u"Ajouter un taux de TVA"}

    def query_items(self):
        return DBSESSION().query(Tva).order_by(desc(Tva.active)).all()

    def customize_schema(self, schema):
        schema.validator = tva_form_validator


def admin_vente_index_view(request):
    """
    vue d'index pour la configuration du module vente
    """
    menus = []
    for label, route, title, icon in (
        (u"Retour", "admin_index", "", "fa fa-step-backward"),
        (
            WorkUnitAdmin.title,
            "admin_vente_workunit",
            WorkUnitAdmin.description,
            ""
        ),
        (
            TaskMentionAdmin.title,
            "admin_vente_mention",
            TaskMentionAdmin.description,
            ""
        ),
        (
            PaymentModeAdmin.title,
            "admin_vente_payment_mode",
            PaymentModeAdmin.description,
            ""
        ),
        (
            PaymentConditionAdmin.title,
            "admin_vente_payment_condition",
            PaymentConditionAdmin.description,
            ""
        ),
        (
            u"Configuration comptable du module Ventes",
            "admin_vente_treasury",
            u"Configuration des modules d'exports prédéfinis et personnalisés",
            ""
        ),
        (
            AdminTva.title,
            'admin_vente_tva',
            AdminTva.description,
            ""
        ),
        (
            u"Configuration comptable des encaissements",
            "admin_receipts",
            u"Configuration des différents comptes analytiques liés \
aux encaissements",
            "",
        )
    ):
        menus.append(dict(label=label, path=route, title=title, icon=icon))
    return dict(title=u"Configuration du module Ventes", menus=menus)


def admin_vente_treasury_index_view(request):
    menus = []
    for label, route, title, icon in (
        (u"Retour", "admin_vente", "", "fa fa-step-backward"),
        (
            AdminVenteTreasuryMain.title,
            "admin_vente_treasury_main",
            AdminVenteTreasuryMain.description,
            ""
        ),
        (
            AdminVenteTreasuryCustom.title,
            "admin_vente_treasury_custom",
            AdminVenteTreasuryCustom.description,
            ""
        ),
    ):
        menus.append(dict(label=label, path=route, title=title, icon=icon))
    return dict(title=u"Configuration comptable du module Ventes", menus=menus)



def include_receipts_views(config):
    """
    Add views for payments configuration
    """
    config.add_route("admin_receipts", "admin/receipts")

    all_views = [
        (
            MainReceiptsConfig,
            "admin_main_receipts",
            "/admin/main.mako",
        ),
        get_model_admin_view(BankAccount, r_path="admin_receipts"),
    ]

    for view, route_name, tmpl in all_views:
        config.add_route(route_name, "admin/" + route_name)
        config.add_admin_view(
            view,
            route_name=route_name,
            renderer=tmpl,
        )

    config.add_admin_view(
        make_enter_point_view(
            "admin_vente",
            all_views,
            u"Configuration comptables du module encaissements",
        ),
        route_name='admin_receipts'
    )


def includeme(config):
    config.add_route('admin_vente', "admin/vente")
    config.add_route("admin_vente_print", "admin/vente/print")
    config.add_route("admin_vente_mention", "admin/vente/mention")
    config.add_route("admin_vente_workunit", "admin/vente/workunit")
    config.add_route("admin_vente_payment_mode", "admin/vente/payment_mode")
    config.add_route("admin_vente_treasury", "admin/vente/treasury")
    config.add_route("admin_vente_treasury_main", "admin/vente/treasury/main")
    config.add_route(
        "admin_vente_treasury_custom",
        "admin/vente/treasury/custom"
    )
    config.add_route("admin_vente_tva", "admin/vente/tva")
    config.add_route(
        "admin_vente_payment_condition",
        "admin/vente/payment_condition"
    )

    config.add_admin_view = functools.partial(
        config.add_view,
        permission='admin',
        renderer="admin/main.mako",
    )

    include_receipts_views(config)

    config.add_admin_view(
        admin_vente_index_view,
        route_name="admin_vente",
    )

    config.add_admin_view(
        admin_vente_treasury_index_view,
        route_name="admin_vente_treasury",
    )

    config.add_admin_view(
        TaskMentionAdmin,
        route_name="admin_vente_mention",
    )

    config.add_admin_view(
        WorkUnitAdmin,
        route_name="admin_vente_workunit",
    )

    config.add_admin_view(
        PaymentModeAdmin,
        route_name="admin_vente_payment_mode",
    )

    config.add_admin_view(
        PaymentConditionAdmin,
        route_name='admin_vente_payment_condition',
    )

    config.add_admin_view(
        AdminVenteTreasuryMain,
        route_name='admin_vente_treasury_main',
    )

    config.add_admin_view(
        AdminVenteTreasuryCustom,
        route_name='admin_vente_treasury_custom',
    )

    config.add_admin_view(
        AdminTva,
        route_name='admin_vente_tva',
    )
