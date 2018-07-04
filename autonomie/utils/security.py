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
from sqlalchemy.orm import (
    undefer_group,
    load_only,
)

from autonomie_base.models.base import DBSESSION
from autonomie_celery.models import (
    Job,
)
from autonomie.models.services.find_company import FindCompanyService
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
    FileType,
    Template,
    TemplatingHistory,
)
from autonomie.models.user.group import Group
from autonomie.models.project import (
    Project,
    Phase,
)
from autonomie.models.project.types import (
    ProjectType,
    BusinessType,
)
from autonomie.models.project.business import Business
from autonomie.models.task.task import (
    TaskLine,
    TaskLineGroup,
    DiscountLine,
    Task,
)
from autonomie.models.task.estimation import (
    PaymentLine,
)
from autonomie.models.task.estimation import Estimation
from autonomie.models.task.invoice import (
    Invoice,
    CancelInvoice,
    Payment,
)
from autonomie.models.task.mentions import TaskMention
from autonomie.models.workshop import (
    Workshop,
    Timeslot,
)
from autonomie.models.expense.sheet import (
    ExpenseSheet,
    BaseExpenseLine,
)
from autonomie.models.expense.payment import ExpensePayment
from autonomie.models.expense.types import ExpenseType
from autonomie.models.indicators import SaleFileRequirement

from autonomie.models.user.login import Login
from autonomie.models.user.user import User
from autonomie.models.user.userdatas import UserDatas
from autonomie.models.training.trainer import TrainerDatas
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
from autonomie.models.career_stage import CareerStage
from autonomie.models.career_path import CareerPath
from autonomie.models.accounting.operations import (
    AccountingOperationUpload,
)
from autonomie.models.accounting.treasury_measures import (
    TreasuryMeasureGrid,
    TreasuryMeasureType,
)
from autonomie.models.accounting.income_statement_measures import (
    IncomeStatementMeasureType,
    IncomeStatementMeasureTypeCategory,
    IncomeStatementMeasureGrid,
)

logger = logging.getLogger(__name__)

DEFAULT_PERM = [
    (Allow, "group:admin", ALL_PERMISSIONS, ),
    (Deny, "group:manager", ('admin',)),
    (Allow, "group:manager", ALL_PERMISSIONS, ),
    (Allow, "group:contractor", ('visit',), ),
    (Allow, "group:trainer", ("add.training",)),
    (Allow, "group:constructor", ("add.construction",)),
]
DEFAULT_PERM_NEW = [
    (Allow, "group:admin", ('admin', 'manage', 'admin_treasury')),
    (Allow, "group:manager", ('manage', 'admin_treasury')),
    (Allow, "group:trainer", ("add.training",)),
    (Allow, "group:constructor", ("add.construction",)),
]


class RootFactory(dict):
    """
       Ressource factory, returns the appropriate resource regarding
       the request object
    """
    __name__ = "root"
    leaves = (
        ("activities", "activity", Activity, ),
        (
            'accounting_operation_uploads',
            'accounting_operation_upload',
            AccountingOperationUpload,
        ),
        ('cancelinvoices', 'cancelinvoice', CancelInvoice, ),
        ('companies', 'company', Company, ),
        ('competences', 'competence', CompetenceGrid, ),
        ('competence_items', 'competence_item', CompetenceGridItem, ),
        ('competence_subitems', 'competence_subitem',
            CompetenceGridSubItem, ),
        ('customers', 'customer', Customer, ),
        ('discount_lines', 'discount_line', DiscountLine,),
        ('estimations', 'estimation', Estimation, ),
        ('expenses', 'expense', ExpenseSheet, ),
        ("expenselines", "expenseline", BaseExpenseLine,),
        ("expense_types", "expense_type", ExpenseType,),
        ('expense_payments', 'expense_payment', ExpensePayment, ),
        ('files', 'file', File, ),
        ('file_types', 'file_type', FileType, ),
        ('invoices', 'invoice', Invoice, ),
        (
            'income_statement_measure_grids',
            'income_statement_measure_grid',
            IncomeStatementMeasureGrid,
        ),
        (
            'income_statement_measure_types',
            'income_statement_measure_type',
            IncomeStatementMeasureType,
        ),
        (
            'income_statement_measure_categories',
            'income_statement_measure_category',
            IncomeStatementMeasureTypeCategory,
        ),
        (
            'sale_file_requirements',
            'sale_file_requirement',
            SaleFileRequirement,
        ),
        ('jobs', 'job', Job, ),
        ('logins', 'login', Login, ),
        ('payments', 'payment', Payment, ),
        ('payment_lines', 'payment_line', PaymentLine,),
        ('phases', 'phase', Phase, ),
        ('projects', 'project', Project, ),
        ('project_types', 'project_type', ProjectType),
        ('sale_categories', 'sale_category', SaleProductCategory, ),
        ('sale_products', 'sale_product', SaleProduct, ),
        ('sale_product_groups', 'sale_product_group', SaleProductGroup, ),
        ('statistics', 'statistic', StatisticSheet,),
        ('statistic_entries', 'statistic_entry', StatisticEntry,),
        ('statistic_criteria', 'statistic_criterion',
            BaseStatisticCriterion,),
        ('businesses', 'business', Business),
        ('business_types', 'business_type', BusinessType),
        ('tasks', 'task', Task),
        ('task_lines', 'task_line', TaskLine),
        ('task_line_groups', 'task_line_group', TaskLineGroup),
        ('task_mentions', 'task_mention', TaskMention),
        ('templates', 'template', Template, ),
        ('templatinghistory', 'templatinghistory', TemplatingHistory, ),
        (
            'treasury_measure_grids',
            'treasury_measure_grid',
            TreasuryMeasureGrid,
        ),
        (
            'treasury_measure_types',
            'treasury_measure_type',
            TreasuryMeasureType,
        ),
        ('timeslots', 'timeslot', Timeslot, ),
        ('trainerdatas', 'trainerdata', TrainerDatas,),
        ('tvas', 'tva', Tva,),
        ('users', 'user', User, ),
        ('userdatas', 'userdatas', UserDatas, ),
        ('workshops', 'workshop', Workshop, ),
        ('career_stages', 'career_stage', CareerStage, ),
        ('career_path', 'career_path', CareerPath, ),
    )
    subtrees = ()

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

        for traversal_name, object_name, factory in self.leaves:
            self[traversal_name] = TraversalDbAccess(
                self,
                traversal_name,
                object_name,
                factory,
            )

        for traversal_name, subtree in self.subtrees:
            self[traversal_name] = subtree

        self['configfiles'] = TraversalDbAccess(
            self, 'configfiles', 'config_file', ConfigFiles, 'key'
        )

    @classmethod
    def register_subtree(cls, traversal_name, subtree):
        cls.subtrees = cls.subtrees + ((traversal_name, subtree),)


class TraversalNode(dict):
    """
    Class representing a simple traversal node
    """
    @property
    def __acl__(self):
        """
            Default permissions
        """
        acl = DEFAULT_PERM[:]
        return acl


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
        return the base acl
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


def get_event_acl(self):
    """
    Return acl fr events participants can view
    """
    acl = DEFAULT_PERM[:]
    for user in self.participants:
        acl.append(
            (
                Allow,
                user.login.login,
                ("view_activity", "view_workshop", "view.file")
            )
        )
    return acl


def get_activity_acl(self):
    """
    Return acl for activities : companies can also view
    """
    acl = get_event_acl(self)
    for companies in self.companies:
        for user in companies.employees:
            acl.append(
                (
                    Allow,
                    user.login.login,
                    ("view_activity", "view.file")
                )
            )
    return acl


def get_company_acl(self):
    """
        Compute the company's acl
    """
    acl = DEFAULT_PERM[:]
    acl.extend(
        [(
            Allow,
            user.login.login,
            (
                "view_company",
                "edit_company",
                # for logo and header
                "view.file",
                "list_customers",
                "add_customer",
                "list_projects",
                "add_project",
                'list_estimations',
                "list_invoices",
                "edit_commercial_handling",
                "list_expenses",
                "add.expense",
                "add.expensesheet",
                "list_sale_products",
                "add_sale_product",
                "list_treasury_files",
                # Accompagnement
                "list_activities",
                "list_workshops",
                # New format
                "view.accounting",
                "list.estimation",
                "list.invoice",
                "list.activity",
                "view.commercial",
                "view.treasury",

            )
        )for user in self.employees]
    )
    return acl


def _get_admin_user_base_acl(self):
    """
    Build acl for user account management for admins

    :returns: A list of user acls
    """
    perms = (
        'view.user',
        'edit.user',
        'admin.user',
        'delete.user',
        'list.holiday',
        'add.holiday',

        "list.company",
        "admin.company",

        "list.activity",

        'add.userdatas',
        "add.login",
        "add.trainerdatas",
    )
    for group in Group.query().options(
        load_only('name')
    ).filter(Group.name != 'admin'):
        perms += (u"addgroup.%s" % group.name,)

    admin_perms = perms + ('addgroup.admin',)

    return [
        (Allow, 'group:admin', admin_perms),
        (Allow, 'group:manager', perms),
    ]


def _get_user_base_acl(self):
    """
    Build acl for user account management for the owner

    :returns: The list of user acls
    """
    result = []
    if self.login and self.login.active:
        perms = (
            'view.user',
            'set_email.user',
            'list.holidays',
            'add.holiday',
            'edit.holiday',
        )
        result = [
            (Allow, self.login.login, perms)
        ]
    return result


def _get_admin_login_base_acl(user):
    """
    Build acl for login management for admins

    :params obj user: A User instance
    :returns: A list of user acls (in the format expected by Pyramid)
    """
    perms = (
        'view.login',
        'edit.login',
        'admin.login',
        "set_password.login",
        'delete.login',
        'disable.login',
    )
    return [
        (Allow, 'group:admin', perms),
        (Allow, 'group:manager', perms),
    ]


def _get_login_base_acl(user):
    """
    Build acl for login management for admins

    :params obj user: A User instance
    :returns: A list of user acls (in the format expected by Pyramid)
    """
    if user.login and user.login.active:
        perms = ('view.login', 'set_password.login')
        return [(Allow, user.login.login, perms)]
    return []


def _get_admin_userdatas_base_acl(self):
    """
    Build acl for userdatas management for admins
    """
    perms = (
        'view.userdatas',
        'edit.userdatas',
        'admin.userdatas',
        'delete.userdatas',
        'addfile.userdatas',
        'filelist.userdatas',
        'py3o.userdatas',
        'history.userdatas',
        'doctypes.userdatas',
        'view.file',
        'edit.file',
        'delete.file',
    )

    return [
        (Allow, 'group:admin', perms),
        (Allow, 'group:manager', perms),
    ]


def _get_userdatas_base_acl(user):
    """
    Build acl for userdatas management for users

    :params obj user: A User instance
    :returns: A list of user acls (in the format expected by Pyramid)
    """
    result = []
    if user.login and user.login.active:
        perms = (
            'filelist.userdatas',
        )

        result = [
            (Allow, user.login.login, perms),
        ]
    return result


def _get_admin_trainerdatas_base_acl(user):
    """
    Collect trainer datas management acl for admins

    :params obj user: A User instance
    :returns: A list of user acls (in the format expected by Pyramid)
    """
    perms = (
        'view.trainerdatas',
        'edit.trainerdatas',
        'delete.trainerdatas',
        'disable.trainerdatas',
        'admin.trainerdatas',
        'addfile.trainerdatas',
        'filelist.trainerdatas',
        'edit.file',
        'delete.file',
    )
    return [
        (Allow, 'group:admin', perms),
        (Allow, 'group:manager', perms),
    ]


def _get_trainerdatas_base_acl(user):
    """
    Collect trainer datas management acl for owner

    :params obj user: A User instance
    :returns: A list of user aces (in the format expected by Pyramid)
    """
    result = []
    if user.login and user.login.active:
        perms = (
            'view.trainerdatas',
            'edit.trainerdatas',
            'view.file',
        )

        result = [
            (Allow, user.login.login, perms),
        ]
    return result


def get_user_acl(self):
    """
    Collect acl for a user context
    :returns: A list of user aces (in the format expected by Pyramid)
    """
    acl = DEFAULT_PERM_NEW[:]

    acl.extend(_get_admin_user_base_acl(self))
    acl.extend(_get_admin_login_base_acl(self))
    acl.extend(_get_admin_userdatas_base_acl(self))
    acl.extend(_get_admin_trainerdatas_base_acl(self))
    acl.extend(_get_user_base_acl(self))
    acl.extend(_get_login_base_acl(self))
    acl.extend(_get_userdatas_base_acl(self))
    acl.extend(_get_trainerdatas_base_acl(self))
    return acl


def get_userdatas_acl(self):
    """
    Collect acl for a UserDatas context
    :returns: A list of user aces (in the format expected by Pyramid)
    """
    acl = DEFAULT_PERM_NEW[:]
    if self.user is not None:
        acl.extend(_get_admin_userdatas_base_acl(self.user))
        acl.extend(_get_userdatas_base_acl(self.user))
    return acl


def get_career_path_acl(self):
    """
    Collect acl for a CareerPath context
    :returns: A list of user aces (in the format expected by Pyramid)
    """
    acl = get_userdatas_acl(self.userdatas)
    if self.userdatas.user is not None:
        acl = get_user_acl(self.userdatas.user)
    return acl


def get_trainerdatas_acl(self):
    """
    Collect acl for TrainerDatas context

    :returns: A list of user aces (in the format expected by Pyramid)
    """
    acl = DEFAULT_PERM_NEW[:]
    if self.user is not None:
        acl.extend(_get_admin_trainerdatas_base_acl(self.user))
        acl.extend(_get_trainerdatas_base_acl(self.user))
    return acl


def get_login_acl(self):
    """
    Compute acl for a login object

    :returns: A list of aces (in the format expected by Pyramid)
    """
    acl = DEFAULT_PERM_NEW[:]
    if self.user is not None:
        acl.extend(_get_admin_login_base_acl(self.user))
        acl.extend(_get_login_base_acl(self.user))
    return acl


# TASKS : invoice/estimation/cancelinvoice
def _get_user_status_acl(self):
    """
    Return the common status related acls
    """
    acl = []

    for user in self.company.employees:
        perms = (
            'view.%s' % self.type_,
            'view.file',
            'add.file',
            'edit.file',
            "delete.file",
        )

        if self.status in ('draft', 'invalid'):
            perms += (
                'edit.%s' % self.type_,
                'wait.%s' % self.type_,
                'delete.%s' % self.type_,
                'draft.%s' % self.type_,
            )
        if self.status in ('wait',):
            perms += ('draft.%s' % self.type_,)

        acl.append((Allow, user.login.login, perms))
    return acl


def _get_admin_status_acl(self):
    """
    Return the common status related acls
    """
    perms = (
        'view.%s' % self.type_,
        'admin.%s' % self.type_,
        'view.file',
        'add.file',
        'edit.file',
        "delete.file",
    )

    if self.status in ('draft', 'wait', 'invalid'):
        perms += (
            'edit.%s' % self.type_,
            'valid.%s' % self.type_,
            'delete.%s' % self.type_,
            'draft.%s' % self.type_,
        )
        if self.status == 'wait':
            perms += ('invalid.%s' % self.type_,)
        else:
            perms += ('wait.%s' % self.type_,)

    return [
        (Allow, 'group:admin', perms),
        (Allow, 'group:manager', perms),
    ]


def get_estimation_default_acl(self):
    """
    Return acl for the estimation handling

    :returns: A pyramid acl list
    :rtype: list
    """
    acl = DEFAULT_PERM_NEW[:]

    acl.extend(_get_admin_status_acl(self))
    admin_perms = ('duplicate.estimation',)

    if self.status == 'valid' and self.signed_status != 'aborted':
        if self.project.project_type.default:
            admin_perms += ('geninv.estimation',)
        else:
            admin_perms += ('genbusiness.estimation',)

    if self.status == 'valid':
        admin_perms += ('set_signed_status.estimation',)

    if self.status == 'valid' and self.signed_status != 'signed' and not \
            self.geninv:
        admin_perms += ('set_date.estimation',)

    if admin_perms:
        acl.append((Allow, "group:admin", admin_perms))
        acl.append((Allow, "group:manager", admin_perms))

    # Common estimation access acl
    if self.status != 'valid':
        acl.append(
            (Allow, "group:estimation_validation", ('valid.estimation',))
        )
        acl.append((Deny, "group:estimation_validation", ('wait.estimation',)))

    acl.extend(_get_user_status_acl(self))

    for user in self.company.employees:
        perms = ('duplicate.estimation', )

        if self.status == 'valid':
            perms += ('set_signed_status.estimation', )
            if not self.signed_status == 'aborted':
                if self.project.project_type.default:
                    perms += ('geninv.estimation',)
                else:
                    perms += ('genbusiness.estimation',)

        if perms:
            acl.append((Allow, user.login.login, perms))
    return acl


def get_invoice_default_acl(self):
    """
    Return the acl for invoices

    :returns: A pyramid acl list
    :rtype: list
    """
    acl = DEFAULT_PERM_NEW[:]
    acl.extend(_get_admin_status_acl(self))

    admin_perms = ('duplicate.invoice',)

    if self.status == 'valid' and self.paid_status != 'resulted':
        admin_perms += ('gencinv.invoice', 'add_payment.invoice',)

    if self.status == 'valid' and self.paid_status == 'waiting':
        admin_perms += ('set_date.invoice',)

    admin_perms += ('set_treasury.invoice',)

    if admin_perms:
        acl.append((Allow, "group:admin", admin_perms))
        acl.append((Allow, "group:manager", admin_perms))

    if self.status != 'valid':
        acl.append((Allow, "group:invoice_validation", ('valid.invoice',)))
        acl.append((Deny, "group:invoice_validation", ('wait.invoice',)))

    if self.status == 'valid' and self.paid_status != 'resulted':
        acl.append((Allow, "group:payment_admin", ('add_payment.invoice',)))

    acl.append((Deny, "group:estimation_only", ("duplicate.invoice",)))
    acl.extend(_get_user_status_acl(self))

    for user in self.company.employees:
        perms = ('duplicate.invoice', )
        if self.status == 'valid' and self.paid_status != 'resulted':
            perms += ('gencinv.invoice',)

        if perms:
            acl.append((Allow, user.login.login, perms))

    return acl


def get_cancelinvoice_default_acl(self):
    """
    Return the acl for cancelinvoices
    """
    acl = DEFAULT_PERM_NEW[:]
    acl.extend(_get_admin_status_acl(self))

    admin_perms = ()
    if self.status == 'valid':
        admin_perms += ('set_treasury.cancelinvoice', 'set_date.cancelinvoice')

    if admin_perms:
        acl.append((Allow, "group:admin", admin_perms))
        acl.append((Allow, "group:manager", admin_perms))

    if self.status != 'valid':
        acl.append(
            (Allow, "group:invoice_validation", ('valid.cancelinvoice',))
        )
        acl.append((Deny, "group:invoice_validation", ('wait.cancelinvoice',)))

    acl.extend(_get_user_status_acl(self))
    return acl


def get_task_line_group_acl(self):
    """
    Return the task line acl
    """
    return self.task.__acl__


def get_task_line_acl(self):
    """
    Return the task line acl
    """
    return self.group.__acl__


def get_discount_line_acl(self):
    """
    Return the acls for accessing the discount line
    """
    return self.task.__acl__


def get_payment_line_acl(self):
    """
    Return the acls for accessing a payment line
    """
    return self.task.__acl__


def get_expense_sheet_default_acl(self):
    """
    Compute the expense Sheet acl

    view
    edit
    add_payment

    wait
    valid
    invalid
    delete

    add.file
    edit.file
    view.file

    :returns: Pyramid acl
    :rtype: list
    """
    acl = DEFAULT_PERM_NEW[:]
    acl.extend(_get_admin_status_acl(self))

    admin_perms = ()
    admin_perms += ('set_treasury.expensesheet',)

    if self.status == 'valid' and self.paid_status != 'resulted':
        admin_perms += ('add_payment.expensesheet',)

    admin_perms += ('set_justified.expensesheet',)

    if admin_perms:
        acl.append((Allow, "group:admin", admin_perms))
        acl.append((Allow, "group:manager", admin_perms))

    acl.extend(_get_user_status_acl(self))

    return acl


def get_expenseline_acl(self):
    """
    Return the default acl for an expenseline
    """
    return get_expense_sheet_default_acl(self.sheet)


def get_payment_default_acl(self):
    """
    Compute the acl for a Payment object

    view
    edit
    """
    acl = DEFAULT_PERM_NEW[:]

    admin_perms = ('view.payment',)
    admin_perms += ('edit.payment', 'delete.payment')

    acl.append((Allow, 'group:admin', admin_perms))
    acl.append((Allow, 'group:manager', admin_perms))
    acl.append((Allow, 'group:payment_admin', admin_perms))

    for user in self.task.company.employees:
        acl.append((Allow, user.login.login, ('view.payment',)))

    return acl


def get_expense_payment_acl(self):
    """
    Compute the acl for an Expense Payment object

    view
    edit
    """
    acl = DEFAULT_PERM_NEW[:]
    admin_perms = ('view.payment',)
    # if not self.exported:
    admin_perms += ('edit.payment', 'delete.payment')

    acl.append((Allow, 'group:admin', admin_perms))
    acl.append((Allow, 'group:manager', admin_perms))

    for user in self.expense.company.employees:
        acl.append((Allow, user.login.login, ('view.payment',)))
    return acl


def get_customer_acl(self):
    """
    Compute the customer's acl
    """
    acl = DEFAULT_PERM[:]
    perms = ('view_customer', 'edit_customer',)

    if not self.has_tasks():
        perms += ('delete_customer',)
    else:
        acl.insert(0, (Deny, Everyone, ('delete_customer',)))

    for user in self.company.employees:
        acl.append((Allow, user.login.login, perms))

    return acl


def get_phase_acl(self):
    """
    Return acl for a phase
    """
    acl = DEFAULT_PERM[:]

    perms = ("edit.phase",)
    if DBSESSION().query(Task.id).filter_by(phase_id=self.id).count() == 0:
        perms += ('delete.phase',)
    else:
        acl.insert(0, (Deny, Everyone, ('delete.phase',)))

    for user in self.project.company.employees:
        acl.append((Allow, user.login.login, perms))

    return acl


def get_project_acl(self):
    """
    Return acl for a project
    """
    acl = DEFAULT_PERM_NEW[:]

    perms = (
        'view_project',
        'view.project',
        'edit_project',
        'edit.project',
        'edit_phase',
        'edit.phase',
        'add_phase',
        'add.phase',
        'add_estimation',
        'add.estimation',
        'add_invoice',
        'add.invoice',
        'list_estimations',
        'list.estimations',
        'list_invoices',
        'list.invoices',
        'view.file',
        'list.files',
        'add.file',
        'edit.file',
        "delete.file",
    )

    if not self.has_tasks():
        perms += ('delete_project', )
    else:
        acl.insert(0, (Deny, Everyone, ('delete_project', )))

    admin_perms = perms[:]
    if not self.project_type.default:
        perms += ('list.businesses', )

    admin_perms += ('list.businesses',)

    acl.append((Allow, "group:admin", admin_perms))
    acl.append((Allow, "group:manager", admin_perms))

    acl.append((Deny, 'group:estimation_only', ('add_invoice', )))

    for user in self.company.employees:
        acl.append((Allow, user.login.login, perms))

    return acl


def get_business_acl(self):
    """
    Compute the acl for the Business object
    """
    acl = get_project_acl(self.project)

    perms = ('view.business', 'add.file',)
    admin_perms = ('view.business',)

    if not self.closed:
        admin_perms += ('edit.business', 'add.invoice', 'close.business',)
        perms += ('edit.business', 'add.invoice',)

        if not self.invoices and not self.cancelinvoices:
            perms += ('delete.business',)
            admin_perms += ('delete.business',)

    acl.append((Allow, 'group:admin', admin_perms))
    acl.append((Allow, 'group:manager', perms))

    for user in self.project.company.employees:
        acl.append((Allow, user.login.login, perms))

    return acl


def get_file_acl(self):
    """
    Compute the acl for a file object
    a file object's acl are simply the parent's
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


def get_product_acl(self):
    """
    Return the acl for a product : A product's acl is given by its category
    """
    acl = DEFAULT_PERM[:]
    for user in self.company.employees:
        acl.append(
            (
                Allow,
                user.login.login,
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
    Return acl for the Competence Grids objects
    """
    acl = DEFAULT_PERM[:]
    login = self.contractor.login
    acl.append(
        (
            Allow,
            u'%s' % login,
            (
                "view_competence",
                "edit_competence"
            )
        )
    )
    return acl


def get_accounting_measure_acl(self):
    """
    Compile the default acl for TreasuryMeasureGrid and
    IncomeStatementMeasureGrid objects
    """
    if self.company is not None:
        return self.company.__acl__
    return []


def get_indicator_acl(self):
    """
    Compile Indicator acl
    """
    acl = DEFAULT_PERM_NEW[:]
    admin_perms = ('view.indicator', 'force.indicator')
    if self.status != 'success':
        admin_perms += ("force.indicator",)

    if self.validation:
        if self.validation_status != 'valid':
            admin_perms += (
                "valid.indicator",
            )
    acl.append((Allow, 'group:admin', admin_perms))
    acl.append((Allow, 'group:manager', admin_perms))
    return acl


def get_sale_file_requirement_acl(self):
    """
    Compile acl for SaleFileRequirement instances
    """
    # Si le parent est validé et l'indicateur est ok, on ne peut plus modifier
    user_perms = ('view.indicator',)
    admin_perms = ()

    locked = False
    if self.status == 'success':
        if hasattr(self.node, 'status') and self.node.status == 'valid':
            locked = True

    if not locked:
        acl = get_indicator_acl(self)
        if self.file_id is None:
            admin_perms += ("add.file",)
            user_perms += ("add.file",)
        else:
            admin_perms += ("edit.file",)
            user_perms += ("edit.file",)

    else:
        acl = DEFAULT_PERM_NEW[:]

    employee_logins = FindCompanyService.find_employees_login_from_node(
        self.node
    )

    for login in employee_logins:
        acl.append((Allow, login, user_perms))

    acl.append((Allow, 'group:admin', admin_perms))
    acl.append((Allow, 'group:manager', admin_perms))
    return acl


def set_models_acl():
    """
    Add acl to the db objects used as context

    Here acl are set globally, but we'd like to set things more dynamically
    when different roles will be implemented
    """
    Activity.__default_acl__ = property(get_activity_acl)
    AccountingOperationUpload.__acl__ = property(get_base_acl)
    Business.__default_acl__ = property(get_business_acl)
    BusinessType.__acl__ = property(get_base_acl)
    CancelInvoice.__default_acl__ = property(get_cancelinvoice_default_acl)
    Company.__default_acl__ = property(get_company_acl)
    CompetenceGrid.__acl__ = property(get_competence_acl)
    CompetenceGridItem.__acl__ = property(get_competence_acl)
    CompetenceGridSubItem.__acl__ = property(get_competence_acl)
    ConfigFiles.__default_acl__ = [(Allow, Everyone, 'view'), ]
    Customer.__default_acl__ = property(get_customer_acl)
    DiscountLine.__acl__ = property(get_discount_line_acl)
    Estimation.__default_acl__ = property(get_estimation_default_acl)
    ExpenseSheet.__default_acl__ = property(get_expense_sheet_default_acl)
    ExpensePayment.__acl__ = property(get_expense_payment_acl)
    File.__default_acl__ = property(get_file_acl)
    FileType.__acl__ = property(get_base_acl)
    Invoice.__default_acl__ = property(get_invoice_default_acl)
    SaleFileRequirement.__acl__ = property(get_sale_file_requirement_acl)
    Job.__default_acl__ = DEFAULT_PERM[:]
    Login.__acl__ = property(get_login_acl)
    Payment.__default_acl__ = property(get_payment_default_acl)
    PaymentLine.__acl__ = property(get_payment_line_acl)
    Phase.__acl__ = property(get_phase_acl)
    Project.__default_acl__ = property(get_project_acl)
    ProjectType.__acl__ = property(get_base_acl)
    SaleProductCategory.__acl__ = property(get_product_acl)
    SaleProduct.__acl__ = property(get_product_acl)
    SaleProductGroup.__acl__ = property(get_product_acl)
    StatisticSheet.__acl__ = property(get_base_acl)
    StatisticEntry.__acl__ = property(get_base_acl)
    BaseStatisticCriterion.__acl__ = property(get_base_acl)
    TaskLine.__acl__ = property(get_task_line_acl)
    TaskLineGroup.__acl__ = property(get_task_line_group_acl)
    TaskMention.__acl__ = property(get_base_acl)
    Template.__default_acl__ = property(get_base_acl)
    TemplatingHistory.__default_acl__ = property(get_base_acl)
    Timeslot.__default_acl__ = property(get_base_acl)
    TrainerDatas.__default_acl__ = property(get_trainerdatas_acl)
    TreasuryMeasureGrid.__acl__ = property(get_accounting_measure_acl)
    TreasuryMeasureType.__acl__ = property(get_base_acl)
    IncomeStatementMeasureGrid.__acl__ = property(get_accounting_measure_acl)
    IncomeStatementMeasureType.__acl__ = property(get_base_acl)
    IncomeStatementMeasureTypeCategory.__acl__ = property(get_base_acl)
    User.__default_acl__ = property(get_user_acl)
    UserDatas.__default_acl__ = property(get_userdatas_acl)
    Workshop.__default_acl__ = property(get_event_acl)

    Tva.__acl__ = property(get_base_acl)
    BaseExpenseLine.__acl__ = property(get_expenseline_acl)
    ExpenseType.__acl__ = property(get_base_acl)
    CareerStage.__acl__ = property(get_base_acl)
    CareerPath.__acl__ = property(get_career_path_acl)
