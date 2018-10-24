# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import colander
from sqlalchemy import extract

from autonomie.utils.widgets import Link
from autonomie.models.accounting.treasury_measures import (
    TreasuryMeasureGrid,
)
from autonomie.models.config import Config
from autonomie.forms.accounting import get_treasury_measures_list_schema
from autonomie.views import BaseListView


logger = logging.getLogger(__name__)


class CompanyTreasuryMeasuresListView(BaseListView):
    title = u"État de trésorerie"
    schema = get_treasury_measures_list_schema()
    add_template_vars = (
        'info_msg',
        'current_grid',
        'stream_actions',
        'last_grid',
        'highlight_key',
    )
    sort_columns = {
        'date': 'date',
    }
    default_sort = 'date'
    default_direction = "desc"

    @property
    def highlight_key(self):
        config_key = Config.get("treasury_measure_ui")
        if config_key is None:
            key = 1
        else:
            key = int(config_key.value)
        return key

    @property
    def info_msg(self):
        return (u"Ces données sont déposées à intervalle régulier dans "
                u"Autonomie par l'équipe comptable de votre CAE")

    def get_company_id(self):
        if isinstance(self.context, TreasuryMeasureGrid):
            return self.context.company_id
        else:
            return self.context.id

    @property
    def last_grid(self):
        company_id = self.get_company_id()
        last_grid_object = TreasuryMeasureGrid.last(company_id)
        last_grid = None
        if last_grid_object is not None:
            last_grid = last_grid_object.__json__(self.request)
        return last_grid

    @property
    def current_grid(self):
        if isinstance(self.context, TreasuryMeasureGrid):
            current_grid_object = self.context
            current_grid = current_grid_object.__json__(self.request)
        else:
            current_grid = self.last_grid
        return current_grid

    def query(self):
        if not self.request.GET and \
                not isinstance(self.context, TreasuryMeasureGrid):
            return None
        else:
            company_id = self.get_company_id()
            query = TreasuryMeasureGrid.query().filter_by(
                company_id=company_id
            )
        return query

    def filter_year(self, query, appstruct):
        year = appstruct.get('year')
        if year not in (None, colander.null):
            query = query.filter(
                extract('year', TreasuryMeasureGrid.date) == year
            )
        return query

    def stream_actions(self, item):
        url = self.request.route_path(
            "/treasury_measure_grids/{id}",
            id=item.id
        )
        return (
            Link(
                url,
                u"Voir cet état",
                title=u"Voir le détail de cet état de trésorerie",
                icon=u"money",
            ),
        )


def add_routes(config):
    config.add_route(
        "/companies/{id}/accounting/treasury_measure_grids",
        "/companies/{id}/accounting/treasury_measure_grids",
        traverse="/companies/{id}",
    )
    config.add_route(
        "/treasury_measure_grids/{id}",
        "/treasury_measure_grids/{id}",
        traverse="/treasury_measure_grids/{id}",
    )


def add_views(config):
    config.add_view(
        CompanyTreasuryMeasuresListView,
        route_name="/companies/{id}/accounting/treasury_measure_grids",
        permission="view.accounting",
        renderer="/accounting/treasury_measures.mako",
    )
    config.add_view(
        CompanyTreasuryMeasuresListView,
        route_name="/treasury_measure_grids/{id}",
        permission="view.accounting",
        renderer="/accounting/treasury_measures.mako",
    )


def includeme(config):
    add_routes(config)
    add_views(config)
