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
import colander
import deform_bootstrap
import deform
from autonomie import deform_extend

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import (
    relationship,
    deferred,
    backref,
)

from autonomie import forms
from autonomie.models.utils import get_current_timestamp
from autonomie.models.types import (
    CustomDateType,
    CustomFileType,
)

from autonomie.models.base import (
    DBBASE,
    DBSESSION,
    default_table_args,
)

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
    goal = deferred(
        Column(
            "object",
            String(255)
        ),
        group='edit'
    )
    email = deferred(
        Column(
            "email",
            String(255)
        ),
        group='edit'
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
    creationDate = deferred(
        Column(
            "creationDate",
            CustomDateType,
            default=get_current_timestamp
        )
    )
    updateDate = deferred(
        Column(
            "updateDate",
            CustomDateType,
            default=get_current_timestamp,
            onupdate=get_current_timestamp
        )
    )
    active = deferred(
        Column(
            "active",
            String(1),
            default="Y")
    )
    logo = deferred(
        Column(
            "logo",
            CustomFileType("logo_", 255)
        ),
        group='edit'
    )
    header = deferred(
        Column(
            "header",
            CustomFileType("header_", 255)
        ),
        group='edit'
    )
    logoType = deferred(
        Column(
            "logoType",
            String(255)
        )
    )
    headerType = deferred(
        Column(
            "headerType",
            String(255)
        )
    )
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
    customers = relationship(
        "Customer",
        order_by="Customer.code",
        backref=backref(
            'company',
            info={'colanderalchemy': forms.EXCLUDED},
        )
    )
    projects = relationship(
        "Project",
        order_by="Project.id",
        backref=backref("company", info={'colanderalchemy': forms.EXCLUDED}),
    )
    code_compta = deferred(
        Column(
            String(30),
            default=0
        ),
        group="edit",
    )
    contribution = deferred(
        Column(Integer),
        group='edit'
    )

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


# Company node related tools
def get_deferred_company_choices(widget_options):
    """
    Build a deferred for company selection widget
    """
    default_entry = widget_options.pop('default', None)
    @colander.deferred
    def deferred_company_choices(node, kw):
        """
        return a deferred company selection widget
        """
        values = [(comp.id, comp.name) for comp in Company.query()]
        if default_entry is not None:
            values.insert(0, default_entry)
        return deform_bootstrap.widget.ChosenSingleWidget(
            values=values,
            placeholder=u"Sélectionner une entreprise",
            **widget_options
            )
    return deferred_company_choices


def company_node(**kw):
    """
    Return a schema node for company selection
    """
    widget_options = kw.pop('widget_options', {})
    return colander.SchemaNode(
        colander.Integer(),
        widget=get_deferred_company_choices(widget_options),
        **kw
        )


# Customer node related tools
@colander.deferred
def deferred_fullcustomer_list_widget(node, kw):
    values = [('', '')]
    for comp in Company.query():
        values.append(
            deform.widget.OptGroup(
                comp.name,
                *[(cust.id, cust.name) for cust in comp.customers]
            )
        )
    return deform_extend.CustomChosenOptGroupWidget(
        values=values,
        placeholder=u"Sélectionner un client"
        )


@colander.deferred
def deferred_customer_list_widget(node, kw):
    values = [(-1, u''), ]
    company = kw['request'].context
    values.extend(((cust.id, cust.name) for cust in company.customers))
    return deform_bootstrap.widget.ChosenSingleWidget(
        values=values,
        placeholder=u'Sélectionner un client',
    )


@colander.deferred
def deferred_company_customer_validator(node, kw):
    """
    Ensure we don't query customers from other companies
    """
    company = kw['request'].context
    values = [-1]
    values.extend([customer.id for customer in company.customers])
    return colander.OneOf(values)


def customer_node(is_admin=False):
    """
    return a customer selection node

        is_admin

            is the associated view restricted to company's invoices
    """
    if is_admin:
        deferred_customer_widget = deferred_fullcustomer_list_widget
        deferred_customer_validator = None
    else:
        deferred_customer_widget = deferred_customer_list_widget
        deferred_customer_validator = deferred_company_customer_validator

    return colander.SchemaNode(
            colander.Integer(),
            name='customer_id',
            widget=deferred_customer_widget,
            validator=deferred_customer_validator,
            missing=-1,
        )
