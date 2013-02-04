# -*- coding: utf-8 -*-
# * File Name : project.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 23-08-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Project model
"""
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy.orm import deferred
from sqlalchemy.orm import relationship

from autonomie.models.utils import get_current_timestamp
from autonomie.models.types import CustomDateType
from autonomie.models.base import DBBASE
from autonomie.models.base import default_table_args

ProjectClient = Table('project_client', DBBASE.metadata,
        Column("project_id", Integer, ForeignKey('project.id')),
        Column("client_id", Integer, ForeignKey('customer.id')),
        mysql_charset=default_table_args['mysql_charset'],
        mysql_engine=default_table_args['mysql_engine'])

class Project(DBBASE):
    """
        The project model
    """
    __tablename__ = 'project'
    __table_args__ = default_table_args
    id = Column('id', Integer, primary_key=True)
    name = Column("name", String(255))
    client_id = Column("client_id", Integer,  ForeignKey('customer.id'))
    code = Column("code", String(4), nullable=False)
    definition = deferred(Column("definition", Text), group='edit')

    company_id = Column("company_id", Integer,
                                    ForeignKey('company.id'))
    creationDate = deferred(Column("creationDate", CustomDateType,
                                            default=get_current_timestamp))
    updateDate = deferred(Column("updateDate", CustomDateType,
                                        default=get_current_timestamp,
                                        onupdate=get_current_timestamp))
    startingDate = deferred(Column("startingDate", CustomDateType,
                                default=get_current_timestamp), group='edit')
    endingDate = deferred(Column("endingDate", CustomDateType,
                                default=get_current_timestamp), group='edit')

    type = deferred(Column('type', String(150)), group='edit')
    archived = Column("archived", String(255), default=0)

    clients = relationship("Client",
                            secondary=ProjectClient,
                            backref='projects')

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

