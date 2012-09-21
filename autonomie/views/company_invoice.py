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
from pyramid.view import view_config

from autonomie.models.model import Invoice
from autonomie.models.model import CancelInvoice
from autonomie.models.model import ManualInvoice
from autonomie.models.model import Company
from autonomie.models.model import Project
from autonomie.models.model import Client
from autonomie.models.types import format_to_taskdate

from .base import ListView

log = logging.getLogger(__name__)

class CompanyInvoicesView(ListView):
    """
        Treasury and invoice view
    """
    columns = dict(taskDate=("taskDate",),
                   number=("number",),
                   client=("project", "client", "name",),
                   company=("project", "company", "name",),
                   officialNumber=("officialNumber",)
                   )
    default_sort = "officialNumber"
    default_direction = 'desc'

    @view_config(route_name='company_invoices',
                 renderer='company_invoices.mako',
                 permission='edit')
    def company_invoices(self):
        """
            List invoices for the given company
        """
        company = self.request.context
        current_year = datetime.date.today().year
        log.debug("Getting invoices")
        search, sort, direction, current_page, items_per_page = \
                    self._get_pagination_args()
        client = self.request.params.get('client')
        if client == '-1':
            client = None
        paid = self.request.params.get('paid', 'both')
        year = self.request.params.get('year', current_year)

        invoices = self.get_invoices(company.id, search, client,
                                        year, paid,sort, direction)
        records = self._get_pagination(invoices, current_page, items_per_page)
        return dict(title=u"Factures",
                    company=company,
                    invoices=records,
                    current_client=client,
                    current_year=year,
                    current_paid=paid,
                    years=self._get_years())

    def _get_taskdates(self):
        """
            Return all taskdates
        """
        @cache_region("long_term", "taskdates")
        def taskdates():
            """
                Cached version
            """
            return self.dbsession.query(Invoice.taskDate), \
                self.dbsession.query(ManualInvoice.taskDate)
        return taskdates()

    def _get_years(self):
        """
            We consider that all documents should be dated after 2000
        """
        inv, man_inv = self._get_taskdates()
        @cache_region("long_term", "taskyears")
        def years():
            """
                cached version
            """
            return sorted(
                    set([i.taskDate.year for i in inv.all()
                            ]).union(
                     set([i.taskDate.year for i in man_inv.all()
                         ]))
                )
        return years()

    @view_config(route_name="invoices",
                renderer="invoices.mako",
                permission="manage")
    def invoices(self):
        """
            Return all invoices
        """
        current_year = datetime.date.today().year
        log.debug("# Getting invoices #")
        search, sort, direction, current_page, items_per_page = \
                    self._get_pagination_args()
        client = self.request.params.get('client')
        if client == '-1':
            client = None
        paid = self.request.params.get('paid', 'both')
        year = self.request.params.get('year', current_year)

        company_id = self.request.params.get('company')
        if company_id == '-1':
            company_id = None

        invoices = self.get_invoices(company_id, search, client,
                    year, paid,sort, direction)
        records = self._get_pagination(invoices, current_page, items_per_page)

        return dict(title=u"Factures",
                    invoices=records,
                    current_client=client,
                    current_year=year,
                    current_paid=paid,
                    years=self._get_years(),
                    current_company=company_id,
                    companies=Company.query(active=False).all())

    def get_invoices(self, company_id=None, search=None, client=None,
                           year=None, paid=None, sort=None, direction="asc"):
        """
            Return the invoices
        """
        cancel_inv, inv, man_inv = self._get_invoices()
        if company_id:
            cancel_inv, inv, man_inv = self._filter_by_company(cancel_inv,
                                                    inv, man_inv, company_id)
        if search:
            cancel_inv, inv, man_inv = self._filter_by_number(cancel_inv,
                                                    inv, man_inv, search)
        #If we search an invoice number, we don't need more filter
        else:
            if client:
                cancel_inv, inv, man_inv = self._filter_by_client(cancel_inv,
                                                        inv, man_inv, client)
            cancel_inv, inv, man_inv = self._filter_by_status(cancel_inv,
                                                        inv, man_inv, paid)
        if year:
            cancel_inv, inv, man_inv = self._filter_by_date(cancel_inv,
                                                        inv, man_inv, year)

        all_inv = inv.all()
        all_inv.extend(cancel_inv)
        all_inv.extend(man_inv)
        if direction == 'asc':
            reverse = False
        else:
            reverse = True

        def sort_key(a):
            """
                dinamycally built sort_key func
            """
            res = a
            for e in sort:
                res = getattr(res, e)
            return res
        inv = inv.all()
        inv.extend(cancel_inv.all())
        inv.extend(man_inv.all())
        invoices = sorted(inv, key=sort_key, reverse=reverse)
        return invoices

    def _get_invoices(self):
        """
            request filter invoices by clients
        """
        join_args = ("project", "client", "company",)
        cancel_inv = self.dbsession.query(CancelInvoice).join(*join_args)
        inv = self.dbsession.query(Invoice).join(*join_args)
        man_inv = self.dbsession.query(ManualInvoice)\
                                .join(ManualInvoice.client)\
                                .join(Client.company)
        return cancel_inv, inv, man_inv

    @staticmethod
    def _filter_by_company(cancel_inv, inv, man_inv, company_id):
        """
            add a filter on the company id
        """
        inv = inv.filter(Project.company_id==company_id )
        cancel_inv = cancel_inv.filter(Project.company_id==company_id )
        man_inv = man_inv.filter(ManualInvoice.company_id==company_id)
        return cancel_inv, inv, man_inv

    @staticmethod
    def _filter_by_number(cancel_inv, inv, man_inv, number):
        """
            add a filter on the numbers to invoices sqla queries
        """
        inv = inv.filter(Invoice.officialNumber == number)
        cancel_inv = cancel_inv.filter(CancelInvoice.officialNumber == number)
        man_inv = man_inv.filter(
                             ManualInvoice.officialNumber == number)
        return cancel_inv, inv, man_inv

    @staticmethod
    def _filter_by_client(cancel_inv, inv, man_inv, client):
        """
            add a filter on the client to invoices sqla queries
        """
        inv = inv.filter(Project.client_id == client)
        cancel_inv = cancel_inv.filter(Project.client_id == client)
        man_inv = man_inv.filter(ManualInvoice.client_id == client)
        return cancel_inv, inv, man_inv

    @staticmethod
    def _filter_by_status(cinv, inv, man_inv, status):
        """
            add a filter on the status to invoices sqla queries
        """
        inv_paid = Invoice.paid_states
        inv_notpaid = Invoice.not_paid_states
        inv_validated = Invoice.valid_states

        cinv_valid = CancelInvoice.valid_states

        if status == "paid":
            inv = inv.filter(Invoice.CAEStatus.in_(inv_paid))
            cinv = cinv.filter(CancelInvoice.CAEStatus.in_(cinv_valid))
            man_inv = man_inv.filter(ManualInvoice.payment_ok==1)
        elif status == "notpaid":
            inv = inv.filter(Invoice.CAEStatus.in_(inv_notpaid))
            # A cancel invoice is always paid
            cinv = cinv.filter(CancelInvoice.CAEStatus=="nutt")
            man_inv = man_inv.filter(ManualInvoice.payment_ok==0)
        else:
            inv = inv.filter(Invoice.CAEStatus.in_(inv_validated))
            cinv = cinv.filter(CancelInvoice.CAEStatus.in_(cinv_valid))
        return cinv, inv, man_inv

    @staticmethod
    def _filter_by_date(cancel_inv, inv, man_inv, year):
        """
            add a filter on dates to the invoices sqla queries
        """
        fday = datetime.date(int(year), 1, 1)
        lday = datetime.date(int(year)+1, 1, 1)
        inv = inv.filter(
                        Invoice.taskDate.between(
                                format_to_taskdate(fday),
                                format_to_taskdate(lday))
                        )
        cancel_inv = cancel_inv.filter(CancelInvoice.taskDate.between(
                                format_to_taskdate(fday),
                                format_to_taskdate(lday)))
        man_inv = man_inv.filter(
                        ManualInvoice.taskDate.between(fday, lday))
        return cancel_inv, inv, man_inv

    @view_config(route_name='company_treasury',
                 renderer='company_treasury.mako',
                 permission='edit')
    def company_treasury(self):
        """
            View for the treasury view
        """
        company = self.request.context
        today = datetime.date.today()
        current_year = today.year
        year = self.request.params.get('year', current_year)
        log.debug("Getting invoices")
        invoices = self.get_invoices(company_id=company.id,
                                         paid="paid",
                                         year=year,
                                         sort=('taskDate',))
        return dict(
                title=u"Trésorerie",
                invoices=invoices,
                company=company,
                years=self._get_years(),
                current_year=year,
                today=today)

