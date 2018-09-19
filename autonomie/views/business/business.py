# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from pyramid.httpexceptions import HTTPFound
from autonomie.forms.project.business import get_business_edit_schema

from autonomie.utils.navigation import NavigationHandler
from autonomie.views import (
    TreeMixin,
    BaseView,
    DeleteView,
    BaseEditView,
)
from autonomie.views.project.routes import (
    PROJECT_ITEM_ROUTE,
    PROJECT_ITEM_BUSINESS_ROUTE,
)
from autonomie.views.business.routes import (
    BUSINESS_ITEM_ROUTE,
    BUSINESS_ITEM_OVERVIEW_ROUTE,
)
from autonomie.views.project.project import ProjectEntryPointView


def remember_navigation_history(request, business_id):
    """
    Remember the last page the user has visited inside a project

    :param obj request: The request object
    """
    keyword = "/businesses/%s" % business_id
    handler = NavigationHandler(request, keyword)
    handler.remember()


def retrieve_navigation_history(request, project_id):
    """
    Retrieve the last page the user has visited inside a project

    :param obj request: The request object
    """
    keyword = "/businesses/%s" % project_id
    handler = NavigationHandler(request, keyword)
    return handler.last()


def business_entry_point_view(context, request):
    """
    Project entry point view only redirects to the most appropriate page
    """
    if context.business_type.label == "default":
        last = request.route_path(PROJECT_ITEM_ROUTE, id=context.project_id)
    else:
        last = retrieve_navigation_history(request, context.id)
        if last is None:
            last = request.route_path(
                BUSINESS_ITEM_OVERVIEW_ROUTE, id=context.id
            )
    return HTTPFound(last)


class BusinessOverviewView(BaseView, TreeMixin):
    """
    Single business view
    """
    route_name = BUSINESS_ITEM_OVERVIEW_ROUTE

    def __init__(self, *args, **kw):
        BaseView.__init__(self, *args, **kw)

    @property
    def tree_is_visible(self):
        """
        Check if this node should be displayed in the breadcrumb tree
        """
        if hasattr(self.context, 'project'):
            if self.context.project.project_type.default:
                return False
        return True

    @property
    def title(self):
        return u"{0.business_type.label} : {0.name}".format(self.context)

    @property
    def tree_url(self):
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
        remember_navigation_history(self.request, self.context.id)
        return dict(
            title=self.title,
            edit_url=self.request.route_path(
                self.route_name,
                id=self.context.id,
                _query={'action': 'edit'}
            ),
            estimations=self.context.estimations,
            indicators=[],  # self.context.indicators,
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
    config.add_view(
        business_entry_point_view,
        route_name=BUSINESS_ITEM_ROUTE,
        permission="view.business",
    )
    config.add_tree_view(
        BusinessOverviewView,
        parent=ProjectEntryPointView,
        renderer="autonomie:templates/business/overview.mako",
        permission="view.business",
        layout='business',
    )
    config.add_tree_view(
        BusinessEditView,
        parent=BusinessOverviewView,
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
        route_name=BUSINESS_ITEM_ROUTE,
        request_param="action=close",
        permission="close.business",
        layout="default"
    )
