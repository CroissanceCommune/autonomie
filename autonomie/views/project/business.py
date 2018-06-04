# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Views related to Businesses
"""
from sqlalchemy import (
    distinct,
)
from autonomie_base.models.base import DBSESSION
from autonomie.models.project.business import Business
from autonomie.utils.widgets import Link

from autonomie.views import (
    BaseListView,
    TreeMixin,
)
from autonomie.utils.menu import (
    MenuItem,
)
from autonomie.views.project.layout import ProjectMenu
from autonomie.views.project.routes import (
    PROJECT_ITEM_BUSINESS_ROUTE,
)
from autonomie.views.business.routes import (
    BUSINESS_ITEM_ROUTE,
)
from autonomie.views.project.lists import ProjectListView
from autonomie.views.project.project import remember_navigation_history


ProjectMenu.add(
    MenuItem(
        name="project_businesses",
        label=u"Liste des affaires",
        route_name=PROJECT_ITEM_BUSINESS_ROUTE,
        icon=u'fa fa-folder-open',
        perm='list.businesses',
    )
)


class BusinessListView(BaseListView, TreeMixin):
    """
    View listing businesses
    """
    add_template_vars = ('stream_actions', )
    schema = None
    sort_columns = {
        "created_at": Business.created_at,
        'name': Business.name,
    }
    default_sort = "name"
    default_direction = "asc"
    route_name = PROJECT_ITEM_BUSINESS_ROUTE
    item_route_name = BUSINESS_ITEM_ROUTE

    @property
    def title(self):
        return u"Affaires du projet {0}".format(self.current().name)

    @property
    def url(self):
        if hasattr(self.context, 'project_id'):
            return self.request.route_path(
                self.route_name, id=self.context.project_id
            )
        else:
            return self.request.route_path(
                self.route_name, id=self.context.id
            )

    def current(self):
        if hasattr(self.context, 'project'):
            return self.context.project
        else:
            return self.context

    def query(self):
        remember_navigation_history(self.request, self.context.id)
        query = DBSESSION().query(distinct(Business.id), Business)
        query = query.filter_by(project_id=self.current().id)
        return query

    def filter_closed(self, query, appstruct):
        closed = appstruct.get('closed', True)
        if not closed:
            query = query.filter_by(closed=False)
        return query

    def stream_actions(self, item):
        yield Link(
            self._get_item_url(item),
            u"Voir/Modifier",
            icon=u"pencil",
        )


def includeme(config):
    config.add_tree_view(
        BusinessListView,
        parent=ProjectListView,
        renderer="autonomie:templates/business/project_list.mako",
        permission="list.businesses",
        layout='project',
    )
