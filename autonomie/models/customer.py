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
    Customer model : represents customers
    Stores the company and its main contact

    >>> from autonomie.models.customer import Customer
    >>> c = Customer()
    >>> c.lastname = u"Dupont"
    >>> c.firstname = u"Jean"
    >>> c.name = u"Compagnie Dupont avec un t"
    >>> c.code = u"DUPT"
    >>> DBSESSION.add(c)

"""
import datetime
import logging

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    ForeignKey,
    Date,
)
from sqlalchemy.orm import (
    deferred,
    relationship,
)
from sqlalchemy.event import listen
from autonomie_base.models.types import (
    PersistentACLMixin,
)
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie.models.services.customer import CustomerService

log = logging.getLogger(__name__)


class Customer(DBBASE, PersistentACLMixin):
    """
        Customer model
        Stores the company and its main contact
        :param name: name of the company
        :param code: internal code of the customer (unique regarding the owner)
        :param multiline address: address of the company
        :param zip_code: zipcode of the company
        :param city: city
        :param country: country, default France
        :param lastname: lastname of the contact
        :param firstname: firstname of the contact
        :param function: function of the contact
    """
    __tablename__ = 'customer'
    __table_args__ = default_table_args
    id = Column(
        'id',
        Integer,
        primary_key=True,
        info={
            'colanderalchemy': {
                'exclude': True,
                'title': u"Identifiant Autonomie",
            }
        },
    )
    type_ = Column(
        'type_',
        String(10),
        default='company',
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        }
    )

    created_at = deferred(
        Column(
            Date(),
            default=datetime.date.today,
            info={
                'export': {'exclude': True},
                'colanderalchemy': {'exclude': True},
            },
            nullable=False,
        ),
        group='all',
    )

    updated_at = deferred(
        Column(
            Date(),
            default=datetime.date.today,
            onupdate=datetime.date.today,
            info={
                'export': {'exclude': True},
                'colanderalchemy': {'exclude': True},
            },
            nullable=False,
        ),
        group='all',
    )

    company_id = Column(
        "company_id",
        Integer,
        ForeignKey('company.id'),
        info={
            'export': {'exclude': True},
            'colanderalchemy': {'exclude': True},
        },
        nullable=False,
    )

    label = Column(
        "label",
        String(255),
        info={
            'colanderalchemy': {'exclude': True},
        },
        default='',
    )

    name = Column(
        "name",
        String(255),
        info={
            "colanderalchemy": {
                'title': u'Nom de la structure',
            },
        },
        default='',
    )

    code = Column(
        'code',
        String(4),
        info={'colanderalchemy': {'title': u"Code client"}},
    )

    civilite = deferred(
        Column(
            'civilite',
            String(10),
            info={
                'colanderalchemy': {
                    'title': u"Civilité",
                }
            }
        ),
        group='edit',
    )

    lastname = deferred(
        Column(
            "lastname",
            String(255),
            info={
                "colanderalchemy": {
                    'title': u"Nom du contact principal",
                }
            },
            nullable=False,
        ),
        group='edit',
    )

    firstname = deferred(
        Column(
            "firstname",
            String(255),
            info={
                'colanderalchemy': {
                    'title': u"Prénom du contact principal",
                }
            },
            default="",
        ),
        group='edit',
    )

    function = deferred(
        Column(
            "function",
            String(255),
            info={
                'colanderalchemy': {
                    'title': u"Fonction du contact principal",
                }
            },
            default='',
        ),
        group="edit",
    )

    address = deferred(
        Column(
            "address",
            String(255),
            info={
                'colanderalchemy': {
                    'title': u'Adresse',
                }
            },
            nullable=False,
        ),
        group='edit'
    )

    zip_code = deferred(
        Column(
            "zip_code",
            String(20),
            info={
                'colanderalchemy': {
                    'title': u'Code postal',
                },
            },
            nullable=False,
        ),
        group='edit',
    )

    city = deferred(
        Column(
            "city",
            String(255),
            info={
                'colanderalchemy': {
                    'title': u'Ville',
                }
            },
            nullable=False,
        ),
        group='edit',
    )

    country = deferred(
        Column(
            "country",
            String(150),
            info={
                'colanderalchemy': {'title': u'Pays'},
            },
            default=u'France',
        ),
        group='edit',
    )

    email = deferred(
        Column(
            "email",
            String(255),
            info={
                'colanderalchemy': {
                    'title': u"Adresse de messagerie",
                },
            },
            default='',
        ),
        group='edit',
    )
    mobile = deferred(
        Column(
            "mobile",
            String(20),
            info={
                'colanderalchemy': {
                    'title': u"Téléphone portable",
                },
            },
            default='',
        ),
        group='edit',
    )

    phone = deferred(
        Column(
            "phone",
            String(50),
            info={
                'colanderalchemy': {
                    'title': u'Téléphone fixe',
                },
            },
            default='',
        ),
        group='edit',
    )

    fax = deferred(
        Column(
            "fax",
            String(50),
            info={
                'colanderalchemy': {
                    'title': u'Fax',
                }
            },
            default='',
        ),
        group="edit"
    )

    tva_intracomm = deferred(
        Column(
            "tva_intracomm",
            String(50),
            info={
                'colanderalchemy': {'title': u"TVA intracommunautaire"},
            },
            default='',
        ),
        group='edit',
    )

    comments = deferred(
        Column(
            "comments",
            Text,
            info={
                'colanderalchemy': {
                    'title': u"Commentaires",
                }
            },
        ),
        group='edit',
    )

    compte_cg = deferred(
        Column(
            String(125),
            info={
                'export': {'exclude': True},
                'colanderalchemy': {
                    'title': u"Compte CG",
                },
            },
            default="",
        ),
        group="edit",
    )

    compte_tiers = deferred(
        Column(
            String(125),
            info={
                'export': {'exclude': True},
                'colanderalchemy': {
                    'title': u"Compte tiers",
                }
            },
            default="",
        ),
        group="edit",
    )
    archived = Column(
        Boolean(),
        default=False,
        info={'colanderalchemy': {'exclude': True}},
    )

    company = relationship(
        "Company",
        primaryjoin="Company.id==Customer.company_id",
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        }
    )

    estimations = relationship(
        "Estimation",
        primaryjoin="Estimation.customer_id==Customer.id",
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        }

    )

    invoices = relationship(
        "Invoice",
        primaryjoin="Invoice.customer_id==Customer.id",
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        }

    )

    cancelinvoices = relationship(
        "CancelInvoice",
        primaryjoin="CancelInvoice.customer_id==Customer.id",
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        }

    )

    _autonomie_service = CustomerService

    def get_company_id(self):
        """
            :returns: the id of the company this customer belongs to
        """
        return self.company.id

    def __json__(self, request):
        """
            :returns: a dict version of the customer object
        """
        projects = [project.__json__(request) for project in self.projects]
        return dict(
            id=self.id,
            code=self.code,
            comments=self.comments,
            tva_intracomm=self.tva_intracomm,
            address=self.address,
            zip_code=self.zip_code,
            city=self.city,
            country=self.country,
            phone=self.phone,
            email=self.email,
            lastname=self.lastname,
            firstname=self.firstname,
            name=self.name,
            projects=projects,
            full_address=self.full_address,
            archived=self.archived,
            company_id=self.company_id,
        )

    @property
    def full_address(self):
        """
            :returns: the customer address formatted in french format
        """
        return self._autonomie_service.get_address(self)

    def has_tasks(self):
        return self._autonomie_service.count_tasks(self) > 0

    def is_deletable(self):
        """
            Return True if this project could be deleted
        """
        return self.archived and not self.has_tasks()

    def is_company(self):
        return self.type_ == 'company'

    def _get_label(self):
        return self._autonomie_service.get_label(self)

    def get_name(self):
        return self._autonomie_service.format_name(self)

    @classmethod
    def check_project_id(cls, customer_id, project_id):
        """
        Check the project and the customer are linked

        :param int customer_id: The customer id
        :param int project_id: The project id
        :returns: True if the customer is attached to the project
        :rtype: bool
        """
        return cls._autonomie_service.check_project_id(customer_id, project_id)

    @classmethod
    def label_query(cls):
        return cls._autonomie_service.label_query(cls)

    def get_project_ids(self):
        return self._autonomie_service.get_project_ids(self)


COMPANY_FORM_GRID = (
    (
        ('name', 4,), ('code', 4),
    ),
    (
        ('civilite', 8),
    ),
    (
        ('lastname', 4),
        ('firstname', 4),),
    (
        ('function', 4),
    ),
    (
        ('address', 6),
    ),
    (
        ('zip_code', 2), ('city', 4),
    ),
    (
        ('country', 4),
    ),
    (
        ('tva_intracomm', 4),
    ),
    (
        ('email', 4),
    ),
    (
        ('mobile', 4),
    ),
    (
        ('phone', 4),
    ),
    (
        ('fax', 4),
    ),
    (
        ('comments', 10),
    ),
    (
        ('compte_cg', 4),
        ('compte_tiers', 4),
    )
)


INDIVIDUAL_FORM_GRID = (
    (
        ('code', 6),
    ),
    (
        ('civilite', 8),
    ),
    (
        ('lastname', 4),
        ('firstname', 4),
    ),
    (
        ('address', 6),
    ),
    (
        ('zip_code', 2), ('city', 4),
    ),
    (
        ('country', 4),
    ),
    (
        ('email', 4),
    ),
    (
        ('mobile', 4),
    ),
    (
        ('phone', 4),
    ),
    (
        ('fax', 4),
    ),
    (
        ('comments', 10),
    ),
    (
        ('compte_cg', 4),
        ('compte_tiers', 4),
    )
)


def set_customer_label(mapper, connection, target):
    """
    Set the label of the given customer
    """
    target.label = target._get_label()


listen(Customer, "before_insert", set_customer_label)
listen(Customer, "before_update", set_customer_label)
