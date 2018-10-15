# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
)

from autonomie.models.task import Task
from autonomie.forms.tasks.invoice import get_list_schema
from autonomie.views import (
    TreeMixin,
    BaseFormView,
)
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
    BUSINESS_ITEM_INVOICING_ROUTE,
    BUSINESS_ITEM_INVOICING_ALL_ROUTE,
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
    add_template_vars = CompanyInvoicesListView.add_template_vars + ('add_url',)
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


class BusinessInvoicingView(BaseFormView):
    pass


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


def gen_invoice_from_payment_deadline(context, request):
    """
    Generate an invoice based on a payment deadline

    :param obj request: The request object
    :param obj context: The current business
    """
    deadline_id = request.matchdict['deadline_id']
    deadline = context.find_deadline(deadline_id)
    if not deadline:
        return HTTPNotFound()

    invoices = context.gen_invoices(request.user, [deadline])
    return HTTPFound(
        request.route_path(
            "/invoices/{id}",
            id=invoices[0].id,
        )
    )


def gen_all_invoices(context, request):
    """
    Generate all invoices attached to a business

    :param obj request: The request object
    :param obj context: The current Business
    """
    invoices = context.gen_invoices(request.user)
    if len(invoices) == 1:
        return HTTPFound(
            request.route_path(
                "/invoices/{id}",
                id=invoices[0].id,
            )
        )
    else:
        return HTTPFound(
            request.route_path(
                BUSINESS_ITEM_INVOICE_ROUTE,
                id=context.id,
            )
        )


def includeme(config):
    config.add_tree_view(
        BusinessInvoicesListView,
        parent=ProjectBusinessListView,
        renderer="autonomie:templates/business/invoices.mako",
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
    config.add_view(
        gen_invoice_from_payment_deadline,
        route_name=BUSINESS_ITEM_INVOICING_ROUTE,
        permission="add.invoice",
    )
    config.add_view(
        gen_all_invoices,
        route_name=BUSINESS_ITEM_INVOICING_ALL_ROUTE,
        permission="add.invoice",
    )
