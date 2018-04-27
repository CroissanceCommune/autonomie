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
    distinct,
)
from sqlalchemy.orm import (
    contains_eager,
    load_only,
)
from beaker.cache import cache_region
from pyramid.httpexceptions import HTTPFound

from autonomie_celery.tasks.export import export_to_file
from autonomie_celery.models import FileGenerationJob
from autonomie_celery.tasks.utils import check_alive
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

from autonomie.utils.renderer import set_close_popup_response
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
    TreeMixin,
    BaseListView,
    submit_btn,
)
from autonomie.views.project.routes import (
    PROJECT_ITEM_INVOICE_ROUTE,
    PROJECT_ITEM_INVOICE_EXPORT_ROUTE,
)
from autonomie.views.project.project import ProjectListView

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


def filter_all_status(self, query, appstruct):
    """
    Filter the invoice by status
    """
    status = appstruct.get('status', 'all')
    if status != 'all':
        logger.info("  + Status filtering : %s" % status)
        query = query.filter(Task.status == status)

    return query


class InvoiceListTools(object):
    title = u"Factures de la CAE"
    schema = get_list_schema(is_global=True, excludes=('status',))
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

    def query(self):
        query = DBSESSION().query(Task)
        query = query.with_polymorphic([Invoice, CancelInvoice])
        query = query.outerjoin(Invoice.payments)
        query = query.outerjoin(Task.customer)
        query = query.outerjoin(Task.company)
        query = query.options(
            contains_eager(Invoice.payments).load_only(
                Payment.id, Payment.date, Payment.mode
            )
        )
        query = query.options(
            contains_eager(Task.customer).load_only(
                Customer.name, Customer.code, Customer.id,
                Customer.firstname, Customer.lastname, Customer.civilite,
                Customer.type_,
            )
        )
        query = query.options(
            contains_eager(Task.company).load_only(
                Company.name,
                Company.id,
            )
        )
        query = query.options(
            load_only(
                "_acl",
                "name",
                "date",
                "id",
                "ht",
                "tva",
                "ttc",
                "company_id",
                "customer_id",
                "official_number",
                "internal_number",
                "prefix",
                "status",
                Invoice.paid_status,
            )
        )
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
            logger.debug(u"    Filtering by official_number : %s" % number)
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
            logger.debug(u"Customer id : %s" % customer_id)
            query = query.filter(Task.customer_id == customer_id)
        return query

    def filter_date(self, query, appstruct):
        logger.debug(u" + Filtering date")
        period = appstruct.get('period', {})
        if period.get('start') not in (None, colander.null):
            start = period.get('start')
            end = period.get('end')
            if end in (None, colander.null):
                end = datetime.date.today()
            query = query.filter(Task.date.between(start, end))

            logger.debug(u"    Between %s and %s" % (start, end))

        year = appstruct.get('year', -1)
        if year != -1:
            query = query.filter(
                or_(
                    Invoice.financial_year == year,
                    CancelInvoice.financial_year == year,
                )
            )
            logger.debug(u"    Year : %s" % year)
        return query

    def filter_status(self, query, appstruct):
        """
        Filter the status a first time (to be overriden)
        """
        logger.debug("Filtering status")
        query = query.filter(Task.status == 'valid')
        return query

    def filter_paid_status(self, query, appstruct):
        status = appstruct['paid_status']
        if status == 'paid':
            query = self._filter_paid(query)
        elif status == 'notpaid':
            query = self._filter_not_paid(query)
        return query

    def _filter_paid(self, query):
        return query.filter(
            or_(
                Invoice.paid_status == 'resulted',
                Task.type_ == 'cancelinvoice',
            )
        )

    def _filter_not_paid(self, query):
        return query.filter(
            Invoice.paid_status.in_(('waiting', 'paid'))
        )

    def filter_doctype(self, query, appstruct):
        """
        Filter invocies by type (invoice/cancelinvoice)
        """
        type_ = appstruct.get('doctype')
        if type_ in ('invoice', 'cancelinvoice'):
            query = query.filter(Task.type_ == type_)
        else:
            query = query.filter(Task.type_.in_(('invoice', 'cancelinvoice')))
        return query


class GlobalInvoicesListView(InvoiceListTools, BaseListView):
    """
        Used as base for company invoices listing
    """
    add_template_vars = (u'title', u'pdf_export_btn', 'is_admin',)
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


class CompanyInvoicesListView(GlobalInvoicesListView):
    """
    Invoice list for one given company
    """
    is_admin = False
    schema = get_list_schema(is_global=False, excludes=("company_id",))
    add_template_vars = (u'title', 'is_admin', "with_draft", )

    @property
    def with_draft(self):
        return True

    def _get_company_id(self, appstruct):
        return self.request.context.id

    @property
    def title(self):
        return u"Factures de l'entreprise {0}".format(self.request.context.name)

    filter_status = filter_all_status


class ProjectInvoicesListView(CompanyInvoicesListView, TreeMixin):
    """
    Invoice list for one given company
    """
    route_name = PROJECT_ITEM_INVOICE_ROUTE
    schema = get_list_schema(
        is_global=False,
        excludes=("company_id", 'year', 'customers',)
    )
    is_admin = False

    def _get_company_id(self, appstruct):
        return self.request.context.company_id

    @property
    def title(self):
        return u"Factures du projet {0}".format(
            self.request.context.name
        )

    def filter_project(self, query, appstruct):
        self.populate_navigation()
        query = query.filter(Task.project_id == self.context.id)
        return query


class GlobalInvoicesCsvView(InvoiceListTools, BaseListView):
    model = Invoice
    file_format = "csv"
    filename = "factures_"

    def query(self):
        query = self.request.dbsession.query(Task).with_polymorphic(
            [Invoice, CancelInvoice]
        )
        query = query.options(load_only(Task.id))
        return query

    def _build_return_value(self, schema, appstruct, query):
        """
        Return the streamed file object
        """
        service_ok, msg = check_alive()
        if not service_ok:
            if "popup" in self.request.GET:
                set_close_popup_response(self.request, error=msg)
                return self.request.response
            else:
                self.request.session.flash(msg, 'error')
                return HTTPFound(self.request.referrer)

        logger.debug("    + In the GlobalInvoicesCsvView._build_return_value")
        job = FileGenerationJob()
        job.set_owner(self.request.user.login.login)
        self.request.dbsession.add(job)
        self.request.dbsession.flush()
        logger.debug("    + The job {job.id} was initialized".format(job=job))
        all_ids = [elem.id for elem in query]
        logger.debug("    + All_ids where collected : {0}".format(all_ids))
        logger.debug("    + Delaying the export_to_file task")
        celery_job = export_to_file.delay(
            job.id,
            'invoices',
            all_ids,
            self.filename,
            self.file_format
        )
        logger.info(
            u"The Celery Task {0} has been delayed, its result "
            "sould be retrieved from the FileGenerationJob {1}".format(
                celery_job.id, job.id
            )
        )

        return HTTPFound(
            self.request.route_path('job', id=job.id, _query={'popup': 1})
        )


class GlobalInvoicesXlsView(GlobalInvoicesCsvView):
    file_format = "xls"


class GlobalInvoicesOdsView(GlobalInvoicesCsvView):
    file_format = "ods"


class CompanyInvoicesCsvView(GlobalInvoicesCsvView):
    schema = get_list_schema(is_global=False, excludes=('company_id',))

    def _get_company_id(self, appstruct):
        return self.request.context.id

    filter_status = filter_all_status


class CompanyInvoicesXlsView(GlobalInvoicesXlsView):
    schema = get_list_schema(is_global=False, excludes=('company_id',))

    def _get_company_id(self, appstruct):
        return self.request.context.id

    filter_status = filter_all_status


class CompanyInvoicesOdsView(GlobalInvoicesOdsView):
    schema = get_list_schema(is_global=False, excludes=('company_id',))

    def _get_company_id(self, appstruct):
        return self.request.context.id

    filter_status = filter_all_status


class ProjectInvoicesCsvView(CompanyInvoicesCsvView):
    schema = get_list_schema(is_global=False, excludes=('company_id', 'year',))

    def _get_company_id(self, appstruct):
        return self.request.context.company_id

    def filter_project(self, query, appstruct):
        return query.filter(Task.project_id == self.context.id)

    filter_status = filter_all_status


class ProjectInvoicesXlsView(CompanyInvoicesXlsView):
    schema = get_list_schema(is_global=False, excludes=('company_id', 'year', ))

    def _get_company_id(self, appstruct):
        return self.request.context.company_id

    def filter_project(self, query, appstruct):
        return query.filter(Task.project_id == self.context.id)

    filter_status = filter_all_status


class ProjectInvoicesOdsView(CompanyInvoicesOdsView):
    schema = get_list_schema(is_global=False, excludes=('company_id', 'year', ))

    def _get_company_id(self, appstruct):
        return self.request.context.company_id

    def filter_project(self, query, appstruct):
        return query.filter(Task.project_id == self.context.id)

    filter_status = filter_all_status


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
    if 'submit' in request.params:
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

            documents = query_documents_for_export(
                start_number,
                end_number,
                year
            )

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
                # There were no documents to export, we send a message to the
                # end user
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
    # Company invoices route
    config.add_route(
        'company_invoices',
        '/company/{id:\d+}/invoices',
        traverse='/companies/{id}',
    )
    # Global invoices route
    config.add_route("invoices", "/invoices")

    # invoice export routes
    config.add_route(
        "invoices_export",
        "/invoices.{extension}"
    )
    config.add_route(
        "company_invoices_export",
        "/company/{id:\d+}/invoices.{extension}",
        traverse='/companies/{id}',
    )


def includeme(config):
    add_routes(config)
    config.add_view(
        GlobalInvoicesListView,
        route_name="invoices",
        renderer="invoices.mako",
        permission="admin_invoices"
    )
    config.add_view(
        GlobalInvoicesCsvView,
        route_name="invoices_export",
        match_param="extension=csv",
        permission="admin_invoices"
    )
    config.add_view(
        GlobalInvoicesOdsView,
        route_name="invoices_export",
        match_param="extension=ods",
        permission="admin_invoices"
    )
    config.add_view(
        GlobalInvoicesXlsView,
        route_name="invoices_export",
        match_param="extension=xls",
        permission="admin_invoices"
    )

    config.add_view(
        CompanyInvoicesListView,
        route_name='company_invoices',
        renderer='invoices.mako',
        permission='list_invoices'
    )
    config.add_view(
        CompanyInvoicesCsvView,
        route_name="company_invoices_export",
        match_param="extension=csv",
        permission="list_invoices"
    )

    config.add_view(
        CompanyInvoicesOdsView,
        route_name="company_invoices_export",
        match_param="extension=ods",
        permission="list_invoices"
    )

    config.add_view(
        CompanyInvoicesXlsView,
        route_name="company_invoices_export",
        match_param="extension=xls",
        permission="list_invoices"
    )

    config.add_tree_view(
        ProjectInvoicesListView,
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

    config.add_view(
        invoices_pdf_view,
        route_name="invoices",
        request_param='action=export_pdf',
        renderer="/base/formpage.mako",
        permission="list_invoices",
    )
