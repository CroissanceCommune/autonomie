# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging

from autonomie.models.treasury import CustomInvoiceBookEntryModule
from autonomie.forms.admin import get_config_schema

from autonomie.views.admin.tools import (
    get_model_admin_view,
    BaseConfigView,
)


logger = logging.getLogger(__name__)

(
    custom_treasury_admin_class,
    custom_treasury_admin_route,
    custom_treasury_admin_tmpl,
) = get_model_admin_view(
    CustomInvoiceBookEntryModule,
    r_path='admin_vente_treasury',
)


class AdminVenteTreasuryMain(BaseConfigView):
    """
        Cae information configuration
    """
    title = u"Configuration des informations générales et des \
modules prédéfinis"
    description = u"Configuration du code journal et des modules prédéfinis \
(Export des factures, contribution à la CAE, RG Externe, RG Interne)"
    redirect_route_name = "admin_vente_treasury"
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
    info_message = u"""
Configurez les exports comptables de votre CAE.
Configurez les champs indispensables aux exports :\
    <ul>\
        <li>Code journal</li>\
        <li>Numéro analytique de la CAE</li>\
        <li>Compte banque de l'entrepreneur</li>\
    </ul>\
Configurez les champs relatifs aux frais et remises:\
    <ul>\
<li>Compte de frais annexes</li>\
<li>Compte RRR (Rabais, Remises et Ristournes)</li>\
    </ul>\
    Configurez et activez des modules de retenues optionnels :\
        <ul>\
    <li>Module de contribution à la CAE</li>\
    <li>Module RG Externe (spécifique bâtiment)</li>\
    <li>Module RG Interne (spécifique bâtiment)</li>\
    </ul>
    """


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
        return self.factory.query().filter_by(active=True).all()


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
        menus.append(
            dict(label=label, route_name=route, title=title, icon=icon)
        )
    return dict(title=u"Configuration comptable du module Ventes", menus=menus)


def add_routes(config):
    config.add_route("admin_vente_treasury", "admin/vente/treasury")
    config.add_route("admin_vente_treasury_main", "admin/vente/treasury/main")
    config.add_route(
        "admin_vente_treasury_custom",
        "admin/vente/treasury/custom"
    )


def includeme(config):
    add_routes(config)
    config.add_admin_view(
        admin_vente_treasury_index_view,
        route_name="admin_vente_treasury",
    )
    config.add_admin_view(
        AdminVenteTreasuryMain,
        route_name='admin_vente_treasury_main',
    )

    config.add_admin_view(
        AdminVenteTreasuryCustom,
        route_name='admin_vente_treasury_custom',
    )
