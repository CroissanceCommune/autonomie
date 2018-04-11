# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;

"""
Admin view for Treasury measure configuration
"""
import logging
import os
from sqlalchemy import asc

from autonomie.models.accounting.treasury_measures import (
    TreasuryMeasureType,
)
from autonomie.forms.admin import (
    get_admin_schema,
    get_config_schema,
)
from autonomie.utils.widgets import Link
from autonomie.views.admin.accounting import (
    AccountingIndexView,
    ACCOUNTING_URL,
)
from autonomie.views.admin.tools import (
    BaseConfigView,
    AdminCrudListView,
    BaseAdminIndexView,
    BaseAdminEditView,
)


logger = logging.getLogger(__name__)


BASE_URL = os.path.join(ACCOUNTING_URL, "treasury_measures")
UI_URL = os.path.join(BASE_URL, 'ui')
TYPE_URL = os.path.join(BASE_URL, 'types')
TYPE_ITEM_URL = os.path.join(TYPE_URL, '{id}')


class TreasuryIndexView(BaseAdminIndexView):
    title = u"États de trésorerie"
    route_name = BASE_URL


class TreasuryMeasureUiView(BaseConfigView):
    title = u"Configuration de l'interface entrepreneur"
    description = (
        u"Configuration des priorités d'affichage dans l'interface"
        u" de l'entrepreneur"
    )
    route_name = UI_URL

    redirect_route_name = BASE_URL
    validation_msg = u"Les informations ont bien été enregistrées"
    keys = ('treasury_measure_ui',)
    schema = get_config_schema(keys)
    info_message = u"""Configurer l'indicateur de trésorerie qui sera mis en \
        avant dans l'interface de l'entrepreneur"""


class TreasuryMeasureTypeListView(AdminCrudListView):
    columns = [
        u"Libellé de l'indicateur", u"Comptes commençant par "
    ]
    title = u"Configuration des indicateurs de trésorerie"
    factory = TreasuryMeasureType
    route_name = TYPE_URL

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
            TYPE_ITEM_URL,
            id=measure_type.id,
            _query=query,
        )

    def stream_actions(self, measure_type):
        """
        Stream the actions available for the given measure_type object
        :param obj measure_type: TreasuryMeasureType instance
        :returns: List of 4-uples (url, label, title, icon,)
        """
        yield Link(
            self._get_item_url(measure_type),
            u"Voir/Modifier",
            icon=u"pencil",
        )

    def load_items(self):
        """
        Return the sqlalchemy models representing current queried elements
        :rtype: SQLAlchemy.Query object
        """
        items = self.factory.query().order_by(asc(self.factory.internal_id))
        return items

    def more_template_vars(self, result):
        """
        Hook allowing to add datas to the templating context
        """
        result['help_msg'] = (
            u"Les définitions ci-dessous indiquent quelles écritures sont "
            u"utilisées pour le calcul des "
            u"indicateurs du tableau de bord trésorerie des entrepreneurs."
        )
        return result


class TreasuryMeasureTypeEditView(BaseAdminEditView):
    route_name = TYPE_ITEM_URL
    schema = get_admin_schema(TreasuryMeasureType)
    factory = TreasuryMeasureType

    @property
    def title(self):
        return u"Modifier la définition de l'indicateur '{0}'".format(
            self.context.label
        )


def add_routes(config):
    """
    Add the routes related to the current module
    """
    config.add_route(BASE_URL, BASE_URL)
    config.add_route(TYPE_URL, TYPE_URL)
    config.add_route(
        TYPE_ITEM_URL,
        TYPE_ITEM_URL,
        traverse="treasury_measure_types/{id}",
    )
    config.add_route(UI_URL, UI_URL)


def add_views(config):
    """
    Add views defined in this module
    """
    config.add_admin_view(
        TreasuryIndexView,
        parent=AccountingIndexView,
    )
    config.add_admin_view(
        TreasuryMeasureUiView,
        parent=TreasuryIndexView,
    )
    config.add_admin_view(
        TreasuryMeasureTypeListView,
        parent=TreasuryIndexView,
        renderer="admin/crud_list.mako",
    )
    config.add_admin_view(
        TreasuryMeasureTypeEditView,
        parent=TreasuryMeasureTypeListView,
        renderer="admin/crud_add_edit.mako",
    )


def includeme(config):
    add_routes(config)
    add_views(config)
