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
    `IDProject` int(11) NOT NULL auto_increment,
    `name` varchar(150) NOT NULL,
    `customerCode` varchar(4) NOT NULL,
    `type` varchar(150) default NULL,
    `code` varchar(4) NOT NULL,
    `definition` text,
    `creationDate` int(11) NOT NULL,
    `updateDate` int(11) NOT NULL,
    `startingDate` int(11) default NULL,
    `endingDate` int(11) default NULL,
    `status` varchar(20) NOT NULL,
    `IDCompany` int(11) NOT NULL,
    `dispatchType` varchar(10) NOT NULL default 'PERCENT',
    `archived` tinyint(4) NOT NULL default '0',
    PRIMARY KEY  (`IDProject`),
    KEY `IDCompany` (`IDCompany`)
"""
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy.orm import deferred

from autonomie.models.utils import get_current_timestamp
from autonomie.models.types import CustomDateType
from autonomie.models import DBBASE

class Project(DBBASE):
    """
        The project model
    """
    __tablename__ = 'project'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    id = Column('id', Integer, primary_key=True)
    name = Column("name", String(255))
    client_id = Column("client_id", Integer,  ForeignKey('customer.id'))
    code = Column("code", String(4), nullable=False)
    definition = deferred(Column("definition", Text), group='edit')

    id_company = Column("IDCompany", Integer,
                                    ForeignKey('company.IDCompany'))
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

    def get_estimation(self, taskid):
        """
            Returns the estimation with id taskid
        """
        for estimation in self.estimations:
            if estimation.IDTask == int(taskid):
                return estimation
        raise KeyError("No such task in this project")

    def get_invoice(self, taskid):
        """
            Returns the estimation with id taskid
        """
        for invoice in self.invoices:
            if invoice.IDTask == int(taskid):
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
    def get_number(document_number, root_str):
        """
            return the number of the given doc
        """
        num = document_number[len(root_str):]
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
