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
    Project model
"""
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import (
    deferred,
    relationship,
    backref,
)

from autonomie.models import widgets
from autonomie.models.utils import get_current_timestamp
from autonomie.models.types import CustomDateType
from autonomie.models.base import (
        default_table_args,
        DBBASE,
        )
from autonomie.models.node import Node

ProjectCustomer = Table('project_customer', DBBASE.metadata,
        Column("project_id", Integer, ForeignKey('project.id')),
        Column("customer_id", Integer, ForeignKey('customer.id')),
        mysql_charset=default_table_args['mysql_charset'],
        mysql_engine=default_table_args['mysql_engine'])

class Project(Node):
    """
        The project model
    """
    __tablename__ = 'project'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'project'}
    id = Column('id', ForeignKey('node.id'), primary_key=True)
    code = Column("code", String(4), nullable=False)
    definition = deferred(Column("definition", Text), group='edit')

    company_id = Column("company_id", Integer,
                                    ForeignKey('company.id'))

    startingDate = deferred(Column("startingDate", CustomDateType,
                                default=get_current_timestamp), group='edit')
    endingDate = deferred(Column("endingDate", CustomDateType,
                                default=get_current_timestamp), group='edit')

    type = deferred(Column('type', String(150)), group='edit')
    archived = Column("archived", String(255), default=0)

    customers = relationship(
        "Customer",
        secondary=ProjectCustomer,
        backref=backref(
            'projects',
            info={'colanderalchemy': widgets.EXCLUDED},
        )
    )

    def get_estimation(self, taskid):
        """
            Returns the estimation with id taskid
        """
        for estimation in self.estimations:
            if estimation.id == int(taskid):
                return estimation
        raise KeyError("No such task in this project")

    def get_invoice(self, taskid):
        """
            Returns the estimation with id taskid
        """
        for invoice in self.invoices:
            if invoice.id == int(taskid):
                return invoice
        raise KeyError("No such task in this project")

    def is_archived(self):
        """
            Return True if the project is archived
        """
        return self.archived == 1

    def is_deletable(self):
        """
            Return True if this project could be deleted
        """
        return self.archived == 1 and not self.invoices

    def get_company_id(self):
        return self.company.id

    @staticmethod
    def get_number(task_number, root_str):
        """
            return the number of the given doc
        """
        num = task_number[len(root_str):]
        try:
            return int(num)
        except:
            return 0

    def get_next_estimation_number(self):
        all_nums = [self.get_number(est.number, "Devis ")
                                        for est in self.estimations]
        all_nums.append(len(self.estimations))
        return max(all_nums) + 1

    def get_next_invoice_number(self):
        all_nums = [self.get_number(inv.number, "Facture ")
                                            for inv in self.invoices]
        all_nums.append(len(self.invoices))
        return max(all_nums) + 1

    def get_next_cancelinvoice_number(self):
        all_nums = [self.get_number(cinv.number, "Avoir ")
                                        for cinv in self.cancelinvoices]
        all_nums.append(len(self.cancelinvoices))
        return max(all_nums) + 1

    def todict(self):
        """
            Return a dict view of this object
        """
        phases = [phase.todict() for phase in self.phases]
        return dict(id=self.id,
                    name=self.name,
                    code=self.code,
                    definition=self.definition,
                    type=self.type,
                    archived=self.archived,
                    phases=phases)

class Phase(DBBASE):
    """
        Phase d'un projet
    """
    __tablename__ = 'phase'
    __table_args__ = default_table_args
    id = Column('id', Integer, primary_key=True)
    project_id = Column('project_id', Integer,
                        ForeignKey('project.id'))
    name = Column("name", String(150), default=u'Phase par défaut')
    project = relationship("Project", backref="phases")
    creationDate = deferred(Column("creationDate", CustomDateType,
                                            default=get_current_timestamp))
    updateDate = deferred(Column("updateDate", CustomDateType,
                                        default=get_current_timestamp,
                                        onupdate=get_current_timestamp))

    def is_default(self):
        """
            return True if this phase is a default one
        """
        return self.name in (u'Phase par défaut', u"default", u"défaut",)

    @property
    def estimations(self):
        return self.get_tasks_by_type('estimation')

    @property
    def invoices(self):
        return self.get_tasks_by_type('invoice')

    @property
    def cancelinvoices(self):
        return self.get_tasks_by_type('cancelinvoice')

    def get_tasks_by_type(self, type_):
        """
            return the tasks of the passed type
        """
        return [doc for doc in self.tasks if doc.type_ == type_]

    def todict(self):
        """
            return a dict version of this object
        """
        return dict(id=self.id,
                    name=self.name)

