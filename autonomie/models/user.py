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
    User models
"""
import logging

from hashlib import md5

from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from autonomie.models.base import DBBASE
from autonomie.models.base import default_table_args

ADMIN_PRIMARY_GROUP = 1
MANAGER_PRIMARY_GROUP = 2
CONTRACTOR_PRIMARY_GROUP = 3

COMPANY_EMPLOYEE = Table('company_employee', DBBASE.metadata,
        Column("company_id", Integer, ForeignKey('company.id')),
        Column("account_id", Integer, ForeignKey('accounts.id')),
        mysql_charset=default_table_args['mysql_charset'],
        mysql_engine=default_table_args['mysql_engine'])

log = logging.getLogger(__name__)


class User(DBBASE):
    """
        User model
    """
    __tablename__ = 'accounts'
    __table_args__ = default_table_args
    id = Column('id', Integer, primary_key=True)
    login = Column('login',
            String(64, collation="utf8_bin"),
             unique=True, nullable=False)
    pwd = Column("password", String(100))
    firstname = Column("firstname", String(50))
    lastname = Column("lastname", String(50))
    primary_group = Column("primary_group",
                            Integer)
    active = Column("active", String(1), default='Y')
    email = Column("email", String(100))
    companies = relationship("Company",
                             secondary=COMPANY_EMPLOYEE,
                             backref="employees")
    code_compta = Column("code_compta", String(30),
                         default=0)

    @staticmethod
    def _encode_pass(password):
        """
            Return a md5 encoded password
        """
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        return md5(password).hexdigest()

    def set_password(self, password):
        """
            Set the user's password
        """
        log.info(u"Modifying password : '{0}'".format(self.login))
        self.pwd = self._encode_pass(password)

    def auth(self, password):
        """
            Authentify the current record with password
        """
        if password:
            return self.pwd == self._encode_pass(password)
        return False

    def get_company(self, cid):
        """
            Return the company
        """
        if not isinstance(cid, int):
            cid = int(cid)
        for company in self.companies:
            if company.id == cid:
                return company
        raise KeyError

    def is_admin(self):
        """
            return true if the user is and administrator
        """
        return self.primary_group == ADMIN_PRIMARY_GROUP

    def is_manager(self):
        """
            return True if the user is a manager
        """
        return self.primary_group == MANAGER_PRIMARY_GROUP

    def is_contractor(self):
        """
            return True if the user is a contractor
        """
        return self.primary_group == CONTRACTOR_PRIMARY_GROUP

    @classmethod
    def query(cls, ordered=True):
        """
            Query users
            Exclude archived users
        """
        query = super(User, cls).query()
        query = query.filter(User.active == 'Y')

        if ordered:
            query = query.order_by(User.lastname)

        return query

    def disable(self):
        """
            disable a user
        """
        self.active = "N"

    def enabled(self):
        """
            is he enabled ?
        """
        return self.active == 'Y'

    def __repr__(self):
        return u"<User {s.id} '{s.lastname} {s.firstname}'>".format(s=self)
