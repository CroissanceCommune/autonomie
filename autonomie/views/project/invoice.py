# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging

from autonomie.models.task import Task
from autonomie.forms.tasks.invoice import get_list_schema
from autonomie.views import TreeMixin
from autonomie.views.invoices.lists import (
    CompanyInvoicesListView,
    CompanyInvoicesCsvView,
    CompanyInvoicesXlsView,
    CompanyInvoicesOdsView,
    filter_all_status,
)
from autonomie.views.project.project import (
    ProjectListView,
    remember_navigation_history,
)
from autonomie.views.project.routes import (
    PROJECT_ITEM_INVOICE_ROUTE,
    PROJECT_ITEM_INVOICE_EXPORT_ROUTE,
)


logger = logging.getLogger(__name__)


class ProjectInvoiceListView(CompanyInvoicesListView, TreeMixin):
    """
    Invoice list for one given company
    """
    route_name = PROJECT_ITEM_INVOICE_ROUTE
    schema = get_list_schema(
        is_global=False,
        excludes=("company_id", 'year', 'customers',)
    )
    add_template_vars = CompanyInvoicesListView.add_template_vars + ('add_url',)
    is_admin = False

    @property
    def add_url(self):
        return self.request.route_path(
            PROJECT_ITEM_INVOICE_ROUTE,
            id=self.context.id,
            _query={'action': 'add'}
        )

    def _get_company_id(self, appstruct):
        return self.request.context.company_id

    @property
    def title(self):
        return u"Factures du projet {0}".format(
            self.request.context.name
        )

    def filter_project(self, query, appstruct):
        remember_navigation_history(self.request, self.context.id)
        self.populate_navigation()
        query = query.filter(Task.project_id == self.context.id)
        return query


class ProjectInvoicesCsvView(CompanyInvoicesCsvView):
    schema = get_list_schema(is_global=False, excludes=('company_id', 'year',))

    def _get_company_id(self, appstruct):
        return self.request.context.company_id

    def filter_project(self, query, appstruct):
        logger.debug(u" + Filtering by project_id")
        return query.filter(Task.project_id == self.context.id)

    filter_status = filter_all_status


class ProjectInvoicesXlsView(CompanyInvoicesXlsView):
    schema = get_list_schema(is_global=False, excludes=('company_id', 'year', ))

    def _get_company_id(self, appstruct):
        return self.request.context.company_id

    def filter_project(self, query, appstruct):
        logger.debug(u" + Filtering by project_id")
        return query.filter(Task.project_id == self.context.id)

    filter_status = filter_all_status


class ProjectInvoicesOdsView(CompanyInvoicesOdsView):
    schema = get_list_schema(is_global=False, excludes=('company_id', 'year', ))

    def _get_company_id(self, appstruct):
        return self.request.context.company_id

    def filter_project(self, query, appstruct):
        logger.debug(u" + Filtering by project_id")
        return query.filter(Task.project_id == self.context.id)

    filter_status = filter_all_status


def includeme(config):
    config.add_tree_view(
        ProjectInvoiceListView,
        parent=ProjectListView,
        renderer="project/invoices.mako",
        permission='list_invoices',
        layout="project",
    )
    config.add_view(
        ProjectInvoicesCsvView,
        route_name=PROJECT_ITEM_INVOICE_EXPORT_ROUTE,
        match_param="extension=csv",
        permission="list_invoices"
    )

    config.add_view(
        ProjectInvoicesOdsView,
        route_name=PROJECT_ITEM_INVOICE_EXPORT_ROUTE,
        match_param="extension=ods",
        permission="list_invoices"
    )

    config.add_view(
        ProjectInvoicesXlsView,
        route_name=PROJECT_ITEM_INVOICE_EXPORT_ROUTE,
        match_param="extension=xls",
        permission="list_invoices"
    )
