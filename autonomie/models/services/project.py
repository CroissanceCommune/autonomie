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
Query service related to projects
"""
from sqlalchemy import distinct
from sqlalchemy.orm import load_only
from sqlalchemy.sql.expression import func
from autonomie_base.models.base import DBSESSION


class ProjectService(object):

    @classmethod
    def get_tasks(cls, instance, type_str=None):
        from autonomie.models.task import Task
        query = DBSESSION().query(Task)
        query = query.filter_by(project_id=instance.id)

        if type_str is not None:
            query = query.filter(Task.type_ == type_str)
        else:
            query = query.filter(
                Task.type_.in_(('invoice', 'cancelinvoice', 'estimation'))
            )
        return query

    @classmethod
    def get_invoices(cls, instance):
        """
        Return a sqla query for getting the project invoices
        """
        return cls.get_tasks(instance, 'invoice')

    @classmethod
    def get_estimations(cls, instance):
        """
        Return a sqla query for getting the project estimations
        """
        return cls.get_tasks(instance, 'estimation')

    @classmethod
    def get_cancelinvoices(cls, instance):
        """
        Return a sqla query for getting the project cancelinvoices
        """
        return cls.get_tasks(instance, 'cancelinvoice')

    @classmethod
    def count_tasks(cls, instance):
        return cls.get_tasks(instance).count()

    @classmethod
    def get_next_index(cls, project, factory):
        query = DBSESSION.query(func.max(factory.project_index))
        query = query.filter(factory.project_id == project.id)
        max_num = query.first()[0]
        if max_num is None:
            max_num = 0

        return max_num + 1

    @classmethod
    def get_next_estimation_index(cls, project):
        """
        Return the next available sequence number in the given project
        """
        from autonomie.models.task import Estimation
        return cls.get_next_index(project, Estimation)

    @classmethod
    def get_next_invoice_index(cls, project):
        """
        Return the next available sequence number in the given project
        """
        from autonomie.models.task import Invoice
        return cls.get_next_index(project, Invoice)

    @classmethod
    def get_next_cancelinvoice_index(cls, project):
        """
        Return the next available sequence number in the given project
        """
        from autonomie.models.task import CancelInvoice
        return cls.get_next_index(project, CancelInvoice)

    @classmethod
    def check_phase_id(cls, project_id, phase_id):
        """
        Check phase_id is attached to project_id
        """
        from autonomie.models.project import Phase
        return DBSESSION().query(Phase.id).filter_by(
            id=phase_id).filter_by(project_id=project_id).count() > 0

    @classmethod
    def label_query(cls, project_class):
        """
        Only load columns used to build project labels
        """
        return project_class.query().options(load_only('id', 'name', 'code'))

    @classmethod
    def get_code_list_with_labels(cls, project_class, company_id):
        query = project_class.query().options(load_only('name', 'code'))
        query = query.filter_by(company_id=company_id)
        query = query.filter(project_class.code != None)
        return query.all()

    @classmethod
    def get_customer_projects(cls, project_class, customer_id):
        from autonomie.models.customer import Customer
        query = project_class.query().options(load_only('id', 'name', 'code'))
        query = query.filter(
            project_class.customers.any(
                Customer.id == customer_id
            )
        )
        query = query.filter(project_class.archived == False)
        return query.all()

    @classmethod
    def get_used_business_type_ids(cls, instance):
        from autonomie.models.task import Task

        return [
            a[0]
            for a in DBSESSION().query(
                distinct(Task.business_type_id)
            ).filter_by(
                project_id=instance.id
            )
            if a[0] is not None
        ]
