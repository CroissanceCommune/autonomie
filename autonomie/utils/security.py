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


DEFAULT_PERM = [
    (Allow, "group:admin", ALL_PERMISSIONS, ),
    (Deny, "group:manager", ('admin',)),
    (Allow, "group:manager", ALL_PERMISSIONS, ),
    (Allow, "group:contractor", ('visit',), ),
]
DEFAULT_PERM_NEW = [
    (Allow, "group:admin", ('admin', 'manage', 'admin_treasury')),
    (Allow, "group:manager", ('manage', 'admin_treasury')),
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


def get_userdatas_acl(self):
    """
    Return the acl for userdatas
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
                    'view.file',
                )
            ),
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
                user.login,
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
                    user.login,
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
            user.login,
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
        Get acl for user account edition
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

        acl.append((Allow, user.login, perms))
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
    admin_perms = ()

    if self.status == 'valid' and self.signed_status != 'aborted':
        admin_perms += ('geninv.estimation',)

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
        acl.append((Allow, "group:estimation_validation", ('valid.estimation',)))
        acl.append((Deny, "group:estimation_validation", ('wait.estimation',)))

    acl.extend(_get_user_status_acl(self))

    for user in self.company.employees:
        perms = ()

        if self.status == 'valid':
            perms += ('set_signed_status.estimation', )
            if not self.signed_status == 'aborted':
                perms += ('geninv.estimation',)

        if perms:
            acl.append((Allow, user.login, perms))
    return acl


def get_invoice_default_acl(self):
    """
    Return the acl for invoices

    :returns: A pyramid acl list
    :rtype: list
    """
    acl = DEFAULT_PERM_NEW[:]
    acl.extend(_get_admin_status_acl(self))

    admin_perms = ()

    if self.status == 'valid' and self.paid_status != 'resulted':
        admin_perms += ('gencinv.invoice', 'add_payment.invoice',)

    if self.status == 'valid' and self.paid_status == 'waiting' and not self.exported:
        admin_perms += ('set_date.invoice',)

    if not self.exported:
        admin_perms += ('set_treasury.invoice',)

    if admin_perms:
        acl.append((Allow, "group:admin", admin_perms))
        acl.append((Allow, "group:manager", admin_perms))

    if self.status != 'valid':
        acl.append((Allow, "group:invoice_validation", ('valid.invoice',)))
        acl.append((Deny, "group:invoice_validation", ('wait.invoice',)))

    if self.status == 'valid' and self.paid_status != 'resulted':
        acl.append((Allow, "group:payment_admin", ('add_payment.invoice',)))

    acl.extend(_get_user_status_acl(self))

    for user in self.company.employees:
        perms = ()
        if self.status == 'valid' and self.paid_status != 'resulted':
            perms += ('gencinv.invoice',)

        if perms:
            acl.append((Allow, user.login, perms))

    return acl


def get_cancelinvoice_default_acl(self):
    """
    Return the acl for cancelinvoices
    """
    acl = DEFAULT_PERM_NEW[:]
    acl.extend(_get_admin_status_acl(self))

    admin_perms = ()
    if not self.exported and self.status == 'valid':
        admin_perms += ('set_treasury.cancelinvoice', 'set_date.cancelinvoice')

    if admin_perms:
        acl.append((Allow, "group:admin", admin_perms))
        acl.append((Allow, "group:manager", admin_perms))

    if self.status != 'valid':
        acl.append((Allow, "group:invoice_validation", ('valid.cancelinvoice',)))
        acl.append((Deny, "group:invoice_validation", ('wait.cancelinvoice',)))

    acl.extend(_get_user_status_acl(self))
    return acl


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
    if not self.exported:
        admin_perms += ('set_treasury.expensesheet',)

    if self.status == 'valid' and self.paid_status != 'resulted':
        admin_perms += ('add_payment.expensesheet',)

    if admin_perms:
        acl.append((Allow, "group:admin", admin_perms))
        acl.append((Allow, "group:manager", admin_perms))

    acl.extend(_get_user_status_acl(self))

    return acl


def get_payment_default_acl(self):
    """
    Compute the acl for a Payment object

    view
    edit
    """
    acl = DEFAULT_PERM_NEW[:]

    admin_perms = ('view.payment',)
    if not self.exported:
        admin_perms += ('edit.payment',)

    acl.append((Allow, 'group:admin', admin_perms))
    acl.append((Allow, 'group:manager', admin_perms))
    acl.append((Allow, 'group:payment_admin', admin_perms))

    for user in self.task.company.employees:
        acl.append((Allow, user.login, ('view.payment',)))

    return acl


def get_expense_payment_acl(self):
    """
    Compute the acl for an Expense Payment object

    view
    edit
    """
    acl = DEFAULT_PERM_NEW[:]
    admin_perms = ('view.expensesheet_payment',)
    if not self.exported:
        admin_perms += ('edit.expensesheet_payment',)

    acl.append((Allow, 'group:admin', admin_perms))
    acl.append((Allow, 'group:manager', admin_perms))

    for user in self.task.company.employees:
        acl.append((Allow, user.login, ('view.expensesheet_payment',)))

    return acl


def get_customer_acl(self):
    """
    Compute the customer's acl
    """
    acl = DEFAULT_PERM[:]
    for user in self.company.employees:
        acl.append(
            (Allow, user.login, ('view_customer', 'edit_customer',))
        )
    return acl


def get_phase_acl(self):
    """
    Return acl for a phase
    """
    return get_project_acl(self.project)


def get_project_acl(self):
    """
    Return acl for a project
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
                    'view.file',
                    'add.file',
                    'edit.file',
                )
            )
        )

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


def set_models_acl():
    """
    Add acl to the db objects used as context

    Here acl are set globally, but we'd like to set things more dynamically
    when different roles will be implemented
    """
    Activity.__default_acl__ = property(get_activity_acl)
    CancelInvoice.__default_acl__ = property(get_cancelinvoice_default_acl)
    Company.__default_acl__ = property(get_company_acl)
    CompetenceGrid.__acl__ = property(get_competence_acl)
    CompetenceGridItem.__acl__ = property(get_competence_acl)
    CompetenceGridSubItem.__acl__ = property(get_competence_acl)
    ConfigFiles.__default_acl__ = [(Allow, Everyone, 'view'), ]
    Customer.__default_acl__ = property(get_customer_acl)
    Estimation.__default_acl__ = property(get_estimation_default_acl)
    ExpenseSheet.__default_acl__ = property(get_expense_sheet_default_acl)
    ExpensePayment.__default_acl__ = property(get_expense_payment_acl)
    File.__default_acl__ = property(get_file_acl)
    Invoice.__default_acl__ = property(get_invoice_default_acl)
    Job.__default_acl__ = DEFAULT_PERM[:]
    Payment.__default_acl__ = property(get_payment_default_acl)
    Phase.__acl__ = property(get_phase_acl)
    Project.__default_acl__ = property(get_project_acl)
    SaleProductCategory.__acl__ = property(get_product_acl)
    SaleProduct.__acl__ = property(get_product_acl)
    SaleProductGroup.__acl__ = property(get_product_acl)
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
