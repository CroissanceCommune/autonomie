# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;

from autonomie.models.task import Estimation
from autonomie.forms.tasks.estimation import get_list_schema
from autonomie.views.estimations.lists import CompanyEstimationList
from autonomie.views import TreeMixin
from autonomie.views.business.routes import BUSINESS_ITEM_ESTIMATION_ROUTE
from autonomie.views.project.business import BusinessListView
from autonomie.views.business.business import (
    remember_navigation_history,
)


class BusinessEstimationList(CompanyEstimationList, TreeMixin):
    route_name = BUSINESS_ITEM_ESTIMATION_ROUTE
    schema = get_list_schema(
        is_global=False,
        excludes=("company_id", 'year', 'customer',)
    )
    add_template_vars = (u'title', 'is_admin', "with_draft", "add_url", )

    @property
    def add_url(self):
        return self.request.route_path(
            self.route_name,
            id=self.request.context.id,
            _query={'action': 'add'}
        )

    @property
    def title(self):
        return u"Devis du projet {0}".format(
            self.request.context.name
        )

    def _get_company_id(self, appstruct):
        """
        Return the current context's company id
        """
        return self.request.context.project.company_id

    def filter_business(self, query, appstruct):
        remember_navigation_history(self.request, self.context.id)
        self.populate_navigation()
        query = query.filter(Estimation.business_id == self.context.id)
        return query


def includeme(config):
    config.add_tree_view(
        BusinessEstimationList,
        parent=BusinessListView,
        renderer="project/estimations.mako",
        permission="list.estimations",
        layout="business"
    )
