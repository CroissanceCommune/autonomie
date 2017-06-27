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
import datetime
import traceback
import deform

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPTemporaryRedirect,
)

from autonomie.exception import Forbidden
from autonomie.forms.payments import (
    ExpensePaymentSchema,
)
from autonomie.forms.expense import (
    ExpenseStatusSchema,
    PeriodSelectSchema,
    ExpenseLineSchema,
    ExpenseKmLineSchema,
    ExpenseSheetSchema,
    BookMarkSchema,
    get_list_schema,
)
from autonomie.models.expense import (
    ExpenseType,
    ExpenseTelType,
    ExpenseKmType,
    ExpenseSheet,
    ExpenseLine,
    ExpenseKmLine,
    Communication,
    get_expense_sheet_name,
)
from autonomie.events.expense import StatusChanged as ExpenseStatusChanged
from autonomie.utils.rest import (
    RestError,
    RestJsonRepr,
    add_rest_views,
    make_redirect_view,
)
from autonomie.models.user import User
from autonomie.utils.widgets import (
    Submit,
    PopUp,
    ViewLink,
)
from autonomie.export.excel import (
    make_excel_view,
    XlsExpense,
)
from autonomie.resources import (
    expense_js,
    admin_expense_js,
)
from autonomie.forms import (
    merge_session_with_post,
)
from autonomie.views import (
    BaseView,
    BaseListView,
    BaseFormView,
    submit_btn,
)
from autonomie.views.taskaction import StatusView
from autonomie.views.render_api import (
    month_name,
    format_account,
)
from autonomie.views.files import (
    get_add_file_link,
    FileUploadView,
)


logger = logging.getLogger(__name__)


class BookMarkHandler(object):
    """
        Wrapper for expense bookmarks
    """
    def __init__(self, request):
        self.request = request
        self.bookmarks = {}
        self.load_bookmarks_from_current_request()

    def load_bookmarks_from_current_request(self):
        session_datas = self.request.user.session_datas or {}
        expense_datas = session_datas.get('expense', {})
        self.bookmarks = expense_datas.get('bookmarks', {})

    def refresh(self):
        self.load_bookmarks_from_current_request()

    def store(self, item):
        """
            Store a bookmark (add/edit)
            :@param item: a dictionnary with the bookmark informations
        """
        id_ = item.get('id')
        if not id_:
            id_ = self._next_id()
            item['id'] = id_

        self.bookmarks[id_] = item
        self._save()
        return item

    def delete(self, id_):
        """
            Removes a bookmark
        """
        item = self.bookmarks.pop(id_, None)
        if item is not None:
            self._save()
        return item

    def _next_id(self):
        """
            Return the next available bookmark id
        """
        id_ = 1
        if self.bookmarks.keys():
            all_keys = [int(key) for key in self.bookmarks.keys()]
            id_ = max(all_keys) + 1
        return id_

    def _save(self):
        """
            Persist the bookmarks in the database
        """
        session_datas = self.request.user.session_datas or {}
        session_datas.setdefault('expense', {})['bookmarks'] = self.bookmarks
        if self.request.user.session_datas is None:
            self.request.user.session_datas = {}

        # NOte : Here we ensure passing through the __setitem__ method of our
        # MutableDict (see models.types for more informations)
        self.request.user.session_datas['expense'] = session_datas['expense']
        self.request.dbsession.merge(self.request.user)
        self.request.dbsession.flush()


def get_bookmarks(request):
    """
        Return the user's bookmarks
    """
    return BookMarkHandler(request).bookmarks.values()


def load_type_ids_from_expense(expense):
    """
    Load the ids of the expense types used in this expense

    :returns: a list of ids
    """
    res = []
    if getattr(expense, '__name__', None) == 'expense':
        for line in expense.lines:
            res.append(line.type_id)
        for line in expense.kmlines:
            res.append(line.type_id)

    return res


def expense_options(request):
    """
    Return options related to the expense configuration
    """
    # Load types already used in this expense
    current_expenses_used_types = load_type_ids_from_expense(request.context)

    options = {
        "expense_types": [],
        "expensekm_types": [],
        "expensetel_types": [],
    }
    for etype in ExpenseType.query():
        if etype.id in current_expenses_used_types or etype.active:
            key = "%s_types" % etype.type
            options[key].append(etype)

    options['categories'] = [
        {
            'value': '1',
            "label": u"Frais",
            'description': u"Frais liés au fonctionnement de l'entreprise"
        },
        {
            'value': '2',
            "label": u"Achats",
            'description': u"Frais concernant directement votre activité \
auprès de vos clients"
        }]

    options['bookmarks'] = get_bookmarks(request)

    expense_sheet = request.context
    month = expense_sheet.month
    year = expense_sheet.year

    date = datetime.date(year, month, 1)
    options['today'] = date

    return options


class ExpenseSheetJson(RestJsonRepr):
    """
        Wrapper for ExpenseSheet objects that allows to convert our sheet to
        json while cleanly handle the specific data types that need to be
        preformated before being rendered
    """
    schema = ExpenseSheetSchema()


class ExpenseLineJson(RestJsonRepr):
    """
        Wrapper for expenselines
    """
    schema = ExpenseLineSchema()


class ExpenseKmLineJson(RestJsonRepr):
    """
        Json wrapper for expense kilometric lines
    """
    schema = ExpenseKmLineSchema()


def get_period_form(request, action_url=""):
    """
        Return a form to select the period of the expense sheet
    """
    schema = PeriodSelectSchema().bind(request=request)
    form = deform.Form(
        schema=schema,
        buttons=(submit_btn,),
        method='GET',
        formid='period_form',
        action=action_url,
    )
    return form


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


def _get_expense_sheet(year, month, cid, uid):
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


def get_expensesheet_years(expenses):
    """
        List of years an expensesheet has been retrieved for
    """
    years = set([exp.year for exp in expenses])
    if not years:
        return [datetime.date.today().year]
    else:
        return years


def get_expensesheet_by_year(company):
    """
        Return expenses stored by year and users for display purpose
    """
    result = {}
    for year in get_expensesheet_years(company.expenses):
        result[year] = []
        for user in company.employees:
            expenses = [exp for exp in user.expenses if exp.year == year]
            result[year].append((user, expenses))
    return result


def expense_configured():
    """
        Return True if the expenses were already configured
    """
    length = 0
    for factory in (ExpenseType, ExpenseKmType, ExpenseTelType):
        length += factory.query().count()
    return length > 0


def company_expenses_view(request):
    """
        View that lists the expenseSheets related to the current company
    """
    title = u"Accès aux notes de dépense des employés de {0}"\
            .format(request.context.name)
    if not expense_configured():
        return dict(
            title=title,
            conf_msg=u"La déclaration des notes de dépense n'est pas encore \
accessible."
        )

    expense_sheets = get_expensesheet_by_year(request.context)
    user_buttons = {}
    cid = request.context.id
    # We add a period form for each user
    for user in request.context.employees:
        uid = user.id
        action_url = request.route_url("user_expenses", id=cid, uid=uid)
        form = get_period_form(request, action_url)
        popup = PopUp("user_expense_{0}".format(uid), u"Créer", form.render())
        request.popups[popup.name] = popup
        user_buttons[user.id] = popup.open_btn(css="btn btn-default")
    return dict(
        title=title,
        expense_sheets=expense_sheets,
        user_buttons=user_buttons,
        current_year=datetime.date.today().year
    )


def get_expense_sheet(request, year, month, cid, uid):
    """
        Return an expense sheet for the given period, add new one if there's no
        one yet
    """
    expense = _get_expense_sheet(year, month, cid, uid)
    if not expense:
        # If it has not already been accessed, we create a new one and
        # we flush it to ensure we can access its id in the view
        expense = get_new_expense_sheet(year, month, cid, uid)
        request.dbsession.add(expense)
        request.dbsession.flush()
    return expense


def expenses_access_view(request):
    """
        get/initialize the expense corresponding to the 4-uple:
            (year, month, user_id, company_id)
        Redirect to the expected expense page
        Should be called with post args
    """
    year, month = get_period(request)
    cid = request.context.id
    uid = request.matchdict.get('uid')
    expense = get_expense_sheet(request, year, month, cid, uid)
    # Here we use a temporary redirect since the expense we redirect too may
    # have change if it was reset
    return HTTPTemporaryRedirect(request.route_path(
        "expensesheet",
        id=expense.id)
    )


def get_expense_history(expensesheet):
    """
        Return the communication history for a given expensesheet
    """
    return expensesheet.communications


def get_payment_form(request, counter=None):
    """
    Return a payment form object
    """
    valid_btn = deform.Button(
        name='submit',
        value="paid",
        type='submit',
        title=u"Valider",
    )
    schema = ExpensePaymentSchema().bind(request=request)
    if request.context.__name__ == 'expense':
        action = request.route_path(
            "expensesheet",
            id=request.context.id,
            _query=dict(action='payment')
        )
    else:
        action = request.route_path(
            "expensesheet",
            id=-1,
            _query=dict(action='payment')
        )
    form = deform.Form(
        schema=schema,
        buttons=(valid_btn,),
        formid="paymentform",
        action=action,
        counter=counter,
    )
    return form


def notify_status_changed(request, status):
    """
    Fire An ExpenseStatusChanged event

    :param obj request: The Pyramid request object
    :param str status: The new status
    """
    request.registry.notify(
        ExpenseStatusChanged(request, request.context, status)
    )


class ExpenseSheetView(BaseFormView):
    """
        ExpenseSheet view
    """
    schema = ExpenseStatusSchema()
    add_template_vars = ('title', 'loadurl', "edit",
                         "communication_history")

    def __init__(self, request):
        super(ExpenseSheetView, self).__init__(request)
        expense_js.need()
        self.month = self.request.context.month
        self.year = self.request.context.year
        self.formcounter = None

    @property
    def communication_history(self):
        """
            Communication history data, will be carried to the template
        """
        return get_expense_history(self.request.context)

    @property
    def title(self):
        """
            Return the title of the page
        """
        return u"Notes de dépense de {0} pour la période de {1} {2}"\
            .format(
                format_account(self.request.context.user),
                month_name(self.month),
                self.year,
            )

    @property
    def buttons(self):
        """
            Return the buttons used for form submission
        """
        btns = []
        logger.debug(u"   + Available actions :")
        for action in self.request.context.get_next_actions():
            logger.debug(u"    * {0}".format(action.name))
            if action.allowed(self.request.context, self.request):
                logger.debug(u"     -> is allowed for the current user")
                if hasattr(self, "_%s_btn" % action.name):
                    func = getattr(self, "_%s_btn" % action.name)
                    btns.append(func())

        for action in ('paid',):
            if (
                self.request.has_permission('set_paid.estimation') and
                self.context.status == 'valid' and
                self.context.paid_status != 'resulted'
            ):
                btns.append(self._paid_btn())
        return btns

    def _reset_btn(self):
        """
            Return a reset button
        """
        return Submit(
            u"Réinitialiser",
            "reset",
            name="reset",
            request=self.request,
            confirm=u"Êtes-vous sûr de vouloir réinitialiser \
cette feuille de notes de dépense (toutes les modifications apportées seront \
perdues) ?")

    def _draft_btn(self):
        """
        Return a button to set the expense to draft again
        """
        msg = u"Annuler la mise en validation et repasser en brouillon"
        return Submit(
            msg,
            "draft",
            request=self.request,
        )

    def _wait_btn(self):
        """
            Return a button for requesting validation
        """
        return Submit(u"Demander la validation", "wait", request=self.request)

    def _valid_btn(self):
        """
            Return a validation button
        """
        return Submit(u"Valider le document", "valid", request=self.request)

    def _invalid_btn(self):
        """
            Return an invalidation button
        """
        return Submit(u"Invalider le document", "invalid", request=self.request)

    def _paid_form(self):
        """
        Return the form for payment registration
        """
        form = get_payment_form(self.request, self.formcounter)
        appstruct = {
            'amount': self.context.topay(),
            'come_from': self.request.current_route_path(),
        }
        form.set_appstruct(appstruct)
        self.formcounter = form.counter
        return form

    def _paid_btn(self):
        """
            Return a button to set a paid btn and a select to choose
            the payment mode
        """
        form = self._paid_form()
        title = u"Notifier un paiement"
        popup = PopUp("paidform", title, form.render())
        self.request.popups[popup.name] = popup
        return popup.open_btn(css='btn btn-primary')

    @property
    def edit(self):
        """
            return True if the current context is editable by the current user
        """
        return self.request.has_permission("edit_expense")

    @property
    def loadurl(self):
        """
            Returns a json representation of the current expense sheet
        """
        return self.request.route_path(
            "expensejson",
            id=self.request.context.id,
        )

    def before(self, form):
        """
        Prepopulate the form
        """
        # Here we override the form counter to avoid field ids conflict
        form.set_appstruct(self.request.context.appstruct())
        if self.request.has_permission('admin_expense'):
            btn = ViewLink(
                u"Revenir à la liste",
                "admin_expense",
                path="expenses",
            )
        else:
            btn = ViewLink(
                u"Revenir à la liste",
                "view_expense",
                path="company_expenses",
                id=self.request.context.company.id,
            )
        self.request.actionmenu.add(btn)
        btn = get_add_file_link(
            self.request,
            label=u"Déposer des justificatifs",
            perm="view_expense",
        )
        self.request.actionmenu.add(btn)

    def submit_success(self, appstruct):
        """
            Handle submission of the expense page, only on state change
            validation
        """
        logger.debug("#  Submitting expense sheet status form  #")
        logger.debug(appstruct)

        # Comment is now stored in a specific table
        comment = None
        if "comment" in appstruct:
            comment = appstruct.pop('comment')

        # here we merge all our parameters with the current expensesheet
        merge_session_with_post(self.request.context, appstruct)

        # We modifiy the expense status
        try:
            expense, status = self.set_expense_status(self.request.context)
            self._store_communication(comment)
            self.request.registry.notify(ExpenseStatusChanged(
                self.request,
                expense,
                status,
                comment,
            ))
        except Forbidden, err:
            logger.exception(u"An access has been forbidden")
            self.request.session.flash(err.message, queue='error')

        return HTTPFound(
            self.request.route_url(
                "expensesheet",
                id=self.request.context.id
            )
        )

    def _store_communication(self, comment):
        """
            Stores a comment that would have been provided on expense state
            change
        """
        # If there was a comment, we add it in the database
        if comment is not None:
            comment = Communication(user_id=self.request.user.id,
                                    content=comment,
                                    expense_sheet_id=self.request.context.id)
            self.dbsession.add(comment)

    def set_expense_status(self, expense):
        """
            Handle expense submission
        """
        params = dict(self.request.POST)
        status = params['submit']
        logger.debug(u"Setting a new status : %s" % status)
        expense.set_status(status, self.request, self.request.user.id, **params)
        expense.status_date = datetime.date.today()
        return expense, status

    def reset_success(self, appstruct):
        """
            Reset an expense
        """
        logger.debug(u"Resetting the expense")
        if self.context.status == 'draft':
            self.dbsession.delete(self.context)
            self.session.flash(u"Votre feuille de notes de dépense de {0} {1} a \
bien été réinitialisée".format(month_name(self.month), self.year))
        else:
            self.session.flash(u"Vous n'êtes pas autorisé à réinitialiser \
cette feuille de notes de dépense")
        cid = self.context.company_id
        uid = self.context.user_id
        url = self.request.route_url(
            "user_expenses",
            id=cid,
            uid=uid,
            _query=dict(year=self.year, month=self.month)
        )
        return HTTPFound(url)


class ExpenseStatusView(StatusView):
    """
    Expense status view
    """
    def notify(self, item, status):
        """
        Notify a status change
        """
        notify_status_changed(self.request, status)


class ExpensePaymentView(BaseFormView):
    """
    Called for setting a payment on an expensesheet
    """
    schema = ExpensePaymentSchema()
    title = u"Saisie d'un paiement"

    def redirect(self, come_from):
        if come_from is not None:
            return HTTPFound(come_from)
        else:
            return HTTPFound(
                self.request.route_path(
                    "expensesheet", id=self.request.context.id
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


def expensesheet_json_view(request):
    """
        Return an json encoded expensesheet
    """
    return dict(
        expense=ExpenseSheetJson(request.context),
        options=expense_options(request),
    )


class RestExpenseLine(BaseView):
    """
        Json-Rest api for expenseline handling
        /expenses/id/lines/{lid}
    """
    _schema = ExpenseLineSchema()
    factory = ExpenseLine
    key = "lines"
    model_wrapper = ExpenseLineJson

    @property
    def schema(self):
        """
            Return a bound schema
        """
        # Ensure all our colander.deferred values are set
        return self._schema.bind()

    def getOne(self):
        """
            get an expense line
        """
        lid = self.request.matchdict.get('lid')
        for line in getattr(self.request.context, self.key):
            if line.id == int(lid):
                return line
        raise RestError({}, 404)

    def get(self):
        """
            Rest get method : return a line
        """
        logger.debug("In the get method")
        return self.model_wrapper(self.getOne())

    def post(self):
        """
            Rest post method : add a line
        """
        logger.debug("In the post method")
        appstruct = self.request.json_body
        try:
            appstruct = self.schema.deserialize(appstruct)
        except colander.Invalid, err:
            traceback.print_exc()
            logger.exception("  - Erreur")
            logger.exception(appstruct)
            raise RestError(err.asdict(), 400)
        line = self.factory(**appstruct)

        line.sheet = self.request.context
        self.request.dbsession.add(line)
        self.request.dbsession.flush()
        return self.model_wrapper(line)

    def delete(self):
        """
            Rest delete method : delete a line
        """
        logger.debug("In the delete method")
        line = self.getOne()
        self.request.dbsession.delete(line)
        return dict(status="success")

    def put(self):
        """
            Rest put method : update a line
        """
        logger.debug("In the put method")
        line = self.getOne()
        appstruct = self.request.json_body
        try:
            appstruct = self.schema.deserialize(appstruct)
        except colander.Invalid, err:
            traceback.print_exc()
            logger.exception("  - Erreur")
            logger.exception(appstruct)
            raise RestError(err.asdict(), 400)
        line = merge_session_with_post(line, appstruct)
        self.request.dbsession.merge(line)
        self.request.dbsession.flush()
        return self.model_wrapper(line)


class RestExpenseKmLine(RestExpenseLine):
    """
        Rest iface for Expense kilometric lines
        Lines are compound by :
            * km : number of kilometers
            * start : the start point
            * end : the end point
            * date : the date
            * description : the description of the displacement context
    """
    _schema = ExpenseKmLineSchema()
    factory = ExpenseKmLine
    key = "kmlines"
    model_wrapper = ExpenseKmLineJson


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


class RestBookMarks(BaseView):
    """
        Json rest-api for expense bookmarks handling
    """
    _schema = BookMarkSchema()

    @property
    def schema(self):
        return self._schema.bind(request=self.request)

    def get(self):
        """
            Rest GET Method : get
        """
        return get_bookmarks(self.request)

    def post(self):
        """
            Rest POST method : add
        """
        logger.debug(u"In the bookmark edition")

        appstruct = self.request.json_body
        try:
            bookmark = self.schema.deserialize(appstruct)
        except colander.Invalid, err:
            traceback.print_exc()
            logger.exception("  - Error in posting bookmark")
            logger.exception(appstruct)
            raise RestError(err.asdict(), 400)

        handler = BookMarkHandler(self.request)
        bookmark = handler.store(bookmark)
        return bookmark

    def put(self):
        """
            Rest PUT method : edit
        """
        self.post()

    def delete(self):
        """
            Removes a bookmark
        """
        logger.debug(u"In the bookmark deletion view")

        handler = BookMarkHandler(self.request)

        # Retrieving the id from the request
        id_ = self.request.matchdict.get('id')

        bookmark = handler.delete(id_)

        # if None is returned => there was no bookmark with this id
        if bookmark is None:
            raise RestError({}, 404)
        else:
            return dict(status="success")


class ExpenseList(BaseListView):
    """
    expenses list

        payment_form

            The payment form is added as a popup and handled through javascript
            to set the expense id
    """
    title = u"Liste des notes de dépense de la CAE"
    schema = get_list_schema()
    sort_columns = dict(
        id_=ExpenseSheet.id,
        month=ExpenseSheet.month,
        name=User.lastname,
    )
    default_sort = 'month'
    default_direction = 'desc'
    add_template_vars = ('title', 'payment_formname',)

    @property
    def payment_formname(self):
        """
        Return a payment form name, add the form to the page popups as well
        """
        admin_expense_js.need()
        form_name = "payment_form"
        form = get_payment_form(self.request)
        form.set_appstruct({'come_from': self.request.current_route_path()})
        popup = PopUp(form_name, u"Saisir un paiement", form.render())
        self.request.popups[popup.name] = popup
        return form_name

    def query(self):
        query = ExpenseSheet.query().outerjoin(ExpenseSheet.user)
        return query

    def filter_search(self, query, appstruct):
        search = appstruct['search']
        if search and search != colander.null:
            query = query.filter(ExpenseSheet.id == search)
        return query

    def filter_year(self, query, appstruct):
        year = appstruct['year']
        if year and year not in (-1, colander.null):
            query = query.filter(ExpenseSheet.year == year)
        return query

    def filter_month(self, query, appstruct):
        month = appstruct['month']
        if month and month not in (-1, colander.null):
            query = query.filter(ExpenseSheet.month == month)
        return query

    def filter_owner(self, query, appstruct):
        user_id = appstruct['owner_id']
        if user_id and user_id not in (-1, colander.null):
            query = query.filter(ExpenseSheet.user_id == user_id)
        return query

    def filter_status(self, query, appstruct):
        status = appstruct['status']
        if status in ('wait', 'valid'):
            query = query.filter(ExpenseSheet.status == status)
        elif status in ('paid', 'resulted'):
            query = query.filter(ExpenseSheet.status == 'valid')
            query = query.filter(ExpenseSheet.paid_status == status)
        elif status == 'justified':
            query = query.filter(ExpenseSheet.justified == True)
        return query


def add_routes(config):
    """
    Add module's related routes
    """
    config.add_route("expenses", "/expenses")
    config.add_route("bookmark", "/bookmarks/{id:\d+}")
    config.add_route("bookmarks", "/bookmarks")

    traverse = '/companies/{id}'
    config.add_route(
        "company_expenses",
        "/company/{id}/expenses",
        traverse=traverse,
    )
    config.add_route(
        "user_expenses",
        "/company/{id}/{uid}/expenses",
        traverse=traverse,
    )

    traverse = "/expenses/{id}"
    config.add_route(
        "expensesheet",
        "/expenses/{id:\d+}",
        traverse=traverse
    )
    config.add_route(
        "expensejson",
        "/expenses/{id:\d+}.json",
        traverse=traverse,
    )
    config.add_route(
        "expensexlsx",
        "/expenses/{id:\d+}.xlsx",
        traverse=traverse,
    )
    config.add_route(
        "expenselines",
        "/expenses/{id:\d+}/lines",
        traverse=traverse,
    )
    config.add_route(
        "expenseline",
        "/expenses/{id:\d+}/lines/{lid}",
        traverse=traverse,
    )
    config.add_route(
        "expensekmlines",
        "/expenses/{id:\d+}/kmlines",
        traverse=traverse,
    )
    config.add_route(
        "expensekmline",
        "/expenses/{id:\d+}/kmlines/{lid}",
        traverse=traverse,
    )


def includeme(config):
    """
        Declare all the routes and views related to this module
    """
    add_routes(config)

    config.add_view(
        ExpenseList,
        route_name="expenses",
        permission="admin_expense",
        renderer="treasury/admin_expenses.mako",
    )

    config.add_view(
        company_expenses_view,
        route_name="company_expenses",
        renderer="treasury/expenses.mako",
        permission="list_expenses",
    )

    config.add_view(
        expenses_access_view,
        route_name="user_expenses",
        permission="add_expense",
    )

    config.add_view(
        ExpenseSheetView,
        route_name="expensesheet",
        renderer="treasury/expense.mako",
        permission="view_expense",
    )

    config.add_view(
        ExpenseStatusView,
        route_name="expensesheet",
        request_param='action=status',
        permission="edit_expense",
        renderer="base/formpage.mako",
    )
    config.add_view(
        ExpensePaymentView,
        route_name="expensesheet",
        request_param='action=payment',
        permission="add_payment",
        renderer="base/formpage.mako",
    )

    config.add_view(
        expensesheet_json_view,
        route_name="expensejson",
        xhr=True,
        renderer="json",
        permission="view_expense",
    )

    # Xls export
    config.add_view(
        make_excel_view(excel_filename, XlsExpense),
        route_name="expensexlsx",
        permission="view_expense",
    )
    # File attachment
    config.add_view(
        FileUploadView,
        route_name="expensesheet",
        renderer='base/formpage.mako',
        permission='add_file',
        request_param='action=attach_file',
    )

    # Rest interface
    redirect_to_expense = make_redirect_view("expensesheet")
    add_rest_views(
        config,
        "expenseline",
        RestExpenseLine,
        view_rights="view_expense",
        add_rights="edit_expense",
        edit_rights="edit_expense",
    )
    config.add_view(redirect_to_expense, route_name="expenseline")
    config.add_view(redirect_to_expense, route_name="expenselines")

    add_rest_views(
        config,
        "expensekmline",
        RestExpenseKmLine,
        view_rights="view_expense",
        add_rights="edit_expense",
        edit_rights="edit_expense",
    )
    config.add_view(redirect_to_expense, route_name="expensekmline")
    config.add_view(redirect_to_expense, route_name="expensekmlines")

    add_rest_views(
        config,
        "bookmark",
        RestBookMarks,
        view_rights="list_expenses",
        add_rights="add_expense",
        edit_rights='add_expense',
    )
