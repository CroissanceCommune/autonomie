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
from autonomie.models.base import DBSESSION
from sqlalchemy.sql.expression import func


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
    def get_next_number(cls, project, factory):
        query = DBSESSION.query(func.max(factory.sequence_number))
        query = query.filter(factory.project_id == project.id)
        max_num = query.first()[0]
        if max_num is None:
            max_num = 0

        return max_num + 1

    @classmethod
    def get_next_estimation_number(cls, project):
        """
        Return the next available sequence number in the given project
        """
        from autonomie.models.task import Estimation
        return cls.get_next_number(project, Estimation)

    @classmethod
    def get_next_invoice_number(cls, project):
        """
        Return the next available sequence number in the given project
        """
        from autonomie.models.task import Invoice
        return cls.get_next_number(project, Invoice)

    @classmethod
    def get_next_cancelinvoice_number(cls, project):
        """
        Return the next available sequence number in the given project
        """
        from autonomie.models.task import CancelInvoice
        return cls.get_next_number(project, CancelInvoice)
