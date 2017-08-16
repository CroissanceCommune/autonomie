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
import colander

from pyramid.httpexceptions import (
    HTTPFound,
)

from autonomie.forms.expense import (
    PeriodSelectSchema,
    ExpensePaymentSchema,
    get_new_expense_schema,
)
from autonomie.utils import strings
from autonomie.models.company import Company
from autonomie.models.expense import (
    ExpenseTelType,
    ExpenseLine,
    ExpenseSheet,
    get_expense_sheet_name,
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
from autonomie.views.status import StatusView
from autonomie.views.render_api import (
    month_name,
    format_account,
)
from autonomie.views.files import (
    FileUploadView,
)


logger = logging.getLogger(__name__)


def get_period(request):
    """
        Return the period configured in the current request
    """
    schema = PeriodSelectSchema().bind(request=request)
    try:
        appstruct = schema.deserialize(request.GET)
    except colander.Invalid:
        appstruct = schema.deserialize({})
    year = appstruct['year']
    month = appstruct['month']
    return year, month


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


def populate_actionmenu(request):
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
    schema = get_new_expense_schema()

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
        sheet = self._find_existing(appstruct)
        if sheet is None:
            sheet = self.create_instance(appstruct)
            self.dbsession.add(sheet)
            self.dbsession.flush()
        return self.redirect(sheet)


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

        expense_resources.need()
        populate_actionmenu(self.request)
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
    schema = get_new_expense_schema()

    @property
    def title(self):
        return u"Dupliquer la note de dépenses de {0} {1}".format(
            self.context.month_label, self.context.year,
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

        sheet = self._find_existing(appstruct)
        if sheet is None:
            sheet = self.context.duplicate(appstruct['year'], appstruct['month'])
            self.dbsession.add(sheet)
            self.dbsession.flush()
            logger.debug(
                u"ExpenseSheet {0} was duplicated to {1}".format(
                    self.context.id, sheet.id
                )
            )
        else:
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

        return self.redirect(sheet)



# class ExpenseSheetView(BaseFormView):
#     """
#         ExpenseSheet view
#     """
#     add_template_vars = (
#         'title',
#         'loadurl',
#         "edit",
#         "communication_history",
#     )
#
#     def __init__(self, request):
#         super(ExpenseSheetView, self).__init__(request)
#         expense_js.need()
#         self.month = self.request.context.month
#         self.year = self.request.context.year
#         self.formcounter = None
#
#     @property
#     def communication_history(self):
#         """
#             Communication history data, will be carried to the template
#         """
#         return get_expense_history(self.request.context)
#
#     @property
#     def title(self):
#         """
#             Return the title of the page
#         """
#
#     @property
#     def buttons(self):
#         """
#             Return the buttons used for form submission
#         """
#         btns = []
#         logger.debug(u"   + Available actions :")
#         for action in self.request.context.get_next_actions():
#             logger.debug(u"    * {0}".format(action.name))
#             if action.allowed(self.request.context, self.request):
#                 logger.debug(u"     -> is allowed for the current user")
#                 if hasattr(self, "_%s_btn" % action.name):
#                     func = getattr(self, "_%s_btn" % action.name)
#                     btns.append(func())
#
#         if self.request.has_permission('add_payment.expense'):
#             btns.append(self._paid_btn())
#         return btns
#
#     def _reset_btn(self):
#         """
#             Return a reset button
#         """
#         return Submit(
#             u"Réinitialiser",
#             "reset",
#             name="reset",
#             request=self.request,
#             confirm=u"Êtes-vous sûr de vouloir réinitialiser \
# cette feuille de notes de dépense (toutes les modifications apportées seront \
# perdues) ?")
#
#     def _draft_btn(self):
#         """
#         Return a button to set the expense to draft again
#         """
#         msg = u"Annuler la mise en validation et repasser en brouillon"
#         return Submit(
#             msg,
#             "draft",
#             request=self.request,
#         )
#
#     def _wait_btn(self):
#         """
#             Return a button for requesting validation
#         """
#         return Submit(u"Demander la validation", "wait", request=self.request)
#
#     def _valid_btn(self):
#         """
#             Return a validation button
#         """
#         return Submit(u"Valider le document", "valid", request=self.request)
#
#     def _invalid_btn(self):
#         """
#             Return an invalidation button
#         """
#         return Submit(u"Invalider le document", "invalid", request=self.request)
#
#     def _paid_form(self):
#         """
#         Return the form for payment registration
#         """
#         form = get_payment_form(self.request, self.formcounter)
#         appstruct = {
#             'amount': self.context.topay(),
#             'come_from': self.request.current_route_path(),
#         }
#         form.set_appstruct(appstruct)
#         self.formcounter = form.counter
#         return form
#
#     def _paid_btn(self):
#         """
#             Return a button to set a paid btn and a select to choose
#             the payment mode
#         """
#         form = self._paid_form()
#         title = u"Notifier un paiement"
#         popup = PopUp("paidform", title, form.render())
#         self.request.popups[popup.name] = popup
#         return popup.open_btn(css='btn btn-primary')
#
#     @property
#     def edit(self):
#         """
#             return True if the current context is editable by the current user
#         """
#         return self.request.has_permission("edit.expensesheet")
#
#     @property
#     def loadurl(self):
#         """
#             Returns a json representation of the current expense sheet
#         """
#         return self.request.route_path(
#             "expensejson",
#             id=self.request.context.id,
#         )
#
#     def before(self, form):
#         """
#         Prepopulate the form
#         """
#         # Here we override the form counter to avoid field ids conflict
#         form.set_appstruct(self.request.context.appstruct())
#         if self.request.has_permission('admin.expensesheet'):
#             btn = ViewLink(
#                 u"Revenir à la liste",
#                 "admin.expensesheet",
#                 path="expenses",
#             )
#         else:
#             btn = ViewLink(
#                 u"Revenir à la liste",
#                 "view.expensesheet",
#                 path="company_expenses",
#                 id=self.request.context.company.id,
#             )
#         self.request.actionmenu.add(btn)
#         btn = get_add_file_link(
#             self.request,
#             label=u"Déposer des justificatifs",
#             perm="add.file",
#         )
#         self.request.actionmenu.add(btn)
#
#     def submit_success(self, appstruct):
#         """
#             Handle submission of the expense page, only on state change
#             validation
#         """
#         logger.debug("#  Submitting expense sheet status form  #")
#         logger.debug(appstruct)
#
#         # Comment is now stored in a specific table
#         comment = None
#         if "comment" in appstruct:
#             comment = appstruct.pop('comment')
#
#         # here we merge all our parameters with the current expensesheet
#         merge_session_with_post(self.request.context, appstruct)
#
#         # We modifiy the expense status
#         try:
#             expense, status = self.set_expense_status(self.request.context)
#             self._store_communication(comment)
#             self.request.registry.notify(ExpenseStatusChanged(
#                 self.request,
#                 expense,
#                 status,
#                 comment,
#             ))
#         except Forbidden, err:
#             logger.exception(u"An access has been forbidden")
#             self.request.session.flash(err.message, queue='error')
#
#         return HTTPFound(
#             self.request.route_url(
#                 "expensesheet",
#                 id=self.request.context.id
#             )
#         )
#
#     def _store_communication(self, comment):
#         """
#             Stores a comment that would have been provided on expense state
#             change
#         """
#         # If there was a comment, we add it in the database
#         if comment is not None:
#             comment = Communication(user_id=self.request.user.id,
#                                     content=comment,
#                                     expense_sheet_id=self.request.context.id)
#             self.dbsession.add(comment)
#
#     def set_expense_status(self, expense):
#         """
#             Handle expense submission
#         """
#         params = dict(self.request.POST)
#         status = params['submit']
#         logger.debug(u"Setting a new status : %s" % status)
#         expense.set_status(status, self.request, self.request.user.id, **params)
#         expense.status_date = datetime.date.today()
#         return expense, status
#
#     def reset_success(self, appstruct):
#         """
#             Reset an expense
#         """
#         logger.debug(u"Resetting the expense")
#         if self.context.status == 'draft':
#             self.dbsession.delete(self.context)
#             self.session.flash(u"Votre feuille de notes de dépense de {0} {1} a \
# bien été réinitialisée".format(month_name(self.month), self.year))
#         else:
#             self.session.flash(u"Vous n'êtes pas autorisé à réinitialiser \
# cette feuille de notes de dépense")
#         cid = self.context.company_id
#         uid = self.context.user_id
#         url = self.request.route_url(
#             "user_expenses",
#             id=cid,
#             uid=uid,
#             _query=dict(year=self.year, month=self.month)
#         )
#         return HTTPFound(url)


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
        renderer="treasury/expense.mako",
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
