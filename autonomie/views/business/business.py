# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from pyramid.httpexceptions import HTTPFound
from autonomie.forms.project.business import get_business_edit_schema

from autonomie.views import (
    TreeMixin,
    BaseView,
    DeleteView,
    BaseEditView,
)
from autonomie.views.project.routes import (
    PROJECT_ITEM_BUSINESS_ROUTE,
)
from autonomie.views.business.routes import (
    BUSINESS_ITEM_ROUTE,
)
from autonomie.views.project.business import BusinessListView


class BusinessView(BaseView, TreeMixin):
    """
    Single business view
    """
    route_name = BUSINESS_ITEM_ROUTE

    @property
    def title(self):
        return u"Affaire : %s" % self.context.name

    @property
    def url(self):
        if hasattr(self.context, 'business_id'):
            return self.request.route_path(
                self.route_name, id=self.context.business_id
            )
        else:
            return self.request.route_path(
                self.route_name, id=self.context.id
            )

    def __call__(self):
        self.populate_navigation()
        return dict(
            title=self.title,
            edit_url=self.request.route_path(
                self.route_name,
                id=self.context.id,
                _query={'action': 'edit'}
            )
        )


class BusinessEditView(BaseEditView, TreeMixin):
    schema = get_business_edit_schema()
    route_name = BUSINESS_ITEM_ROUTE

    @property
    def title(self):
        return u"Modification de {0}".format(self.context.name)

    def before(self, form):
        self.populate_navigation()
        return BaseEditView.before(self, form)

    def redirect(self):
        return HTTPFound(
            self.request.route_path(BUSINESS_ITEM_ROUTE, id=self.context.id)
        )


class BusinessDeleteView(DeleteView):
    def redirect(self):
        return HTTPFound(
            self.request.route_path(
                PROJECT_ITEM_BUSINESS_ROUTE,
                id=self.context.project_id
            )
        )


def close_business_view(context, request):
    """
    View used to close a Business
    """
    context.closed = True
    request.dbsession.merge(context)

    return HTTPFound(request.route_path(BUSINESS_ITEM_ROUTE, id=context.id))


def includeme(config):
    config.add_tree_view(
        BusinessView,
        parent=BusinessListView,
        renderer="autonomie:templates/business/business.mako",
        permission="view.business",
        layout='business',
    )
    config.add_tree_view(
        BusinessEditView,
        parent=BusinessView,
        renderer="autonomie:templates/base/formpage.mako",
        request_param="action=edit",
        permission="edit.business",
        layout='business',
    )
    config.add_view(
        BusinessDeleteView,
        request_param="action=delete",
        permission="delete.business",
        layout="default"
    )
    config.add_view(
        close_business_view,
        request_param="action=close",
        permission="close.business",
        layout="default"
    )
