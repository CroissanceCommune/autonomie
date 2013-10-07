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
    Root factory <=> Acl handling
"""
import logging
from pyramid.security import Allow
from pyramid.security import Authenticated
from pyramid.security import ALL_PERMISSIONS
from sqlalchemy.orm import undefer_group

from autonomie.models.project import Project
from autonomie.models.company import Company
from autonomie.models.client import Client
from autonomie.models.task.estimation import Estimation
from autonomie.models.task.invoice import Invoice
from autonomie.models.task.invoice import CancelInvoice
from autonomie.models.user import User
from autonomie.models.treasury import ExpenseSheet

log = logging.getLogger(__name__)

MANAGER_ROLES = (
    (u"3", u'Entrepreneur'),
    (u"2", u'Membre de la coopérative'),
)
ADMIN_ROLES = (
    (u"3", u'Entrepreneur'),
    (u"1", u'Administrateur'),
    (u"2", u'Membre de la coopérative'),
)

DEFAULT_PERM = [
    (Allow, "group:admin", ALL_PERMISSIONS,),
    (Allow, "group:manager", ("manage", "add", "edit", "view")),
]


class RootFactory(dict):
    """
       Ressource factory, returns the appropriate resource regarding
       the request object
    """
    __name__ = "root"

    @property
    def __acl__(self):
        """
            Default permissions
        """
        acl = DEFAULT_PERM[:]
        acl.append((Allow, Authenticated, 'view',))
        return acl

    def __init__(self, request):
        self.request = request
        self['companies'] = CompanyFactory(self, "companies")
        self['projects'] = ProjectFactory(self, 'projects')
        self['clients'] = ClientFactory(self, 'clients')
        self['estimations'] = EstimationFactory(self, 'estimations')
        self['invoices'] = InvoiceFactory(self, 'invoices')
        self['cancelinvoices'] = CancelInvoiceFactory(self, 'cancelinvoices')
        self['users'] = UserFactory(self, 'users')
        self['expenses'] = ExpenseSheetFactory(self, "expenses")


class BaseDBFactory(object):
    """
        Base class for dbrelated objects
    """
    __acl__ = DEFAULT_PERM[:]
    dbsession = None
    def __init__(self, parent, name):
        self.__parent__ = parent
        self.__name__ = name


    def _get_item(self, klass, key, object_name):
        assert self.dbsession is not None, "Missing dbsession"

        dbsession = self.dbsession()
        obj = dbsession.query(klass)\
                       .options(undefer_group('edit'))\
                       .filter(klass.id == key)\
                       .scalar()

        if obj is None:
            raise KeyError

        obj.__name__ = object_name
        return obj


class CompanyFactory(BaseDBFactory):
    """
        Handle access to a project
    """
    def __getitem__(self, key):
        """
            Returns the traversed object
        """
        return self._get_item(Company, key, "company")


class ProjectFactory(BaseDBFactory):
    """
        Handle access to a project
    """
    def __getitem__(self, key):
        """
            Returns the traversed object
        """
        return self._get_item(Project, key, 'project')


class ClientFactory(BaseDBFactory):
    """
        Handle access to a client
    """
    def __getitem__(self, key):
        """
            Returns the traversed object
        """
        return self._get_item(Client, key, 'client')


class EstimationFactory(BaseDBFactory):
    """
        Handle access to a client
    """
    def __getitem__(self, key):
        """
            Returns the traversed object
        """
        return self._get_item(Estimation, key, 'estimation')


class InvoiceFactory(BaseDBFactory):
    """
        Handle access to an invoice
    """
    def __getitem__(self, key):
        """
            Returns the traversed object
        """
        return self._get_item(Invoice, key, 'invoice')


class CancelInvoiceFactory(BaseDBFactory):
    """
        Handle access to a cancelinvoice
    """
    def __getitem__(self, key):
        """
            Returns the traversed object
        """
        return self._get_item(CancelInvoice, key, 'cancelinvoice')


class UserFactory(BaseDBFactory):
    """
        Handle access to a user account
    """
    def __getitem__(self, key):
        """
            Returns the traversed object
        """
        return self._get_item(User, key, 'user')


class ExpenseSheetFactory(BaseDBFactory):
    """
        Handle access to expense sheets
    """
    def __getitem__(self, key):
        """
            Returns the traversed object
        """
        return self._get_item(ExpenseSheet, key, "expensesheet")


def get_base_acl(self):
    """
        return the base acls
    """
    acl = DEFAULT_PERM[:]
    return acl


def get_company_acl(self):
    """
        Compute the company's acls
    """
    acl = DEFAULT_PERM[:]
    acl.append((Allow, Authenticated, 'view',))
    acl.extend(
        [(Allow,
          u"%s" % user.login,
          ("view", "edit", "add"))
         for user in self.employees]
    )
    return acl


def get_user_acl(self):
    """
        Get acls for user account edition
    """
    acl = DEFAULT_PERM[:]
    acl.append(
        (Allow,
         u"%s" % self.login,
         ("view", "edit", "add"))
    )
    acl.append((Allow, Authenticated, ('view')))
    return acl


def get_task_acl(self):
    """
        return the acls of the current task object
    """
    acl = DEFAULT_PERM[:]
    acl.extend(
        [(Allow,
          u"%s" % user.login,
          ("view", "edit", "add"))
         for user in self.project.company.employees]
    )
    return acl


def get_client_or_project_acls(self):
    """
        Compute the project's acls
    """
    acl = DEFAULT_PERM[:]
    acl.extend(
        [(Allow,
          u"%s" % user.login,
          ("view", "edit", "add"))
         for user in self.company.employees]
    )
    return acl


def get_expensesheet_acl(self):
    """
        Compute the expense Sheet acl
    """
    if self.status in ('draft', 'invalid'):
        user_rights = ("view", "edit", "add")
    else:
        user_rights = ("view",)
    acl = DEFAULT_PERM[:]
    acl.extend([(Allow, u"%s" % user.login, user_rights)
            for user in self.company.employees])
    return acl


def wrap_db_objects():
    """
        Add acls and names to the db objects used as context
    """
    Company.__acl__ = property(get_company_acl)
    Project.__acl__ = property(get_client_or_project_acls)
    Client.__acl__ = property(get_client_or_project_acls)
    Estimation.__acl__ = property(get_task_acl)
    Invoice.__acl__ = property(get_task_acl)
    CancelInvoice.__acl__ = property(get_task_acl)
    User.__acl__ = property(get_user_acl)
    ExpenseSheet.__acl__ = property(get_expensesheet_acl)
