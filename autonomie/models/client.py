# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 04-09-2012
# * Last Modified :
#
# * Project :
#
"""
    Client model : represents customers
"""
import logging
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import deferred

from autonomie.models.types import CustomDateType
from autonomie.models.utils import get_current_timestamp
from autonomie.models import DBBASE
log = logging.getLogger(__name__)

class Client(DBBASE):
    """
        Client model
    """
    __tablename__ = 'customer'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset":'utf8'}
    id = Column('id', Integer, primary_key=True)
    code = Column('code', String(4))
    comments = deferred(Column("comments", Text), group='edit')
    creationDate = Column("creationDate", CustomDateType,
                                            default=get_current_timestamp)
    updateDate = Column("updateDate", CustomDateType,
                                        default=get_current_timestamp,
                                        onupdate=get_current_timestamp)
    company_id = Column("company_id", Integer,
                                    ForeignKey('company.id'))
    intraTVA = deferred(Column("intraTVA", String(50)), group='edit')
    address = deferred(Column("address", String(255)), group='edit')
    zipCode = deferred(Column("zipCode", String(20)), group='edit')
    city = deferred(Column("city", String(255)), group='edit')
    country = deferred(Column("country", String(150)), group='edit')
    phone = deferred(Column("phone", String(50)), group='edit')
    email = deferred(Column("email", String(255)), group='edit')
    contactLastName = deferred(Column("contactLastName",
                    String(255), default=None), group='edit')
    name = Column("name", String(255), default=None)
    contactFirstName = deferred(Column("contactFirstName",
                    String(255), default=None), group='edit')
    projects = relationship("Project", backref="client")

    def get_company_id(self):
        """
            return the id of the company this client belongs to
        """
        return self.company.id

    def todict(self):
        """
            Return a dict version of the client object
        """
        projects = [project.todict() for project in self.projects]
        return dict(id=self.id,
                    code=self.code,
                    comments=self.comments,
                    intraTVA=self.intraTVA,
                    address=self.address,
                    zipCode=self.zipCode,
                    city=self.city,
                    country=self.country,
                    phone=self.phone,
                    email=self.email,
                    contactLastName=self.contactLastName,
                    contactFirstName=self.contactFirstName,
                    name=self.name,
                    projects=projects
                    )
