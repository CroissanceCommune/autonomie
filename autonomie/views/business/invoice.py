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
from autonomie.views.project.business import ProjectBusinessListView
from autonomie.views.business.business import (
    remember_navigation_history,
)
from autonomie.views.business.routes import (
    BUSINESS_ITEM_INVOICE_ROUTE,
    BUSINESS_ITEM_INVOICE_EXPORT_ROUTE,
)


logger = logging.getLogger(__name__)


class BusinessInvoicesListView(CompanyInvoicesListView, TreeMixin):
    """
    Invoice list for one given company
    """
    route_name = BUSINESS_ITEM_INVOICE_ROUTE
    schema = get_list_schema(
        is_global=False,
        excludes=("company_id", 'year', 'customer',)
    )
    add_template_vars = (u'title', 'is_admin', "with_draft", 'add_url', )
    is_admin = False

    @property
    def add_url(self):
        return self.request.route_path(
            BUSINESS_ITEM_INVOICE_ROUTE,
            id=self.context.id,
            _query={'action': 'add'}
        )

    def _get_company_id(self, appstruct):
        return self.request.context.project.company_id

    @property
    def title(self):
        return u"Factures de l'affaire {0}".format(
            self.request.context.name
        )

    def filter_business(self, query, appstruct):
        remember_navigation_history(self.request, self.context.id)
        self.populate_navigation()
        query = query.filter(Task.business_id == self.context.id)
        return query


class BusinessInvoicesCsvView(CompanyInvoicesCsvView):
    schema = get_list_schema(is_global=False, excludes=('company_id', 'year',))

    def _get_company_id(self, appstruct):
        return self.request.context.project.company_id

    def filter_business(self, query, appstruct):
        logger.debug(u" + Filtering by business_id")
        return query.filter(Task.business_id == self.context.id)

    filter_status = filter_all_status


class BusinessInvoicesXlsView(CompanyInvoicesXlsView):
    schema = get_list_schema(is_global=False, excludes=('company_id', 'year', ))

    def _get_company_id(self, appstruct):
        return self.request.context.project.company_id

    def filter_business(self, query, appstruct):
        logger.debug(u" + Filtering by business_id")
        return query.filter(Task.business_id == self.context.id)

    filter_status = filter_all_status


class BusinessInvoicesOdsView(CompanyInvoicesOdsView):
    schema = get_list_schema(is_global=False, excludes=('company_id', 'year', ))

    def _get_company_id(self, appstruct):
        return self.request.context.project.company_id

    def filter_business(self, query, appstruct):
        logger.debug(u" + Filtering by business_id")
        return query.filter(Task.business_id == self.context.id)

    filter_status = filter_all_status


def includeme(config):
    config.add_tree_view(
        BusinessInvoicesListView,
        parent=ProjectBusinessListView,
        renderer="autonomie:templates/project/invoices.mako",
        permission='list.invoices',
        layout="business",
    )
    config.add_view(
        BusinessInvoicesCsvView,
        route_name=BUSINESS_ITEM_INVOICE_EXPORT_ROUTE,
        match_param="extension=csv",
        permission="list.invoices"
    )

    config.add_view(
        BusinessInvoicesOdsView,
        route_name=BUSINESS_ITEM_INVOICE_EXPORT_ROUTE,
        match_param="extension=ods",
        permission="list.invoices"
    )

    config.add_view(
        BusinessInvoicesXlsView,
        route_name=BUSINESS_ITEM_INVOICE_EXPORT_ROUTE,
        match_param="extension=xls",
        permission="list.invoices"
    )
