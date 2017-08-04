# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
#

"""
    Company invoice list view
"""
import logging
import datetime
import colander
from deform import (
    Form,
    ValidationFailure,
)

from sqlalchemy import (
    or_,
    and_,
    distinct,
)
from sqlalchemy.orm import contains_eager
from beaker.cache import cache_region

from autonomie_base.models.base import (
    DBSESSION,
)
from autonomie.models.task import (
    Task,
    Invoice,
    CancelInvoice,
    Payment,
)
from autonomie.models.customer import Customer
from autonomie.models.company import Company

from autonomie.utils.widgets import (
    PopUp,
    ViewLink,
)
from autonomie.utils.pdf import write_pdf

from autonomie.views.task.views import html

from autonomie.forms.tasks.invoice import (
    get_list_schema,
    pdfexportSchema,
)
from autonomie.views import (
    BaseListView,
    submit_btn,
)

logger = log = logging.getLogger(__name__)


# Here we do some multiple function stuff to allow caching to work
# Beaker caching is done through signature (dbsession is changing each time, so
# it won't cache if it's an argument of the cached function
def get_taskdates(dbsession):
    """
        Return all taskdates
    """
    @cache_region("long_term", "taskdates")
    def taskdates():
        """
            Cached version
        """
        return dbsession.query(distinct(Invoice.financial_year))
    return taskdates()


def get_years(dbsession):
    """
        We consider that all documents should be dated after 2000
    """
    inv = get_taskdates(dbsession)

    @cache_region("long_term", "taskyears")
    def years():
        """
            cached version
        """
        return [invoice[0] for invoice in inv.all()]
    return years()


def get_year_range(year):
    """
        Return the first january of the current and the next year
    """
    fday = datetime.date(year, 1, 1)
    lday = datetime.date(year + 1, 1, 1)
    return fday, lday


class GlobalInvoicesList(BaseListView):
    """
        Used as base for company invoices listing
    """
    title = u"Liste des factures de la CAE"
    add_template_vars = (u'title', u'pdf_export_btn', 'is_admin',)
    schema = get_list_schema(is_admin=True)
    sort_columns = dict(
        date=Task.date,
        internal_number=Task.internal_number,
        customer=Customer.name,
        company=Company.name,
        official_number=Task.official_number,
        ht=Task.ht,
        ttc=Task.ttc,
        payment=Payment.date,
    )

    default_sort = "official_number"
    default_direction = 'desc'
    is_admin = True

    @property
    def pdf_export_btn(self):
        """
        return a popup open button for the pdf export form and place the popup
        in the request attribute
        """
        form = get_invoice_pdf_export_form(self.request)
        popup = PopUp("pdfexportform", u'Export massif', form.render())
        self.request.popups = {popup.name: popup}
        return popup.open_btn()

    def query(self):
        query = DBSESSION().query(Task)
        query = query.with_polymorphic([Invoice, CancelInvoice])
        query = query.outerjoin(Invoice.payments)
        query = query.outerjoin(Task.customer)
        query = query.options(
            contains_eager(Invoice.payments).load_only(
                Payment.id, Payment.date, Payment.mode
            )
        )
        query = query.options(
            contains_eager(Task.customer).load_only(
                Customer.name, Customer.code, Customer.id
            )
        )
        query = query.filter(Task.status == 'valid')
        return query

    def _get_company_id(self, appstruct):
        """
        Return the company_id found in the appstruct
        Should be overriden if we want a company specific list view
        """
        res = appstruct.get('company_id')
        logger.debug("Company id : %s" % res)
        return res

    def filter_company(self, query, appstruct):
        company_id = self._get_company_id(appstruct)
        if company_id not in (None, colander.null):
            query = query.filter(Task.company_id == company_id)
        return query

    def filter_official_number(self, query, appstruct):
        number = appstruct['search']
        if number and number != -1:
            prefix = self.request.config.get('invoiceprefix', '')
            if prefix and number.startswith(prefix):
                number = number[len(prefix):]
            query = query.filter(Task.official_number == number)
        return query

    def filter_ttc(self, query, appstruct):
        ttc = appstruct.get('ttc', {})
        if ttc.get('start') not in (None, colander.null):
            log.info(u"Filtering by ttc amount : %s" % ttc)
            start = ttc.get('start')
            end = ttc.get('end')
            if end in (None, colander.null):
                query = query.filter(Task.ttc >= start)
            else:
                query = query.filter(Task.ttc.between(start, end))
        return query

    def filter_customer(self, query, appstruct):
        customer_id = appstruct.get('customer_id')
        if customer_id not in (None, colander.null):
            query = query.filter(Task.customer_id == customer_id)
        return query

    def filter_date(self, query, appstruct):
        period = appstruct.get('period', {})
        if period.get('start') not in (None, colander.null):
            start = period.get('start')
            end = period.get('end')
            if end in (None, colander.null):
                end = datetime.date.today()
            query = query.filter(Task.date.between(start, end))

        year = appstruct['year']
        if year != -1:
            query = query.filter(
                or_(
                    Invoice.financial_year == year,
                    CancelInvoice.financial_year == year,
                )
            )
        return query

    def filter_status(self, query, appstruct):
        status = appstruct['status']
        if status == 'paid':
            query = self._filter_paid(query)
        elif status == 'notpaid':
            query = self._filter_not_paid(query)
        return query

    def _filter_paid(self, query):
        return query.filter(
            or_(
                and_(
                    Task.paid_status == 'resulted',
                    Task.type_ == 'invoice'
                ),
                Task.type_ == 'cancelinvoice',
            )
        )

    def _filter_not_paid(self, query):
        return query.filter(
            Task.paid_status.in_(('waiting', 'paid'))
        ).filter(
            Task.type_ == 'invoice'
        )

    def filter_doctype(self, query, appstruct):
        """
        Filter invocies by type (invoice/cancelinvoice)
        """
        type_ = appstruct.get('doctype')
        if type_ in ('invoice', 'cancelinvoice'):
            query = query.filter(Task.type_ == type_)
        return query


class CompanyInvoicesList(GlobalInvoicesList):
    """
    Invoice list for one given company
    """
    schema = get_list_schema(is_admin=False)
    is_admin = False

    def _get_company_id(self, appstruct):
        return self.request.context.id


def get_invoice_pdf_export_form(request):
    """
        Return the form used to search for invoices that will be exported
    """
    schema = pdfexportSchema.bind(request=request)
    action = request.route_path(
        "invoices",
        _query=dict(action="export_pdf"),
    )
    query_form = Form(schema, buttons=(submit_btn,), action=action)
    return query_form


def query_documents_for_export(from_number, to_number, year):
    """
        Query the database to retrieve the documents for the pdf export
    """
    # querying the database
    query = Task.query().with_polymorphic([Invoice, CancelInvoice])
    query = query.filter(Task.official_number >= from_number)

    # Default provided in the form schema is -1
    if to_number > 0:
        query = query.filter(Task.official_number <= to_number)
    query = query.filter(
        or_(
            Invoice.financial_year == year,
            CancelInvoice.financial_year == year,
        )
    )
    records = query.order_by(Task.official_number).all()
    return records


def invoices_pdf_view(request):
    """
        Bulk pdf output : output a large amount of invoices/cancelinvoices

    """
    # We retrieve the form
    query_form = get_invoice_pdf_export_form(request)

    try:
        appstruct = query_form.validate(request.params.items())
    except ValidationFailure as e:
        # Form validation failed, the error contains the form with the error
        # messages
        query_form = e
        appstruct = None

    if appstruct is not None:
        # The form has been validated, we can query for documents
        start_number = appstruct["start"]
        end_number = appstruct["end"]
        year = appstruct['year']

        documents = query_documents_for_export(start_number, end_number, year)

        # We've got some documents to export
        if documents:
            # Getting the html output
            html_string = html(request, documents, bulk=True)

            filename = u"factures_{0}_{1}_{2}.pdf".format(
                year,
                start_number,
                end_number,
            )

            try:
                # Placing the pdf datas in the request
                write_pdf(request, filename, html_string)
                return request.response
            except BaseException as e:
                import traceback
                traceback.print_exc()
                request.session.flash(u"Erreur à l'export des factures, \
essayez de limiter le nombre de factures à exporter. Prévenez \
votre administrateur si le problème persiste.", queue="error")
        else:
            # There were no documents to export, we send a message to the end
            # user
            request.session.flash(
                u"Aucune facture n'a pu être retrouvée",
                queue="error"
            )
    gotolist_btn = ViewLink(
        u"Liste des factures",
        "admin_invoices",
        path="invoices"
    )
    request.actionmenu.add(gotolist_btn)
    return dict(
        title=u"Export massif de factures au format PDF",
        form=query_form.render(),
    )


def add_routes(config):
    """
    Add module's related route
    """
    # Company invoices view
    config.add_route(
        'company_invoices',
        '/company/{id:\d+}/invoices',
        traverse='/companies/{id}',
    )
    # Global invoices view
    config.add_route("invoices", "/invoices")


def includeme(config):
    add_routes(config)
    config.add_view(
        CompanyInvoicesList,
        route_name='company_invoices',
        renderer='invoices.mako',
        permission='list_invoices'
    )

    config.add_view(
        GlobalInvoicesList,
        route_name="invoices",
        renderer="invoices.mako",
        permission="admin_invoices"
    )

    config.add_view(
        invoices_pdf_view,
        route_name="invoices",
        request_param='action=export_pdf',
        renderer="/base/formpage.mako",
        permission="admin_invoices",
    )
