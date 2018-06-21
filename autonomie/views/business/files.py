# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Attached files related views
"""
from autonomie.models.task import Task

from autonomie.views.business.routes import (
    BUSINESS_ITEM_FILE_ROUTE,
    BUSINESS_ITEM_ADD_FILE_ROUTE,
)
from autonomie.views.project.business import ProjectBusinessListView
from autonomie.views.project.files import (
    ProjectFileAddView,
    ProjectFilesView,
)
from autonomie.views.business.business import BusinessOverviewView


class BusinessFileAddView(ProjectFileAddView):
    route_name = BUSINESS_ITEM_ADD_FILE_ROUTE


class BusinessFilesView(ProjectFilesView):
    route_name = BUSINESS_ITEM_FILE_ROUTE
    add_route = BUSINESS_ITEM_FILE_ROUTE
    help_message = u"""
    Liste des documents rattachés à l'affaire courante ou à un des documents
    qui la composent."""

    @property
    def title(self):
        return u"Documents rattachés à l'affaire {0}".format(self.context.name)

    def collect_parent_ids(self):
        ids = [i[0] for i in self.request.dbsession.query(Task.id).filter_by(
            business_id=self.context.id
        )]

        ids.append(self.context.id)
        return ids


def includeme(config):
    config.add_tree_view(
        BusinessFileAddView,
        parent=BusinessOverviewView,
        permission="add.file",
        layout='default',
        renderer="autonomie:templates/base/formpage.mako",
    )
    config.add_tree_view(
        BusinessFilesView,
        parent=ProjectBusinessListView,
        permission="list.files",
        renderer="autonomie:templates/business/files.mako",
        layout="business",
    )
