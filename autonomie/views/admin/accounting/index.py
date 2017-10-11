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
            u"Configuration des indicateurs de trésorerie",
            "/admin/accounting/treasury_measure_types",
            u"Définition des codes comptables utilisés pour le calcul des "
            u"indicateurs de trésorerie",
            "",
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
