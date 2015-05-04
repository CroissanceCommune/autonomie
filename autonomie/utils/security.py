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
from pyramid.security import (
    Allow,
    Deny,
    Everyone,
    Authenticated,
    ALL_PERMISSIONS,
)
from sqlalchemy.orm import undefer_group

from autonomie.models.config import ConfigFiles
from autonomie.models.activity import Activity
from autonomie.models.company import Company
from autonomie.models.customer import Customer
from autonomie.models.files import (
    File,
    Template,
    TemplatingHistory,
)
from autonomie.models.project import (
    Project,
    Phase,
)
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
from autonomie.models.job import (
    Job,
)
from autonomie.models.statistics import (
    StatisticSheet,
    StatisticEntry,
)

log = logging.getLogger(__name__)


DEFAULT_PERM = [
    (Allow, "group:admin", ALL_PERMISSIONS,),
    (Deny, "group:manager", ('admin', )),
    (Allow, "group:manager", ALL_PERMISSIONS,),
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
            ('jobs', 'job', Job, ),
            ('payments', 'payment', Payment, ),
            ('phases', 'phase', Phase, ),
            ('projects', 'project', Project, ),
            ('statistics', 'statistic', StatisticSheet,),
            ('statistic_entries', 'statistic_entry', StatisticEntry,),
            ('templates', 'template', Template, ),
            ('templatinghistory', 'templatinghistory', TemplatingHistory, ),
            ('timeslots', 'timeslot', Timeslot, ),
            ('users', 'user', User, ),
            ('userdatas', 'userdatas', UserDatas, ),
            ('workshops', 'workshop', Workshop, ),
        ):

            self[traversal_name] = TraversalDbAccess(
                self,
                traversal_name,
                object_name,
                factory,
            )

        self['configfiles'] = TraversalDbAccess(
            self, 'configfiles', 'config_file', ConfigFiles, 'key'
        )


class TraversalDbAccess(object):
    """
        Class handling access to dbrelated objects
    """
    __acl__ = DEFAULT_PERM[:]
    dbsession = None

    def __init__(self, parent, traversal_name, object_name, factory,
                 id_key='id'):
        self.__parent__ = parent
        self.factory = factory
        self.object_name = object_name
        self.__name__ = traversal_name
        self.id_key = id_key

    def __getitem__(self, key):
        return self._get_item(self.factory, key, self.object_name)

    def _get_item(self, klass, key, object_name):
        assert self.dbsession is not None, "Missing dbsession"

        dbsession = self.dbsession()
        obj = dbsession.query(klass)\
                       .options(undefer_group('edit'))\
                       .filter(getattr(klass, self.id_key) == key)\
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


def get_userdatas_acl(self):
    """
    Return the acls for userdatas
    only the related account has view rights
    """
    acl = DEFAULT_PERM[:]
    if self.user is not None:
        acl.append((Allow, self.user.login, 'view'))
    return acl


def get_event_acl(self):
    """
    Return acls fr events participants can view
    """
    acl = DEFAULT_PERM[:]
    acl.extend(
        [(Allow, u"%s" % user.login, "view") for user in self.participants]
    )
    return acl


def get_activity_acl(self):
    """
    Return acls for activities : companies can also view
    """
    acl = get_event_acl(self)
    for companies in self.companies:
        for user in companies.employees:
            acl.append((Allow, u"%s" % user.login, "view",))
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


def get_estimation_acl(self):
    """
    Return the acls for estimations
    """
    acls = get_task_acl(self)
    for user in self.project.company.employees:
        if "estimation_validation" in user.groups:
            acls.append((Allow, user.login, ("valid.estimation")))
        else:
            acls.append((Allow, user.login, ("wait.estimation")))

    return acls


def get_invoice_acl(self):
    """
    Return the acls for invoices
    """
    acls = get_task_acl(self)
    for user in self.project.company.employees:
        if "invoice_validation" in user.groups:
            acls.append((Allow, user.login, ("valid.invoice")))
        else:
            acls.append((Allow, user.login, ("wait.invoice")))
    return acls


def get_customer_acls(self):
    """
    Compute the customer's acls
    """
    acl = DEFAULT_PERM[:]
    for user in self.company.employees:
        acl.append(
            (Allow, user.login, ('view', 'edit', 'add'))
        )
    return acl


def get_phase_acls(self):
    """
    Return acls for a phase
    """
    return get_project_acls(self.project)


def get_project_acls(self):
    """
    Return acls for a project
    """
    acl = DEFAULT_PERM[:]
    for user in self.company.employees:
        acl.append(
            (Allow, user.login, ('view', 'edit', 'add'))
        )
        if "estimation_validation" in user.groups:
            # The user can validate its estimations
            acl.append(
                (Allow, user.login, ('valid.estimation',))
            )
        else:
            # The user need to ask for validation process
            acl.append(
                (Allow, user.login, ('wait.estimation',))
            )
        if "invoice_validation" in user.groups:
            acl.append(
                (Allow, user.login, ('valid.invoice',))
            )
        else:
            # The user need to ask for validation process
            acl.append(
                (Allow, user.login, ('wait.invoice',))
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
    acl.extend(
        [
            (Allow, u"%s" % user.login, user_rights)
            for user in self.company.employees
        ]
    )
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
    acl.extend(
        [
            (Allow, u"%s" % user.login, user_rights)
            for user in self.sheet.company.employees
        ]
    )
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
    Activity.__default_acl__ = property(get_activity_acl)
    BaseExpenseLine.__default_acl__ = property(get_expense_acl)
    CancelInvoice.__default_acl__ = property(get_invoice_acl)
    Company.__default_acl__ = property(get_company_acl)
    ConfigFiles.__default_acl__ = [(Allow, Everyone, 'view'), ]
    Customer.__default_acl__ = property(get_customer_acls)
    Estimation.__default_acl__ = property(get_estimation_acl)
    ExpenseSheet.__default_acl__ = property(get_expensesheet_acl)
    File.__default_acl__ = property(get_file_acl)
    Invoice.__default_acl__ = property(get_invoice_acl)
    Job.__default_acl__ = DEFAULT_PERM[:]
    Payment.__default_acl__ = property(get_base_acl)
    Phase.__acl__ = property(get_phase_acls)
    Project.__default_acl__ = property(get_project_acls)
    StatisticSheet.__default_acl__ = property(get_base_acl)
    StatisticEntry.__default_acl__ = property(get_base_acl)
    Template.__default_acl__ = property(get_base_acl)
    TemplatingHistory.__default_acl__ = property(get_base_acl)
    Timeslot.__default_acl__ = property(get_base_acl)
    User.__default_acl__ = property(get_user_acl)
    UserDatas.__default_acl__ = property(get_userdatas_acl)
    Workshop.__default_acl__ = property(get_event_acl)
