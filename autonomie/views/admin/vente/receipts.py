# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;

from autonomie.forms.admin import get_config_schema
from autonomie.views.admin.tools import (
    get_model_admin_view,
    BaseConfigView,
    make_enter_point_view,
)
from autonomie.models.payments import (
    BankAccount,
)


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
    redirect_route_name = "admin_receipts"


def add_routes(config):
    config.add_route("admin_receipts", "admin/receipts")


def add_views(config):
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
        route_name='admin_receipts',
    )


def includeme(config):
    """
    Add views for payments configuration
    """
    add_routes(config)
    add_views(config)
