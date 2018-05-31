# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


from autonomie.models.task import Estimation
from autonomie.forms.tasks.estimation import get_list_schema
from autonomie.views.estimations.lists import CompanyEstimationList
from autonomie.views import TreeMixin
from autonomie.views.project.routes import PROJECT_ITEM_ESTIMATION_ROUTE
from autonomie.views.project.project import (
    ProjectListView,
    remember_navigation_history,
)


class ProjectEstimationList(CompanyEstimationList, TreeMixin):
    route_name = PROJECT_ITEM_ESTIMATION_ROUTE
    schema = get_list_schema(
        is_global=False,
        excludes=("company_id", 'year', 'customers',)
    )
    add_template_vars = (u'title', 'is_admin', "with_draft", "add_url", )

    @property
    def add_url(self):
        return self.request.route_path(
            PROJECT_ITEM_ESTIMATION_ROUTE,
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
        return self.request.context.company_id

    def filter_project(self, query, appstruct):
        remember_navigation_history(self.request, self.context.id)
        self.populate_navigation()
        query = query.filter(Estimation.project_id == self.context.id)
        return query


def includeme(config):
    config.add_tree_view(
        ProjectEstimationList,
        parent=ProjectListView,
        renderer="project/estimations.mako",
        permission="list_estimations",
        layout="project"
    )
