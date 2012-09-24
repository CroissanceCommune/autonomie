# -*- coding: utf-8 -*-
# * File Name : user.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 25-07-2012
# * Last Modified :
#
# * Project :
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

from autonomie.models import DBBASE

COMPANY_EMPLOYEE = Table('company_employee', DBBASE.metadata,
    Column("company_id", Integer, ForeignKey('company.id')),
    Column("account_id", Integer, ForeignKey('accounts.id')),
        mysql_charset='utf8', mysql_engine='MyISAM')

log = logging.getLogger(__name__)


class User(DBBASE):
    """
        User model
    """
    __tablename__ = 'accounts'
    __table_args__ = {'mysql_engine': 'MyISAM', "mysql_charset": 'utf8'}
    id = Column('id', Integer, primary_key=True)
    login = Column('login', String(64))
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
        if type(password) == unicode:
            password = password.encode('utf-8')
        return md5(password).hexdigest()

    def set_password(self, password):
        """
            Set the user's password
        """
        self.pwd = self._encode_pass(password)

    def auth(self, password):
        """
            Authentify the current record with password
        """
        if password:
            return self.pwd == self._encode_pass(password)
        else:
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
        return self.primary_group == 1

    def is_manager(self):
        """
            return True if the user is a manager
        """
        return self.primary_group == 2

    def is_contractor(self):
        """
            return True if the user is a contractor
        """
        return self.primary_group == 3

    @classmethod
    def query(cls, ordered=True):
        """
            Query users
            Exclud archived users
        """
        query = super(User, cls).query()
        query = query.filter(User.active=='Y')
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
