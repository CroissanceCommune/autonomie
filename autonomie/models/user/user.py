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

import logging


from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
)

from sqlalchemy.orm import (
    relationship,
    backref,
    deferred,
)
from sqlalchemy.event import listen

from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
    DBSESSION,
)
from autonomie_base.models.types import (
    JsonEncodedDict,
    PersistentACLMixin,
)
from autonomie_base.consts import (
    CIVILITE_OPTIONS,
)

from autonomie.utils.strings import (
    format_name,
)
from autonomie.models.tools import (
    set_attribute,
    get_excluded_colanderalchemy,
)


COMPANY_EMPLOYEE = Table(
    'company_employee',
    DBBASE.metadata,
    Column("company_id", Integer, ForeignKey('company.id'), nullable=False),
    Column("account_id", Integer, ForeignKey('accounts.id'), nullable=False),
    mysql_charset=default_table_args['mysql_charset'],
    mysql_engine=default_table_args['mysql_engine'],
)


log = logging.getLogger(__name__)


class User(DBBASE, PersistentACLMixin):
    """
        User model
    """
    __tablename__ = 'accounts'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': {'exclude': True}},
    )
    civilite = Column(
        String(10),
        info={
            'colanderalchemy': {
                'title': u'Civilité',
            }
        },
        default=CIVILITE_OPTIONS[0][0],
        nullable=False,
    )

    lastname = Column(
        String(50),
        info={'colanderalchemy': {'title': u'Nom'}},
        nullable=False,
    )

    firstname = Column(
        String(50),
        info={'colanderalchemy': {'title': u'Prénom'}},
        nullable=False,
    )

    email = deferred(
        Column(
            String(100),
            info={
                'colanderalchemy': {
                    'title': u"Adresse e-mail",
                }
            },
            nullable=False,
        ),
        group='edit',
    )

    companies = relationship(
        "Company",
        secondary=COMPANY_EMPLOYEE,
        backref=backref(
            "employees",
            info={
                'colanderalchemy': get_excluded_colanderalchemy(u'Employés'),
                'export': {'exclude': True}
            },
        ),
        info={
            'colanderalchemy': get_excluded_colanderalchemy(u'Entreprises'),
            'export': {'exclude': True}
        },
    )

    compte_tiers = deferred(
        Column(
            String(30),
            info={
                'colanderalchemy':
                {
                    'title': u'Compte tiers pour note de dépense',
                }
            },
            default="",
        ),
        group="edit",
    )

    vehicle = deferred(
        Column(
            String(66),  # 50 + 1 + 15
            nullable=True,
            info={
                'colanderalchemy':
                {
                    'title': u'Type de véhicule',
                    'description': (
                        u"Permet de restreindre les frais "
                        u"kilométriques déclarables par l'entrepreneur"
                    ),
                }
            },
        )
    )

    session_datas = deferred(
        Column(
            JsonEncodedDict,
            info={
                'colanderalchemy': {'exclude': True},
                'export': {'exclude': True}
            },
            default=None,
        ),
        group="edit"
    )

    userdatas = relationship(
        "UserDatas",
        primaryjoin='User.id==UserDatas.user_id',
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan',
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        }
    )
    trainerdatas = relationship(
        "TrainerDatas",
        back_populates="user",
        uselist=False,
        cascade='all, delete-orphan',
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        }
    )
    login = relationship(
        "Login",
        back_populates="user",
        uselist=False,
        cascade='all, delete-orphan',
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        }
    )

    @classmethod
    def find_user(cls, value, *args, **kw):
        """
        Try to find a user instance based on the given value

        :param str value: The value that should match a user
        """
        result = cls.query().join(cls.login).filter_by(login=value).first()

        if result is None:
            value = value.split(' ')
            if len(value) >= 2:
                firstname = value[-1]
                lastname = " ".join(value[:-1])
                try:
                    query = cls.query()
                    query = query.filter_by(lastname=lastname)
                    query = query.filter_by(firstname=firstname)
                    result = query.one()
                except:
                    result = None
        return result

    def get_company(self, cid):
        """
        Retrieve the user's company with id cid

        :param int cid: The user's company id
        :returns: A Company instance
        :raises: `sqlalchemy.orm.exc.NoResultFound` if no company can be found
        """
        from autonomie.models.company import Company
        if not isinstance(cid, int):
            cid = int(cid)

        query = DBSESSION().query(Company)
        query = query.filter(Company.employees.any(User.id == self.id))
        query = query.filter(Company.id == cid)
        return query.one()

    def has_userdatas(self):
        """
        Return True if the current object has userdatas associated to it
        """
        from autonomie.models.user.userdatas import UserDatas
        query = DBSESSION().query(UserDatas.id)
        query = query.filter(UserDatas.user_id == self.id)
        count = query.count()
        return count >= 1

    def __unicode__(self):
        return u"<User {s.id} '{s.lastname} {s.firstname}'>".format(s=self)

    def __repr__(self):
        return self.__unicode__().encode('utf-8')

    def __json__(self, request):
        return dict(
            civilite=self.civilite,
            lastname=self.lastname,
            firstname=self.firstname,
        )

    @property
    def label(self):
        return format_name(self.firstname, self.lastname)

    @property
    def active_companies(self):
        """
        Return only enabled companies
        """
        return [company for company in self.companies if company.active]


# Registering event handlers to keep datas synchronized
def sync_user_to_userdatas(source_key, userdatas_key):
    def handler(target, value, oldvalue, initiator):
        parentclass = initiator.parent_token.parent.class_
        if parentclass is User:
            if source_key == initiator.key:
                if target.userdatas is not None:
                    set_attribute(
                        target.userdatas, userdatas_key, value, initiator
                    )
    return handler


listen(
    User.firstname,
    'set',
    sync_user_to_userdatas('firstname', 'coordonnees_firstname')
)
listen(
    User.lastname,
    'set',
    sync_user_to_userdatas('lastname', 'coordonnees_lastname')
)
listen(
    User.email,
    'set',
    sync_user_to_userdatas('email', 'coordonnees_email1')
)
