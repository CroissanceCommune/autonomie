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
    Company model
"""
import os
import logging

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import deferred

from autonomie.models.utils import get_current_timestamp
from autonomie.models.types import CustomDateType
from autonomie.models.types import CustomFileType

from autonomie.models.base import DBBASE
from autonomie.models.base import DBSESSION
from autonomie.models.base import default_table_args

log = logging.getLogger(__name__)


class Company(DBBASE):
    """
        Company model
        Store all company specific stuff (headers, logos, RIB, ...)
    """
    __tablename__ = 'company'
    __table_args__ = default_table_args
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(150))
    goal = deferred(Column("object", String(255)),
            group='edit')
    email = deferred(Column("email", String(255)),
            group='edit')
    phone = deferred(Column("phone", String(20), default=""),
            group='edit')
    mobile = deferred(Column("mobile", String(20)),
            group='edit')
    comments = deferred(Column("comments", Text),
            group='edit')
    creationDate = deferred(Column("creationDate", CustomDateType,
                                            default=get_current_timestamp))
    updateDate = deferred(Column("updateDate", CustomDateType,
                                        default=get_current_timestamp,
                                        onupdate=get_current_timestamp))
    active = deferred(Column("active", String(1), default="Y"))
    logo = deferred(Column("logo", CustomFileType("logo_", 255)),
            group='edit')
    header = deferred(Column("header", CustomFileType("header_", 255)),
            group='edit')
    logoType = deferred(Column("logoType", String(255)))
    headerType = deferred(Column("headerType", String(255)))
    RIB = deferred(Column("RIB", String(255)),
            group='edit')
    IBAN = deferred(Column("IBAN", String(255)),
            group='edit')
    customers = relationship("Customer",
                            order_by="Customer.code",
                            backref='company')
    projects = relationship("Project",
                            order_by="Project.id",
                            backref="company")
    code_compta = deferred(Column(String(30), default=0), group="edit")
    contribution = deferred(Column(Integer), group='edit')

    def get_path(self):
        """
            get the relative filepath specific to the given company
        """
        return os.path.join("company", str(self.id))

    def get_header_filepath(self):
        """
            Returns the header's relative filepath
        """
        if self.header:
            return os.path.join(self.get_path(),
                            'header',
                            self.header['filename'])
        else:
            return None

    def get_logo_filepath(self):
        """
            Return the logo's relative filepath
        """
        if self.logo:
            return os.path.join(self.get_path(),
                            'logo',
                             self.logo['filename'])
        else:
            return None

    def get_company_id(self):
        """
            Return the current company id
            Allows company id access through request's context
        """
        return self.id

    @classmethod
    def query(cls, keys=None, active=True):
        """
            Return a query
        """
        if keys:
            query = DBSESSION().query(*keys)
        else:
            query = super(Company, cls).query()
        if active:
            query = query.filter(cls.active == "Y")
        return query.order_by(cls.name)

    def disable(self):
        """
            Disable the current company
        """
        self.active = "N"

    def enable(self):
        """
            enable a company
        """
        self.active = "Y"

    def enabled(self):
        return self.active == 'Y'

    def has_invoices(self):
        """
            return True if this company owns invoices
        """
        for project in self.projects:
            for invoice in project.invoices:
                if invoice.has_been_validated():
                    return True
        return False

    def todict(self):
        """
            return a dict representation
        """
        customers = [customer.todict() for customer in self.customers]
        projects = [project.todict() for project in self.projects]
        return dict(id=self.id,
                    name=self.name,
                    goal=self.goal,
                    email=self.email,
                    phone=self.phone,
                    mobile=self.mobile,
                    comments=self.comments,
                    RIB=self.RIB,
                    IBAN=self.IBAN,
                    logo=self.get_logo_filepath(),
                    header=self.get_header_filepath(),
                    customers=customers,
                    projects=projects)

    def get_tasks(self):
        """
        Get all tasks for this company, as a list
        """
        tasks = []
        for project in self.projects:
            tasks.extend(project.estimations)
            tasks.extend(project.invoices)
        return tasks

    def get_recent_tasks(self, page_nb, nb_per_page):
        """
        :param int nb_per_page: how many to return
        :param int page_nb: pagination index

        .. todo:: this is naive, use sqlalchemy pagination

        :return: pagination for wanted tasks, total nb of tasks
        """
        all_tasks = sorted(self.get_tasks(),
                        key=lambda t: t.statusDate,
                        reverse=True)
        offset = page_nb * nb_per_page
        return all_tasks[offset:offset + nb_per_page], len(all_tasks)
