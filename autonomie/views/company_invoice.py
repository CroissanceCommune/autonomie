# -*- coding: utf-8 -*-
# * File Name : company_invoice.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 27-08-2012
# * Last Modified :
#
# * Project :
#
"""
    Company invoice list view
"""
import logging
import datetime

from beaker.cache import cache_region

from autonomie.models.task.task import Task
from autonomie.models.task.invoice import Invoice
from autonomie.models.task.invoice import CancelInvoice
from autonomie.models.task.invoice import ManualInvoice
from autonomie.models.company import Company
from autonomie.models.project import Project
from autonomie.models.client import Client
from autonomie.models.types import format_to_taskdate
from autonomie.views.forms.invoices import InvoicesListSchema
from autonomie.views.forms.invoices import STATUS_OPTIONS
from sqlalchemy import or_, and_
from sqlalchemy.orm import aliased

from .base import BaseListView

log = logging.getLogger(__name__)

p1 = aliased(Project)
p2 = aliased(Project)
c1 = aliased(Client)
c2 = aliased(Client)
c3 = aliased(Client)


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
    schema = InvoicesListSchema()
    sort_columns = dict(taskDate=("taskDate",),
               number=("number",),
               client=("client", "name",),
               company=("project", "company", "name",),
               officialNumber=("officialNumber",))

    default_sort = "officialNumber"
    default_direction = 'desc'

    def query(self):
        query = Task.query()\
                .with_polymorphic([Invoice, CancelInvoice, ManualInvoice])\
                     .outerjoin(p1, Invoice.project)\
                     .outerjoin(p2, CancelInvoice.project)\
                     .outerjoin(c1, Invoice.client)\
                     .outerjoin(c2, CancelInvoice.client)\
                     .outerjoin(c3, ManualInvoice.client)
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
        if number != -1:
            query = query.filter(or_(Invoice.officialNumber == number,
                                CancelInvoice.officialNumber == number,
                                ManualInvoice.officialNumber == number))
        return query

    def filter_client(self, query, appstruct):
        client_id = appstruct['client_id']
        if client_id != -1:
            query = query.filter(or_(p1.client_id == client_id,
                                     p2.client_id == client_id,
                                     ManualInvoice.client_id == client_id))
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
        values["clients"] = self.request.context.clients
        return values

class GlobalInvoicesList(InvoicesList):
    def _get_company_id(self, appstruct):
        return appstruct['company_id']

    def default_form_values(self, appstruct):
        values = super(GlobalInvoicesList, self).default_form_values(appstruct)
        values['companies'] = Company.query(active=False).all()
        return values

# A bit silly but will be removed soon
def company_treasury(request):
    """
        View for the treasury view
    """
    invoices = Invoice.query().join(Project).filter(Invoice.CAEStatus=='resulted')

    company = request.context
    invoices = invoices.filter(Project.company_id==company.id)

    today = datetime.date.today()
    current_year = today.year
    year = request.params.get('year', current_year)
    try:
        year = int(year)
    except:
        year = current_year
    invoices = invoices.filter(Invoice.financial_year == year)
    invoices = invoices.order_by(Invoice.taskDate)
    return dict(
            title=u"Trésorerie",
            invoices=invoices,
            company=company,
            years=get_years(request.dbsession),
            current_year=year,
            today=today)

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
    config.add_view(company_treasury,
                    route_name='company_treasury',
                    renderer='company_treasury.mako',
                    permission='edit')
