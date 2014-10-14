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

from autonomie.models.activity import Activity
from autonomie.models.company import Company
from autonomie.models.customer import Customer
from autonomie.models.files import File
from autonomie.models.project import Project
from autonomie.models.task.estimation import Estimation
from autonomie.models.task.invoice import (
    Invoice,
    CancelInvoice,
    Payment,
)
from autonomie.models.workshop import (
    Workshop,
    Timeslot,
)
from autonomie.models.treasury import (
    ExpenseSheet,
    BaseExpenseLine,
)
from autonomie.models.user import (
    User,
    UserDatas,
)

log = logging.getLogger(__name__)

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

        for traversal_name, object_name, factory in (
            ("activities", "activity", Activity, ),
            ('cancelinvoices', 'cancelinvoice', CancelInvoice, ),
            ('companies', 'company', Company, ),
            ('customers', 'customer', Customer, ),
            ('estimations', 'estimation', Estimation, ),
            ('expenses', 'expense', ExpenseSheet, ),
            ('expenselines', 'expenseline', BaseExpenseLine, ),
            ('files', 'file', File, ),
            ('invoices', 'invoice', Invoice, ),
            ('projects', 'project', Project, ),
            ('users', 'user', User, ),
            ('userdatas', 'userdatas', UserDatas, ),
            ('payments', 'payment', Payment, ),
            ('workshops', 'workshop', Workshop, ),
            ('timeslots', 'timeslot', Timeslot, ),
            ):

            self[traversal_name] = TraversalDbAccess(
                self,
                traversal_name,
                object_name,
                factory)


class TraversalDbAccess(object):
    """
        Class handling access to dbrelated objects
    """
    __acl__ = DEFAULT_PERM[:]
    dbsession = None

    def __init__(self, parent, traversal_name, object_name, factory):
        self.__parent__ = parent
        self.factory = factory
        self.object_name = object_name
        self.__name__ = traversal_name

    def __getitem__(self, key):
        return self._get_item(self.factory, key, self.object_name)

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


def get_base_acl(self):
    """
        return the base acls
    """
    acl = DEFAULT_PERM[:]
    acl.append((Allow, Authenticated, 'view',))
    return acl


def get_activity_acl(self):
    """
    Return acls for activities
    """
    acl = DEFAULT_PERM[:]
    acl.extend(
        [(Allow, u"%s" % user.login, "view") for user in self.participants]
            )
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


def get_customer_or_project_acls(self):
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


def get_expense_acl(self):
    """
        Compute the acls for an expenseline
    """
    if self.sheet.status in ('draft', 'invalid'):
        user_rights = ("view", "edit", "add")
    else:
        user_rights = ("view",)
    acl = DEFAULT_PERM[:]
    acl.extend([(Allow, u"%s" % user.login, user_rights)
        for user in self.sheet.company.employees])
    return acl


def get_file_acl(self):
    """
    Compute the acls for a file object
    a file object's acls are simply the parent's
    """
    if self.parent is not None:
        return self.parent.__acl__
    elif self.company_header_backref is not None:
        return self.company_header_backref.__acl__
    elif self.company_logo_backref is not None:
        return self.company_logo_backref.__acl__
    else:
        return []


def set_models_acls():
    """
    Add acls to the db objects used as context

    Here acls are set globally, but we'd like to set things more dynamically
    when different roles will be implemented
    """
    Company.__acl__ = property(get_company_acl)
    Project.__acl__ = property(get_customer_or_project_acls)
    Customer.__acl__ = property(get_customer_or_project_acls)
    Estimation.__acl__ = property(get_task_acl)
    Invoice.__acl__ = property(get_task_acl)
    CancelInvoice.__acl__ = property(get_task_acl)
    User.__acl__ = property(get_user_acl)
    UserDatas.__acl__ = property(get_base_acl)
    ExpenseSheet.__acl__ = property(get_expensesheet_acl)
    BaseExpenseLine.__acl__ = property(get_expense_acl)
    Activity.__acl__ = property(get_activity_acl)
    File.__acl__ = property(get_file_acl)
    Payment.__acl__ = property(get_base_acl)
    Workshop.__acl__ = property(get_activity_acl)
    Timeslot.__acl__ = property(get_base_acl)
