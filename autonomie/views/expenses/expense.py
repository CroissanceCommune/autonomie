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
    Expense handling view
"""
import logging
from pyramid.httpexceptions import (
    HTTPFound,
)

from autonomie.forms.expense import (
    ExpensePaymentSchema,
    get_add_edit_sheet_schema,
)
from autonomie.utils import strings
from autonomie.models.company import Company
from autonomie.models.expense.sheet import (
    ExpenseLine,
    ExpenseSheet,
    get_expense_sheet_name,
)
from autonomie.models.expense.types import (
    ExpenseTelType,
)
from autonomie.events.expense import StatusChanged as ExpenseStatusChanged
from autonomie.utils.widgets import (
    ViewLink,
)
from autonomie.export.excel import (
    make_excel_view,
    XlsExpense,
)
from autonomie.resources import (
    expense_resources,
)
from autonomie.views import (
    BaseFormView,
    BaseView,
)
from autonomie.views.render_api import (
    month_name,
    format_account,
)
from autonomie.views.files import (
    FileUploadView,
)


logger = logging.getLogger(__name__)


def get_expense_sheet(year, month, cid, uid):
    """
        Return the expense sheet for the given 4-uple
    """
    return ExpenseSheet.query()\
        .filter(ExpenseSheet.year == year)\
        .filter(ExpenseSheet.month == month)\
        .filter(ExpenseSheet.company_id == cid)\
        .filter(ExpenseSheet.user_id == uid).first()


def get_new_expense_sheet(year, month, cid, uid):
    """
        Return a new expense sheet for the given 4-uple
    """
    expense = ExpenseSheet()
    expense.name = get_expense_sheet_name(month, year)
    expense.year = year
    expense.month = month
    expense.company_id = cid
    expense.user_id = uid
    query = ExpenseTelType.query()
    query = query.filter(ExpenseTelType.active == True)
    teltypes = query.filter(ExpenseTelType.initialize == True)
    for type_ in teltypes:
        line = ExpenseLine(
            type_id=type_.id,
            ht=0,
            tva=0,
            description=type_.label
        )
        expense.lines.append(line)
    return expense


def notify_status_changed(request, status):
    """
    Fire An ExpenseStatusChanged event

    :param obj request: The Pyramid request object
    :param str status: The new status
    """
    request.registry.notify(
        ExpenseStatusChanged(request, request.context, status)
    )


def get_redirect_btn(request, id_):
    """
        Button for "go back to project" link
    """


def populate_actionmenu(request, tolist=False):
    """
        Add buttons in the request actionmenu attribute
    """
    link = None
    if isinstance(request.context, Company):
        link = ViewLink(
            u"Revenir à la liste des dépenses",
            path="company_expenses",
            id=request.context.id
        )
    elif isinstance(request.context, ExpenseSheet):
        if tolist:
            link = ViewLink(
                u"Revenir à la liste des dépenses",
                path="company_expenses",
                id=request.context.company_id
            )
        else:
            link = ViewLink(
                u"Revenir à la note de dépenses",
                path="/expenses/{id}",
                id=request.context.id
            )
    if link is not None:
        request.actionmenu.add(link)


class ExpenseSheetAddView(BaseFormView):
    """
    A simple expense sheet add view
    """
    schema = get_add_edit_sheet_schema()

    def before(self, form):
        populate_actionmenu(self.request)

    def redirect(self, sheet):
        return HTTPFound(
            self.request.route_path('/expenses/{id}', id=sheet.id)
        )

    def _find_existing(self, appstruct):
        """
        Find an existing expense sheet
        """
        return get_expense_sheet(
            appstruct['year'],
            appstruct['month'],
            self.context.id,
            self.request.matchdict['uid']
        )

    def create_instance(self, appstruct):
        """
        Create a new expense sheet instance
        """
        result = get_new_expense_sheet(
            appstruct['year'],
            appstruct['month'],
            self.context.id,
            self.request.matchdict['uid']
        )
        return result

    def submit_success(self, appstruct):
        sheet = self.create_instance(appstruct)
        self.dbsession.add(sheet)
        self.dbsession.flush()
        return self.redirect(sheet)

    def submit_failure(self, e):
        errors = e.error.asdict()
        if 'month' in errors and 'year' in errors:
            appstruct = self.request.POST
            sheet = self._find_existing(appstruct)
            if sheet is not None:
                return self.redirect(sheet)

        BaseFormView.submit_failure(self, e)


class ExpenseSheetEditView(BaseView):
    def title(self):
        return u"Notes de dépense de {0} pour la période de {1} {2}"\
            .format(
                format_account(self.request.context.user),
                month_name(self.context.month),
                self.context.year,
            )

    def context_url(self):
        return self.request.route_path(
            '/api/v1/expenses/{id}',
            id=self.request.context.id
        )

    def form_config_url(self):
        return self.request.route_path(
            '/api/v1/expenses/{id}',
            id=self.request.context.id,
            _query={'form_config': '1'}
        )

    def __call__(self):
        # if not self.request.has_permission('edit.expense'):
        #    return HTTPFound(self.request.current_route_path() + '.html')
        populate_actionmenu(self.request, tolist=True)
        expense_resources.need()
        return dict(
            context=self.context,
            title=self.title(),
            context_url=self.context_url(),
            form_config_url=self.form_config_url(),
            communication_history=self.context.communications,
        )


class ExpenseSheetDeleteView(BaseView):
    """
    Expense deletion view

    Current context is an expensesheet
    """
    msg = u"La note de frais a bien été supprimée"

    def __call__(self):
        logger.info(
            u"# {user.login} deletes expensesheet {expense.id}".format(
                user=self.request.user,
                expense=self.context,
            )
        )
        company = self.context.company

        try:
            self.request.dbsession.delete(self.context)
        except:
            logger.exception(u"Unknown error")
            self.request.session.flash(
                u"Une erreur inconnue s'est produite",
                queue="error",
            )
        else:
            message = self.msg.format(context=self.context)
            self.request.session.flash(message)

        return HTTPFound(
            self.request.route_path(
                'company_expenses',
                id=company.id
            )
        )


class ExpenseSheetDuplicateView(BaseFormView):
    form_options = (('formid', 'duplicate_form'),)
    schema = get_add_edit_sheet_schema()

    @property
    def title(self):
        return u"Dupliquer la note de dépenses de {0} {1}".format(
            strings.month_name(self.context.month),
            self.context.year,
        )

    def before(self, form):
        populate_actionmenu(self.request)

    def redirect(self, sheet):
        return HTTPFound(
            self.request.route_path('/expenses/{id}', id=sheet.id)
        )

    def _find_existing(self, appstruct):
        """
        Find an existing expense sheet
        """
        return get_expense_sheet(
            appstruct['year'],
            appstruct['month'],
            self.context.company_id,
            self.context.user_id,
        )

    def submit_success(self, appstruct):
        logger.debug("# Duplicating an expensesheet #")
        sheet = self.context.duplicate(appstruct['year'], appstruct['month'])
        self.dbsession.add(sheet)
        self.dbsession.flush()
        logger.debug(
            u"ExpenseSheet {0} was duplicated to {1}".format(
                self.context.id, sheet.id
            )
        )
        return self.redirect(sheet)

    def submit_failure(self, e):
        errors = e.error.asdict()
        if 'month' in errors and 'year' in errors:
            appstruct = self.request.POST
            sheet = self._find_existing(appstruct)
            if sheet is not None:
                sheet = self.context
                self.request.session.flash(
                    u"Impossible de dupliquer cette note de dépenses."
                    u"Une note de dépense existe déjà pour la période "
                    u"de {0} {1}.".format(
                        strings.month_name(appstruct['month']),
                        appstruct['year'],
                    ),
                    'error'
                )
                return self.redirect(self.context)

        BaseFormView.submit_failure(self, e)


class ExpenseSheetPaymentView(BaseFormView):
    """
    Called for setting a payment on an expensesheet
    """
    schema = ExpensePaymentSchema()
    title = u"Saisie d'un paiement"

    def before(self, form):
        populate_actionmenu(self.request)

    def redirect(self, come_from):
        if come_from:
            return HTTPFound(come_from)
        else:
            return HTTPFound(
                self.request.route_path(
                    "/expenses/{id}", id=self.request.context.id
                )
            )

    def submit_success(self, appstruct):
        """
        Create the payment
        """
        logger.debug("+ Submitting an expense payment")
        logger.debug(appstruct)
        come_from = appstruct.pop('come_from', None)
        self.context.record_payment(user_id=self.request.user.id, **appstruct)
        self.dbsession.merge(self.context)
        self.request.session.flash(u"Le paiement a bien été enregistré")
        notify_status_changed(self.request, self.context.paid_status)
        return self.redirect(come_from)


def excel_filename(request):
    """
        return an excel filename based on the request context
    """
    exp = request.context
    return u"ndf_{0}_{1}_{2}_{3}.xlsx".format(
        exp.year,
        exp.month,
        exp.user.lastname,
        exp.user.firstname,
    )


def add_routes(config):
    """
    Add module's related routes
    """
    config.add_route("expenses", "/expenses")

    config.add_route(
        "user_expenses",
        "/company/{id}/{uid}/expenses",
        traverse='/companies/{id}'
    )

    config.add_route(
        "/expenses/{id}",
        "/expenses/{id:\d+}",
        traverse="/expenses/{id}",
    )

    for extension in ('xls',):
        config.add_route(
            "/expenses/{id}.xlsx",
            "/expenses/{id:\d+}.xlsx",
            traverse="/expenses/{id}",
        )

    for action in (
        'delete',
        'duplicate',
        'addpayment',
        'addfile',
    ):
        config.add_route(
            "/expenses/{id}/%s" % action,
            "/expenses/{id:\d+}/%s" % action,
            traverse="/expenses/{id}",
        )


def includeme(config):
    """
        Declare all the routes and views related to this module
    """
    add_routes(config)

    config.add_view(
        ExpenseSheetAddView,
        route_name="user_expenses",
        permission="add.expense",
        renderer="base/formpage.mako",
    )

    config.add_view(
        ExpenseSheetEditView,
        route_name="/expenses/{id}",
        renderer="expenses/expense.mako",
        permission="view.expensesheet",
        layout="opa",
    )

    config.add_view(
        ExpenseSheetDeleteView,
        route_name="/expenses/{id}/delete",
        permission="delete.expensesheet",
    )

    config.add_view(
        ExpenseSheetDuplicateView,
        route_name="/expenses/{id}/duplicate",
        renderer="base/formpage.mako",
        permission="view.expensesheet",
    )

    config.add_view(
        ExpenseSheetPaymentView,
        route_name="/expenses/{id}/addpayment",
        permission="add_payment.expensesheet",
        renderer="base/formpage.mako",
    )

    # Xls export
    config.add_view(
        make_excel_view(excel_filename, XlsExpense),
        route_name="/expenses/{id}.xlsx",
        permission="view.expensesheet",
    )
    # File attachment
    config.add_view(
        FileUploadView,
        route_name="/expenses/{id}/addfile",
        renderer='base/formpage.mako',
        permission='add.file',
    )
