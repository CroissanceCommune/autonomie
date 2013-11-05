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

from beaker.cache import cache_region

from autonomie.models.task.task import Task
from autonomie.models.task.invoice import (
        Invoice,
        CancelInvoice,
        ManualInvoice,
        )
from autonomie.models.company import Company
from autonomie.models.project import Project
from autonomie.models.customer import Customer
from autonomie.views.forms.invoices import (
        InvoicesListSchema,
        STATUS_OPTIONS,
        )
from sqlalchemy import or_, and_
from sqlalchemy.orm import aliased

from .base import BaseListView

log = logging.getLogger(__name__)

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
    schema = InvoicesListSchema()
    sort_columns = dict(taskDate=("taskDate",),
               number=("number",),
               customer=("customer", "name",),
               company=("project", "company", "name",),
               officialNumber=("officialNumber",))

    default_sort = "officialNumber"
    default_direction = 'desc'

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
