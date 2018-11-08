# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Attached files related views
"""
from pyramid.httpexceptions import HTTPFound

from autonomie.models import files
from autonomie.models.task import Task
from autonomie.models.project.business import Business

from autonomie.views import (
    BaseView,
    TreeMixin,
)

from autonomie.views.files import FileUploadView
from autonomie.views.project.routes import (
    PROJECT_ITEM_FILE_ROUTE,
    PROJECT_ITEM_ADD_FILE_ROUTE,
)
from autonomie.views.project.project import ProjectListView


class ProjectFileAddView(FileUploadView, TreeMixin):
    route_name = PROJECT_ITEM_ADD_FILE_ROUTE

    def __init__(self, *args, **kw):
        FileUploadView.__init__(self, *args, **kw)
        self.populate_navigation()

    def redirect(self, come_from):
        return HTTPFound(
            self.request.route_path(
                self.route_name,
                id=self.context.id,
            )
        )


class ProjectFilesView(BaseView, TreeMixin):
    route_name = PROJECT_ITEM_FILE_ROUTE
    add_route = PROJECT_ITEM_ADD_FILE_ROUTE
    help_message = u"""
    Liste des documents rattachés au projet courant ou à un des documents
    qui le composent."""

    @property
    def title(self):
        return u"Documents rattachés au projet {0}".format(self.context.name)

    @property
    def tree_url(self):
        return self.request.route_path(self.route_name, id=self.context.id)

    def collect_parent_ids(self):
        """
        Collect the element ids for which we want the associated files
        """
        ids = [
            i[0] for i in self.request.dbsession.query(Task.id).filter_by(
                project_id=self.context.id
            )
        ]
        ids.extend(
            [
                i[0]
                for i in self.request.dbsession.query(Business.id).filter_by(
                    project_id=self.context.id
                )
            ]
        )
        ids.append(self.context.id)
        return ids

    def __call__(self):
        self.populate_navigation()
        ids = self.collect_parent_ids()
        query = files.File.query_for_filetable()
        query = query.filter(files.File.parent_id.in_(ids))

        return dict(
            title=self.title,
            files=query,
            add_url=self.request.route_path(
                self.add_route, 
                id=self.context.id,
                _query=dict(action='attach_file')
            ),
            help_message=self.help_message,
        )


def includeme(config):
    config.add_tree_view(
        ProjectFileAddView,
        parent=ProjectFilesView,
        permission="add.file",
        request_param="action=attach_file",
        layout='default',
        renderer="autonomie:templates/base/formpage.mako",
    )
    config.add_tree_view(
        ProjectFilesView,
        parent=ProjectListView,
        permission="list.files",
        renderer="autonomie:templates/project/files.mako",
        layout="project",
    )
