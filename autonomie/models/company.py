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
import logging
import datetime

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    Date,
    Boolean,
)
from sqlalchemy.orm import (
    relationship,
    deferred,
    backref,
)

from autonomie_base.models.base import (
    DBBASE,
    DBSESSION,
    default_table_args,
)
from autonomie_base.models.types import (
    PersistentACLMixin,
)

from autonomie.compute import math_utils
from autonomie.models.options import (
    ConfigurableOption,
    get_id_foreignkey_col,
)
from autonomie.models.tools import (
    get_excluded_colanderalchemy,
)
from autonomie.models.services.company import CompanyService
from autonomie.models.user.user import COMPANY_EMPLOYEE

log = logging.getLogger(__name__)


COMPANY_ACTIVITY = Table(
    'company_activity_rel',
    DBBASE.metadata,
    Column("company_id", Integer, ForeignKey('company.id')),
    Column("activity_id", Integer, ForeignKey('company_activity.id')),
    mysql_charset=default_table_args['mysql_charset'],
    mysql_engine=default_table_args['mysql_engine'],
)


class CompanyActivity(ConfigurableOption):
    """
    Company activities
    """
    __colanderalchemy_config__ = {
        'title': u"Domaine d'activité",
        'validation_msg': u"Les domaines d'activité ont bien été configurées",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class Company(DBBASE, PersistentACLMixin):
    """
        Company model
        Store all company specific stuff (headers, logos, RIB, ...)
    """
    __tablename__ = 'company'
    __table_args__ = default_table_args
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(150), nullable=False)
    goal = deferred(
        Column(
            "object",
            String(255),
            default="",
        ),
        group='edit'
    )
    email = deferred(
        Column(
            "email",
            String(255)
        ),
        group='edit',
    )
    phone = deferred(
        Column(
            "phone",
            String(20),
            default=""
        ),
        group='edit'
    )
    mobile = deferred(
        Column(
            "mobile",
            String(20)
        ),
        group='edit'
    )
    comments = deferred(
        Column(
            "comments",
            Text
        ),
        group='edit'
    )

    created_at = deferred(
        Column(
            Date(),
            default=datetime.date.today,
            nullable=False,
        ),
    )
    updated_at = deferred(
        Column(
            Date(),
            default=datetime.date.today,
            onupdate=datetime.date.today,
            nullable=False,
        )
    )
    active = deferred(Column(Boolean(), default=True))
    RIB = deferred(
        Column(
            "RIB",
            String(255)
        ),
        group='edit'
    )
    IBAN = deferred(
        Column(
            "IBAN",
            String(255)
        ),
        group='edit'
    )

    code_compta = deferred(
        Column(
            String(30),
            default=""
        ),
        group="edit",
    )
    contribution = deferred(
        Column(Integer),
        group='edit'
    )

    header_id = Column(
        ForeignKey('file.id'),
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True}
        },
    )
    logo_id = Column(
        ForeignKey('file.id'),
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True}
        },
    )
    cgv = deferred(
        Column(Text, default=''),
        group='edit',
    )
    # Relationships
    header_file = relationship(
        "File",
        primaryjoin="File.id==Company.header_id",
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True}
        },
    )

    logo_file = relationship(
        "File",
        primaryjoin="File.id==Company.logo_id",
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True}
        },
    )

    activities = relationship(
        "CompanyActivity",
        secondary=COMPANY_ACTIVITY,
        backref=backref(
            'companies',
            info={
                'colanderalchemy': {'exclude': True},
                'export': {'exclude': True},
            },
        ),
        info={
            'colanderalchemy': {
                'title': u'Activités',
            },
            'export': {'exclude': True},
        },
    )

    customers = relationship(
        "Customer",
        order_by="Customer.code",
        back_populates="company",
        info={
            'colanderalchemy': {'exclude': True},
            "export": {'exclude': True}
        }
    )

    projects = relationship(
        "Project",
        order_by="Project.id",
        back_populates="company",
        info={
            'colanderalchemy': {'exclude': True},
            "export": {'exclude': True}
        },
    )
    tasks = relationship(
        "Task",
        primaryjoin="Task.company_id==Company.id",
        order_by='Task.date',
        back_populates="company",
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        },
    )
    employees = relationship(
        "User",
        secondary=COMPANY_EMPLOYEE,
        back_populates="companies",
        info={
            'colanderalchemy': get_excluded_colanderalchemy(u'Employés'),
            'export': {'exclude': True}
        },
    )
    sale_catalog = relationship(
        "SaleProductCategory",
        order_by="SaleProductCategory.title",
        back_populates="company",
        info={
            'export': {'exclude': True},
        }
    )
    expense = relationship(
        "ExpenseSheet",
        order_by="ExpenseSheet.month",
        cascade="all, delete-orphan",
        back_populates="company",
        info={
            'export': {'exclude': True},
        }
    )


    _autonomie_service = CompanyService

    def get_company_id(self):
        """
            Return the current company id
            Allows company id access through request's context
        """
        return self.id

    @property
    def header(self):
        return self.header_file

    @header.setter
    def header(self, appstruct):
        if self.header_file is None:
            from autonomie.models.files import File
            self.header_file = File()

        for key, value in appstruct.items():
            setattr(self.header_file, key, value)
        if 'name' not in appstruct:
            self.header_file.name = 'header.png'
        self.header_file.description = 'Header'

    @property
    def logo(self):
        return self.logo_file

    @logo.setter
    def logo(self, appstruct):
        if self.logo_file is None:
            from autonomie.models.files import File
            self.logo_file = File()

        for key, value in appstruct.items():
            setattr(self.logo_file, key, value)
        if 'name' not in appstruct:
            self.logo_file.name = 'logo.png'
        self.logo_file.description = 'Logo'

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
            query = query.filter(cls.active == True)
        return query.order_by(cls.name)

    def __json__(self, request):
        """
            return a dict representation
        """
        customers = [customer.__json__(request) for customer in self.customers]
        projects = [project.__json__(request) for project in self.projects]
        return dict(id=self.id,
                    name=self.name,
                    goal=self.goal,
                    email=self.email,
                    phone=self.phone,
                    mobile=self.mobile,
                    comments=self.comments,
                    RIB=self.RIB,
                    IBAN=self.IBAN,
                    customers=customers,
                    projects=projects)

    def get_tasks(self):
        """
        Get all tasks for this company, as a list
        """
        return self._autonomie_service.get_tasks(self)

    def get_recent_tasks(self, page_nb, nb_per_page):
        """
        :param int nb_per_page: how many to return
        :param int page_nb: pagination index

        .. todo:: this is naive, use sqlalchemy pagination

        :return: pagination for wanted tasks, total nb of tasks
        """
        count = self.get_tasks().count()
        offset = page_nb * nb_per_page
        items = self._autonomie_service.get_tasks(
            self, offset=offset, limit=nb_per_page
        )
        return items, count

    def get_estimations(self, valid=False):
        """
        Return the estimations of the current company
        """
        return self._autonomie_service.get_estimations(self, valid)

    def get_invoices(self, valid=False):
        """
        Return the invoices of the current company
        """
        return self._autonomie_service.get_invoices(self, valid)

    def get_cancelinvoices(self, valid=False):
        """
        Return the cancelinvoices of the current company
        """
        return self._autonomie_service.get_cancelinvoices(self, valid)

    def has_invoices(self):
        """
            return True if this company owns invoices
        """
        return self.get_invoices(self, valid=True).count() > 0 or \
            self.get_cancelinvoices(self, valid=True).count() > 0

    def get_real_customers(self, year):
        """
        Return the real customers (with invoices)
        """
        return self._autonomie_service.get_customers(self, year)

    def get_late_invoices(self):
        """
        Return invoices waiting for more than 45 days
        """
        return self._autonomie_service.get_late_invoices(self)

    def get_customer_codes_and_names(self):
        """
        Return current company's customer codes and names
        """
        return self._autonomie_service.get_customer_codes_and_names(self)

    def get_project_codes_and_names(self):
        """
        Return current company's project codes and names
        """
        return self._autonomie_service.get_project_codes_and_names(self)

    def get_next_estimation_index(self):
        """
        Return the next estimation index
        """
        return self._autonomie_service.get_next_estimation_index(self)

    def get_next_invoice_index(self):
        """
        Return the next invoice index
        """
        return self._autonomie_service.get_next_invoice_index(self)

    def get_next_cancelinvoice_index(self):
        """
        Return the next cancelinvoice index
        """
        return self._autonomie_service.get_next_cancelinvoice_index(self)

    def get_turnover(self, year):
        """
        Retrieve the annual turnover for the current company

        :param int year: The current year
        """
        ca = self._autonomie_service.get_turnover(self, year)
        return math_utils.integer_to_amount(ca, precision=5)

    @classmethod
    def label_query(cls):
        return cls._autonomie_service.label_query(cls)


    @classmethod
    def get_id_by_analytical_account(cls, analytical_account):
        return cls._autonomie_service.get_id_by_analytical_account(
            cls,
            analytical_account
        )
