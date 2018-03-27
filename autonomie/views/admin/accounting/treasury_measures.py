# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;

"""
Admin view for Treasury measure configuration
"""
import logging
from sqlalchemy import asc

from autonomie.models.accounting.treasury_measures import (
    TreasuryMeasureType,
)
from autonomie.forms.admin import (
    get_admin_schema,
    get_config_schema,
)

from autonomie.views.admin.tools import (
    BaseConfigView,
)
from autonomie.views import (
    BaseView,
    BaseEditView,
)


logger = logging.getLogger(__name__)


BASE_URL = "/admin/accounting/treasury_measures"


def index_view(request):
    menus = []
    for label, route, title, icon in (
        (u"Retour", "/admin/accounting", "", "fa fa-step-backward"),
        (
            u"Configuration de l'interface entrepreneur",
            BASE_URL + "/ui",
            u"Configuration des priorités d'affichage dans l'interface de "
            u"l'entrepreneur",
            "fa fa-tv",
        ),
        (
            u"Configuration des indicateurs de trésorerie",
            BASE_URL + "/types",
            u"Définition des codes comptables utilisés pour le calcul des "
            u"indicateurs de trésorerie",
            "fa fa-braille",
        ),
    ):
        menus.append(
            dict(label=label, route_name=route, title=title, icon=icon)
        )
    return dict(
        title=u"Configuration de la génération des États de trésorerie",
        menus=menus
    )


class TreasuryMeasureUiView(BaseConfigView):
    title = u"Configuration de l'interface entrepreneur"
    description = (
        u"Configuration des priorités d'affichage dans l'interface"
        u" de l'entrepreneur"
    )
    redirect_route_name = BASE_URL
    validation_msg = u"Les informations ont bien été enregistrées"
    keys = ('treasury_measure_ui',)
    schema = get_config_schema(keys)
    info_message = u"""Configurer l'indicateur de trésorerie qui sera mis en \
        avant dans l'interface de l'entrepreneur"""


class TreasuryMeasureTypeListView(BaseView):
    columns = [
        u"Libellé de l'indicateur", u"Comptes commençant par "
    ]
    title = u"Configuration des indicateurs de trésorerie"
    factory = TreasuryMeasureType

    def stream_columns(self, measure_type):
        """
        Stream a column object (called from within the template)

        :param obj measure_type: The object to display
        :returns: A generator of labels representing the different columns of
        our list
        :rtype: generator
        """
        yield measure_type.label
        yield measure_type.account_prefix

    def _get_item_url(self, measure_type, action=None):
        """
        shortcut for route_path calls
        """
        query = dict(self.request.GET)
        if action is not None:
            query['action'] = action

        return self.request.route_path(
            BASE_URL + "/types/{id}",
            id=measure_type.id,
            _query=query,
        )

    def stream_actions(self, measure_type):
        """
        Stream the actions available for the given measure_type object
        :param obj measure_type: TreasuryMeasureType instance
        :returns: List of 4-uples (url, label, title, icon,)
        """
        yield (
            self._get_item_url(measure_type),
            u"Voir/Modifier",
            u"Voir/Modifier",
            u"pencil",
        )

    def _load_items(self, year=None):
        """
        Return the sqlalchemy models representing current queried elements
        :rtype: SQLAlchemy.Query object
        """
        items = self.factory.query().order_by(asc(self.factory.internal_id))
        return items

    def _more_template_vars(self, result):
        """
        Hook allowing to add datas to the templating context
        """
        result['help_msg'] = (
            u"Les définitions ci-dessous indiquent quelles écritures sont "
            u"utilisées pour le calcul des "
            u"indicateurs du tableau de bord trésorerie des entrepreneurs."
        )
        return result

    def _get_menus(self):
        """
        Return the menu entries
        """
        return [
            dict(
                label=u"Retour",
                route_name=BASE_URL,
                icon="fa fa-step-backward"
            )
        ]

    def _get_actions(self, items):
        """
        Return the description of additionnal main actions buttons

        :rtype: list
        """
        return []

    def __call__(self):
        menus = self._get_menus()

        items = self._load_items()

        result = dict(
            items=items,
            columns=self.columns,
            stream_columns=self.stream_columns,
            stream_actions=self.stream_actions,
            title=self.title,
            menus=menus,
            actions=self._get_actions(items),
        )
        self._more_template_vars(result)

        return result


class TreasuryMeasureTypeEditView(BaseEditView):
    add_template_vars = ('menus', 'help_msg')
    schema = get_admin_schema(TreasuryMeasureType)
    factory = TreasuryMeasureType

    @property
    def title(self):
        return u"Modifier la définition de l'indicateur '{0}'".format(
            self.context.label
        )

    @property
    def redirect_route(self):
        return BASE_URL + "/types"

    @property
    def menus(self):
        return [
            dict(
                label=u"Retour",
                route_name=self.redirect_route,
                icon="fa fa-step-backward"
            )
        ]


def add_routes(config):
    """
    Add the routes related to the current module
    """
    config.add_route(BASE_URL, BASE_URL)

    types_url = BASE_URL + "/types"
    config.add_route(types_url, types_url)
    config.add_route(
        types_url + "/{id}",
        types_url + "/{id}",
        traverse="treasury_measure_types/{id}",
    )
    config.add_route(
        BASE_URL + "/ui",
        BASE_URL + "/ui"
    )


def add_views(config):
    """
    Add views defined in this module
    """
    config.add_admin_view(
        index_view, route_name=BASE_URL, renderer="admin/index.mako"
    )
    config.add_admin_view(
        TreasuryMeasureUiView,
        route_name=BASE_URL + "/ui",
        renderer="admin/main.mako",
    )
    config.add_admin_view(
        TreasuryMeasureTypeListView,
        route_name=BASE_URL + "/types",
        renderer="admin/crud_list.mako",
    )
    config.add_admin_view(
        TreasuryMeasureTypeEditView,
        route_name=BASE_URL + "/types/{id}",
        renderer="admin/crud_add_edit.mako",
    )


def includeme(config):
    add_routes(config)
    add_views(config)
