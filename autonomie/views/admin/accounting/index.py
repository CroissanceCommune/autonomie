# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def admin_accounting_index_view(request):
    menus = []
    for label, route, title, icon in (
        (u"Retour", "admin_index", "", "fa fa-step-backward"),
        (
            u"Configurer les États de Trésorerie",
            "/admin/accounting/treasury_measures",
            u"Les états de trésorerie sont générés depuis les balances "
            u"analytiques déposées dans Autonomie",
            "fa fa-money",
        ),
        (
            u"Configurer les Comptes de résultat",
            "/admin/accounting/income_statement_measures",
            u"Les comptes de résultat sont générés depuis les grands livres "
            u"déposés dans Autonomie",
            "fa fa-cog",
        ),
    ):
        menus.append(
            dict(label=label, route_name=route, title=title, icon=icon)
        )
    return dict(
        title=u"Configuration du module Fichier de trésorerie",
        menus=menus
    )


def includeme(config):
    config.add_route('/admin/accounting', "/admin/accounting")
    config.add_admin_view(
        admin_accounting_index_view,
        route_name="/admin/accounting"
    )
