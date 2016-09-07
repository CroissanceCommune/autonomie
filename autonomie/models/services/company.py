# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2016 Croissance Commune
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
"""
Company query service
"""
import datetime
from sqlalchemy import (
    desc,
    and_,
)
from sqlalchemy.orm import load_only

from autonomie.models.base import DBSESSION


class CompanyService(object):
    @classmethod
    def get_tasks(cls, instance, offset=None, limit=None):
        from autonomie.models.task import Task
        query = DBSESSION().query(Task)
        query = query.filter(Task.company_id == instance.id)
        query = query.filter(
            Task.type_.in_(('invoice', 'estimation', 'cancelinvoice'))
        )
        query = query.order_by(desc(Task.statusDate))
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        return query

    @classmethod
    def get_estimations(cls, instance, valid=False):
        from autonomie.models.task import Estimation
        query = DBSESSION().query(Estimation)
        query = query.filter(Estimation.company_id == instance.id)
        if valid:
            query = query.filter(
                Estimation.CAEStatus.in_(Estimation.valid_states)
            )

        return query

    @classmethod
    def get_invoices(cls, instance, valid=False, not_paid=False):
        from autonomie.models.task import Invoice
        query = DBSESSION().query(Invoice)
        query = query.filter(Invoice.company_id == instance.id)
        if valid:
            query = query.filter(Invoice.CAEStatus.in_(Invoice.valid_states))
        elif not_paid:
            query = query.filter(Invoice.CAEStatus.in_(Invoice.not_paid_states))
        return query

    @classmethod
    def get_cancelinvoices(cls, instance, valid=False):
        from autonomie.models.task import CancelInvoice
        query = DBSESSION().query(CancelInvoice)
        query = query.filter(CancelInvoice.company_id == instance.id)
        if valid:
            query = query.filter(
                CancelInvoice.CAEStatus.in_(CancelInvoice.valid_states)
            )
        return query

    @classmethod
    def get_customers(cls, instance, year):
        from autonomie.models.task import Invoice
        from autonomie.models.customer import Customer
        query = DBSESSION().query(Customer)
        query = query.filter(Customer.company_id == instance.id)
        query = query.filter(
            Customer.invoices.any(
                and_(
                    Invoice.CAEStatus.in_(Invoice.valid_states),
                    Invoice.financial_year == year
                )
            )
        )
        return query

    @classmethod
    def get_late_invoices(cls, instance):
        from autonomie.models.task import Invoice
        query = cls.get_invoices(instance, not_paid=True)
        key_day = datetime.date.today() - datetime.timedelta(days=45)
        query = query.filter(Invoice.date < key_day)
        query = query.order_by(desc(Invoice.date))
        return query

    @classmethod
    def get_customer_codes_and_names(cls, company):
        """
        Return a query for code and names of customers related to company
        :param company: the company we're working on
        :returns: an orm query loading Customer instances with only the columns
        we want
        :rtype: A Sqlalchemy query object
        """
        from autonomie.models.customer import Customer
        query = DBSESSION().query(Customer)
        query = query.options(load_only('code', 'name'))
        query = query.filter(Customer.code != None)
        query = query.filter(Customer.company_id == company.id)
        return query.order_by(Customer.code)

    @classmethod
    def get_project_codes_and_names(cls, company):
        """
        Return a query for code and names of projects related to company

        :param company: the company we're working on
        :returns: an orm query loading Project instances with only the columns
        we want
        :rtype: A Sqlalchemy query object
        """
        from autonomie.models.project import Project
        query = DBSESSION().query(Project)
        query = query.options(load_only('code', 'name'))
        query = query.filter(Project.code != None)
        query = query.filter(Project.company_id == company.id)
        return query.order_by(Project.code)
