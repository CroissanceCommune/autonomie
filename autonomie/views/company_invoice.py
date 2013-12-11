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
from deform import (
        Form,
        ValidationFailure,
        )

from sqlalchemy import (
            or_,
            and_,
            )
from sqlalchemy.orm import aliased

from beaker.cache import cache_region

from autonomie.models.task import (
        Task,
        Invoice,
        CancelInvoice,
        ManualInvoice,
        )
from autonomie.models.company import Company
from autonomie.models.project import Project
from autonomie.models.customer import Customer

from autonomie.utils.views import submit_btn
from autonomie.utils.widgets import (
        PopUp,
        ViewLink,
        )
from autonomie.utils.pdf import write_pdf

from autonomie.views.taskaction import html

from autonomie.views.forms.invoices import (
        InvoicesListSchema,
        pdfexportSchema,
        STATUS_OPTIONS,
        )
from autonomie.views.base import BaseListView

log = logging.getLogger(__name__)

# Aliases needed to outerjoin tables properly
p1 = aliased(Project)
p2 = aliased(Project)
c1 = aliased(Customer)
c2 = aliased(Customer)
c3 = aliased(Customer)


#Here we do some multiple function stuff to allow caching to work
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
        return dbsession.query(Invoice.financial_year), \
               dbsession.query(ManualInvoice.financial_year)
    return taskdates()


def get_years(dbsession):
    """
        We consider that all documents should be dated after 2000
    """
    inv, man_inv = get_taskdates(dbsession)

    @cache_region("long_term", "taskyears")
    def years():
        """
            cached version
        """
        return sorted(set([i.financial_year for i in inv.all()])\
            .union(set([i.financial_year for i in man_inv.all()]))
            )
    return years()


def get_year_range(year):
    """
        Return the first january of the current and the next year
    """
    fday = datetime.date(year, 1, 1)
    lday = datetime.date(year + 1, 1, 1)
    return fday, lday


class InvoicesList(BaseListView):
    """
        Used as base for company invoices listing
    """
    title = u""
    add_template_vars = (u'title', u'pdf_export_btn',)
    schema = InvoicesListSchema()
    sort_columns = dict(taskDate=("taskDate",),
               number=("number",),
               customer=("customer", "name",),
               company=("project", "company", "name",),
               officialNumber=("officialNumber",))

    default_sort = "officialNumber"
    default_direction = 'desc'

    @property
    def pdf_export_btn(self):
        """
            return a popup object for the pdf export form
        """
        form = get_invoice_pdf_export_form(self.request)
        popup = PopUp("pdfexportform", u'Export massif', form.render())
        self.request.popups = {popup.name: popup}
        return popup.open_btn()

    def query(self):
        query = Task.query()\
                .with_polymorphic([Invoice, CancelInvoice, ManualInvoice])\
                     .outerjoin(p1, Invoice.project)\
                     .outerjoin(p2, CancelInvoice.project)\
                     .outerjoin(c1, Invoice.customer)\
                     .outerjoin(c2, CancelInvoice.customer)\
                     .outerjoin(c3, ManualInvoice.customer)
        if self.request.context == 'company':
            company_id = self.request.context.id
            query = query.filter(or_(p1.company_id == company_id,
                                    p2.company_id == company_id,
                                    ManualInvoice.company_id == company_id))
        return query

    def filter_company(self, query, appstruct):
        company_id = self._get_company_id(appstruct)
        if company_id != -1:
            query = query.filter(or_(p1.company_id == company_id,
                                    p2.company_id == company_id,
                                    ManualInvoice.company_id == company_id))
        return query

    def _get_company_id(self, appstruct):
        """
            Return the company id : should be overriden
        """
        return -1


    def filter_officialNumber(self, query, appstruct):
        number = appstruct['search']
        if number and number != -1:
            prefix = self.request.config.get('invoiceprefix', '')
            number = number.strip(prefix)
            query = query.filter(or_(Invoice.officialNumber == number,
                                CancelInvoice.officialNumber == number,
                                ManualInvoice.officialNumber == number))
        return query

    def filter_customer(self, query, appstruct):
        customer_id = appstruct['customer_id']
        if customer_id != -1:
            query = query.filter(or_(Invoice.customer_id == customer_id,
                                     CancelInvoice.customer_id == customer_id,
                                     ManualInvoice.customer_id == customer_id))
        return query

    def filter_taskDate(self, query, appstruct):
        year = appstruct['year']
        query = query.filter(or_(Invoice.financial_year == year,
                                CancelInvoice.financial_year == year,
                                ManualInvoice.financial_year == year))
        return query

    def filter_status(self, query, appstruct):
        status = appstruct['status']
        if status == 'paid':
            query = self._filter_paid(query)
        elif status == 'notpaid':
            query = self._filter_not_paid(query)
        else:
            query = self._filter_valid(query)
        return query

    def _filter_paid(self, query):
        inv_paid = Invoice.paid_states
        cinv_valid = CancelInvoice.valid_states
        maninv_paid = ManualInvoice.paid_states
        return query.filter(or_(and_(Task.CAEStatus.in_(inv_paid),
                                     Task.type_=='invoice'),
                                and_(Task.CAEStatus.in_(cinv_valid),
                                     Task.type_=='cancelinvoice'),
                                and_(Task.CAEStatus.in_(maninv_paid),
                                     Task.type_=='manualinvoice')))

    def _filter_not_paid(self, query):
        inv_notpaid = Invoice.not_paid_states
        maninv_notpaid = ManualInvoice.not_paid_states
        return query.filter(or_(and_(Task.CAEStatus.in_(inv_notpaid),
                                     Task.type_=='invoice'),
                                and_(Task.CAEStatus.in_(maninv_notpaid),
                                    Task.type_=='manualinvoice')))

    def _filter_valid(self, query):
        inv_validated = Invoice.valid_states
        cinv_valid = CancelInvoice.valid_states
        return query.filter(or_(and_(Task.CAEStatus.in_(inv_validated),
                                     Task.type_=='invoice'),
                                and_(Task.CAEStatus.in_(cinv_valid),
                                    Task.type_=='cancelinvoice'),
                                Task.type_=='manualinvoice'))

    def default_form_values(self, appstruct):
        super(InvoicesList, self).default_form_values(appstruct)
        appstruct['years'] = get_years(self.request.dbsession)
        appstruct['status_options'] = STATUS_OPTIONS
        return appstruct

    def _sort(self, query, appstruct):
        """
            Custom sort function
            Since we're using polymorphism, we can't order by child specific
            attributes
        """
        direction = appstruct['direction']
        if direction == 'asc':
            reverse = False
        else:
            reverse = True

        sort_key = appstruct['sort']
        sort = self.sort_columns[sort_key]

        def sort_func(a):
            """
                dinamycally built sort_key func
                sort is a path of attributes like (a,b,c) which gives a.b.c
            """
            res = a
            for e in sort:
                res = getattr(res, e)
            return res

        invoices = query.all()
        invoices = sorted(invoices, key=sort_func, reverse=reverse)
        return invoices

class CompanyInvoicesList(InvoicesList):
    def _get_company_id(self, appstruct):
        return self.request.context.id

    def default_form_values(self, appstruct):
        values = super(CompanyInvoicesList, self).default_form_values(appstruct)
        values["customers"] = self.request.context.customers
        return values

class GlobalInvoicesList(InvoicesList):
    def _get_company_id(self, appstruct):
        return appstruct['company_id']

    def default_form_values(self, appstruct):
        values = super(GlobalInvoicesList, self).default_form_values(appstruct)
        values['companies'] = Company.query().all()
        return values


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
    query = query.filter(or_(
        Invoice.officialNumber >= from_number,
        CancelInvoice.officialNumber >= from_number,
        ))

    # Default provided in the form schema is -1
    if to_number > 0:
        query = query.filter(or_(
            Invoice.officialNumber <= to_number,
            CancelInvoice.officialNumber <= to_number,
            ))
    query = query.filter(
        or_(
            Invoice.financial_year == year,
            CancelInvoice.financial_year == year,
            ))
    return query.all()


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
            html_string = html(request, documents)

            filename = u"factures_{0}_{1}_{2}.pdf".format(year,
                        start_number,
                        end_number)

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
            request.session.flash(u"Aucune facture n'a pu être retrouvée",
                    queue="error")
    gotolist_btn = ViewLink(u"Liste des factures", "edit", path="invoices")
    request.actionmenu.add(gotolist_btn)
    return dict(
                title=u"Export massif de factures au format PDF",
                form=query_form.render(),
                )


def includeme(config):
    # Company invoices view
    config.add_route('company_invoices',
                     '/company/{id:\d+}/invoices',
                     traverse='/companies/{id}')
    # Global invoices view
    config.add_route("invoices",
                    "/invoices")

    config.add_view(CompanyInvoicesList,
                    route_name='company_invoices',
                    renderer='company_invoices.mako',
                    permission='edit')
    config.add_view(GlobalInvoicesList,
                    route_name="invoices",
                    renderer="invoices.mako",
                    permission="manage")
    config.add_view(
            invoices_pdf_view,
            route_name="invoices",
            request_param='action=export_pdf',
            renderer="/base/formpage.mako",
            permission="manage",
            )
