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
from autonomie.models.competence import (
    CompetenceGrid,
    CompetenceGridItem,
    CompetenceGridSubItem,
)
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
from autonomie.models.expense import (
    ExpenseSheet,
    ExpensePayment,
    ExpenseType,
    ExpenseKmType,
    ExpenseTelType,
)
from autonomie.models.user import (
    User,
    UserDatas,
)
from autonomie_celery.models import (
    Job,
)
from autonomie.models.statistics import (
    StatisticSheet,
    StatisticEntry,
    BaseStatisticCriterion,
)
from autonomie.models.sale_product import (
    SaleProduct,
    SaleProductGroup,
    SaleProductCategory,
)
from autonomie.models.tva import Tva

logger = logging.getLogger(__name__)


DEFAULT_PERM = [
    (Allow, "group:admin", ALL_PERMISSIONS, ),
    (Deny, "group:manager", ('admin',)),
    (Allow, "group:manager", ALL_PERMISSIONS, ),
    (Allow, "group:contractor", ('visit',), ),
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
            ('competences', 'competence', CompetenceGrid, ),
            ('competence_items', 'competence_item', CompetenceGridItem, ),
            ('competence_subitems', 'competence_subitem',
             CompetenceGridSubItem, ),
            ('customers', 'customer', Customer, ),
            ('estimations', 'estimation', Estimation, ),
            ('expenses', 'expense', ExpenseSheet, ),
            (
                'expense_types_expenses',
                'expense_types_expense',
                ExpenseType
            ),
            (
                'expense_types_expensekms',
                'expense_types_expensekm',
                ExpenseKmType
            ),
            (
                'expense_types_expensetels',
                'expense_types_expensetel',
                ExpenseTelType
            ),
            ('expense_payments', 'expense_payment', ExpensePayment, ),
            ('files', 'file', File, ),
            ('invoices', 'invoice', Invoice, ),
            ('jobs', 'job', Job, ),
            ('payments', 'payment', Payment, ),
            ('phases', 'phase', Phase, ),
            ('projects', 'project', Project, ),
            ('sale_categories', 'sale_category', SaleProductCategory, ),
            ('sale_products', 'sale_product', SaleProduct, ),
            ('sale_product_groups', 'sale_product_group', SaleProductGroup, ),
            ('statistics', 'statistic', StatisticSheet,),
            ('statistic_entries', 'statistic_entry', StatisticEntry,),
            ('statistic_criteria', 'statistic_criterion',
             BaseStatisticCriterion,),
            ('templates', 'template', Template, ),
            ('templatinghistory', 'templatinghistory', TemplatingHistory, ),
            ('timeslots', 'timeslot', Timeslot, ),
            ('tvas', 'tva', Tva,),
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
    acl.append(
        (
            Allow,
            Authenticated,
            'view',
        )
    )
    return acl


def get_userdatas_acl(self):
    """
    Return the acls for userdatas
    only the related account has view rights
    """
    acl = DEFAULT_PERM[:]
    if self.user is not None:
        acl.append(
            (
                Allow,
                self.user.login,
                (
                    'view',
                    'view_file',
                )
            ),
        )
    return acl


def get_event_acl(self):
    """
    Return acls fr events participants can view
    """
    acl = DEFAULT_PERM[:]
    for user in self.participants:
        acl.append(
            (
                Allow,
                user.login,
                ("view_activity", "view_workshop", "view_file")
            )
        )
    return acl


def get_activity_acl(self):
    """
    Return acls for activities : companies can also view
    """
    acl = get_event_acl(self)
    for companies in self.companies:
        for user in companies.employees:
            acl.append(
                (
                    Allow,
                    user.login,
                    ("view_activity", "view_file")
                )
            )
    return acl


def get_company_acl(self):
    """
        Compute the company's acls
    """
    acl = DEFAULT_PERM[:]
    acl.extend(
        [(
            Allow,
            user.login,
            (
                "view_company",
                "edit_company",
                # for logo and header
                "view_file",
                "list_customers",
                "add_customer",
                "list_projects",
                "add_project",
                'list_estimations',
                "list_invoices",
                "edit_commercial_handling",
                "list_expenses",
                "add_expense",
                "list_sale_products",
                "add_sale_product",
                "list_treasury_files",
                # Accompagnement
                "list_activities",
                "list_workshops",
            )
        )for user in self.employees]
    )
    return acl


def get_user_acl(self):
    """
        Get acls for user account edition
    """
    acl = DEFAULT_PERM[:]
    if self.enabled():
        acl.append(
            (
                Allow,
                self.login,
                (
                    "view_user",
                    "edit_user",
                    'list_holidays',
                    'add_holiday',
                    'edit_holiday',
                    'list_competences',
                )
            )
        )
        acl.append((Allow, Authenticated, ('visit')))
    return acl


def get_estimation_acl(self):
    """
    Return the acls for estimations
    """
    acls = DEFAULT_PERM[:]
    for user in self.project.company.employees:
        acls.append((
            Allow,
            user.login,
            (
                'view_estimation',
                'edit_estimation',
                'delete_estimation',
                'view_file',
                'add_file',
                'edit_file',
            )
        ))
        if "estimation_validation" in user.groups:
            acls.append((Allow, user.login, ("valid.estimation")))
        else:
            acls.append((Allow, user.login, ("wait.estimation")))

    return acls


def get_invoice_acl(self):
    """
    Return the acls for invoices
    """
    acls = DEFAULT_PERM[:]
    for user in self.project.company.employees:
        acls.append((
            Allow,
            user.login,
            (
                'view_invoice',
                'edit_invoice',
                'delete_invoice',
                'view_file',
                'add_file',
                'edit_file',
                'view_payment',
            )
        ))
        if "invoice_validation" in user.groups:
            acls.append((Allow, user.login, ("valid.invoice",)))
        else:
            acls.append((Allow, user.login, ("wait.invoice",)))

        if "payment_admin" in user.groups:
            acls.append((Allow, user.login, ("add_payment",)))

    return acls


def get_cancelinvoice_acl(self):
    """
    Return the acls for cancelinvoices
    """
    acls = DEFAULT_PERM[:]
    for user in self.project.company.employees:
        rights = (
            'view_cancelinvoice',
            'edit_cancelinvoice',
            'delete_cancelinvoice',
            'view_file',
            'add_file',
            'edit_file',
        )
        if "invoice_validation" in user.groups:
            rights += ("valid.cancelinvoice",)
        else:
            rights += ("wait.cancelinvoice",)
        acls.append((Allow, user.login, rights))
    return acls


def get_payment_acl(self):
    """
    Compute the acls for a Payment object
    """
    acl = DEFAULT_PERM[:]
    for user in self.task.company.employees:
        rights = ('view_payment',)
        if "payment_admin" in user.groups:
            rights += ('edit_payment',)
        acl.append((Allow, user.login, rights,))

    return acl


def get_customer_acls(self):
    """
    Compute the customer's acls
    """
    acl = DEFAULT_PERM[:]
    for user in self.company.employees:
        acl.append(
            (Allow, user.login, ('view_customer', 'edit_customer',))
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
            (
                Allow,
                user.login,
                (
                    'view_project',
                    'edit_project',
                    'add_project',
                    'edit_phase',
                    'add_phase',
                    'add_estimation',
                    'add_invoice',
                    'list_estimations',
                    'list_invoices',
                    'view_file',
                    'add_file',
                    'edit_file',
                )
            )
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


def get_expensesheet_default_acls(self):
    """
    Compute the expense Sheet acl

    :returns: Pyramid acls
    :rtype: list
    """
    acls = DEFAULT_PERM[:]

    if self.status == 'valid':
        acls.insert(
            0,
            (Deny, Everyone, 'edit_expense'),
        )
    for user in self.company.employees:
        perms = (
            'view_expense',
            'view_file',
            'add_file',
            'edit_file',
        )

        if self.is_draft():
            perms += ("edit_expense",)
        acls.append((Allow, user.login, perms,))
    return acls


def get_expense_payment_acl(self):
    """
    Compute the ExpensePayment acls
    """
    acl = DEFAULT_PERM[:]
    user_rights = ('view_expense_payment',)
    acl.extend(
        [
            (Allow, u"%s" % user.login, user_rights)
            for user in self.parent.company.employees
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
    # Exceptions: headers and logos are not attached throught the Node's parent
    # rel
    elif self.company_header_backref is not None:
        return self.company_header_backref.__acl__
    elif self.company_logo_backref is not None:
        return self.company_logo_backref.__acl__
    else:
        return []


def get_product_acls(self):
    """
    Return the acls for a product : A product's acls is given by its category
    """
    acl = DEFAULT_PERM[:]
    for user in self.company.employees:
        acl.append(
            (
                Allow,
                user.login,
                (
                    'list_sale_products',
                    'view_sale_product',
                    'edit_sale_product',
                )
            )
        )
    return acl


def get_competence_acl(self):
    """
    Return acls for the Competence Grids objects
    """
    acls = DEFAULT_PERM[:]
    login = self.contractor.login
    acls.append(
        (
            Allow,
            u'%s' % login,
            (
                "view_competence",
                "edit_competence"
            )
        )
    )
    return acls


def set_models_acls():
    """
    Add acls to the db objects used as context

    Here acls are set globally, but we'd like to set things more dynamically
    when different roles will be implemented
    """
    Activity.__default_acl__ = property(get_activity_acl)
    CancelInvoice.__default_acl__ = property(get_cancelinvoice_default_acls)
    Company.__default_acl__ = property(get_company_acl)
    CompetenceGrid.__acl__ = property(get_competence_acl)
    CompetenceGridItem.__acl__ = property(get_competence_acl)
    CompetenceGridSubItem.__acl__ = property(get_competence_acl)
    ConfigFiles.__default_acl__ = [(Allow, Everyone, 'view'), ]
    Customer.__default_acl__ = property(get_customer_acls)
    Estimation.__default_acl__ = property(get_estimation_default_acls)
    ExpenseSheet.__default_acl__ = property(get_expensesheet_default_acls)
    ExpensePayment.__default_acl__ = property(get_expense_payment_acl)
    File.__default_acl__ = property(get_file_acl)
    Invoice.__default_acl__ = property(get_invoice_default_acls)
    Job.__default_acl__ = DEFAULT_PERM[:]
    Payment.__default_acl__ = property(get_payment_acl)
    Phase.__acl__ = property(get_phase_acls)
    Project.__default_acl__ = property(get_project_acls)
    SaleProductCategory.__acl__ = property(get_product_acls)
    SaleProduct.__acl__ = property(get_product_acls)
    SaleProductGroup.__acl__ = property(get_product_acls)
    StatisticSheet.__acl__ = property(get_base_acl)
    StatisticEntry.__acl__ = property(get_base_acl)
    BaseStatisticCriterion.__acl__ = property(get_base_acl)
    Template.__default_acl__ = property(get_base_acl)
    TemplatingHistory.__default_acl__ = property(get_base_acl)
    Timeslot.__default_acl__ = property(get_base_acl)
    User.__default_acl__ = property(get_user_acl)
    UserDatas.__default_acl__ = property(get_userdatas_acl)
    Workshop.__default_acl__ = property(get_event_acl)

    Tva.__acl__ = property(get_base_acl)
    ExpenseType.__acl__ = property(get_base_acl)
    ExpenseKmType.__acl__ = property(get_base_acl)
    ExpenseTelType.__acl__ = property(get_base_acl)
