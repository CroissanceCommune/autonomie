# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Attached files related views
"""
from sqlalchemy.orm import (
    load_only,
)
from pyramid.httpexceptions import HTTPFound

from autonomie.models import files

from autonomie.views import (
    BaseView,
    TreeMixin,
)

from autonomie.views.files import FileUploadView
from autonomie.views.business.routes import (
    BUSINESS_ITEM_FILE_ROUTE,
    BUSINESS_ITEM_ROUTE,
)
from autonomie.views.project.business import BusinessListView
from autonomie.views.business.business import BusinessOverviewView


class BusinessFileAddView(FileUploadView, TreeMixin):
    route_name = BUSINESS_ITEM_ROUTE

    def __init__(self, *args, **kw):
        FileUploadView.__init__(self, *args, **kw)
        self.populate_navigation()

    def redirect(self, come_from):
        return HTTPFound(
            self.request.route_path(
                BUSINESS_ITEM_FILE_ROUTE,
                id=self.context.id,
            )
        )


class BusinessFilesView(BaseView, TreeMixin):
    route_name = BUSINESS_ITEM_FILE_ROUTE

    @property
    def current_business(self):
        return self.context

    def __call__(self):
        self.populate_navigation()
        query = files.File.query().options(load_only(
            "description",
            "name",
            "updated_at",
            "id",
        ))
        query = query.filter_by(parent_id=self.current_business.id)

        return dict(
            title=u"Documents rattachés à cette affaire",
            files=query,
            current_business=self.current_business,
        )


def includeme(config):
    config.add_tree_view(
        BusinessFileAddView,
        parent=BusinessOverviewView,
        permission="add.file",
        request_param="action=attach_file",
        layout='default',
        renderer="autonomie:templates/base/formpage.mako",
    )
    config.add_tree_view(
        BusinessFilesView,
        parent=BusinessListView,
        permission="list.files",
        renderer="autonomie:templates/business/files.mako",
        layout="business",
    )
