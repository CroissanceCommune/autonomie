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

from deform import Form
from pyramid.security import has_permission
from pyramid.httpexceptions import (
        HTTPFound,
        HTTPTemporaryRedirect,
        )

from autonomie.exception import Forbidden
from autonomie.views.forms.expense import (
    ExpenseStatusSchema,
    PeriodSelectSchema,
    ExpenseLineSchema,
    ExpenseKmLineSchema,
    ExpenseSheetSchema,
    BookMarkSchema,
    get_list_schema,
    STATUS_OPTIONS
)
from autonomie.views import BaseListView
from autonomie.models.treasury import (
    BaseExpenseLine,
    ExpenseType,
    ExpenseTelType,
    ExpenseKmType,
    ExpenseSheet,
    ExpenseLine,
    ExpenseKmLine,
    Communication,
)
from autonomie.events.expense import StatusChanged
from autonomie.views.base import BaseView
from autonomie.views.render_api import (
        month_name,
        format_account,
        )
from autonomie.utils.rest import (
        Apiv1Resp,
        RestError,
        RestJsonRepr,
        add_rest_views,
        make_redirect_view,
)
from autonomie.utils.views import submit_btn
from autonomie.utils.widgets import (
        Submit,
        PopUp,
        ViewLink,
        )
from autonomie.export.excel import (
        make_excel_view,
        ExcelExpense,
        )
from autonomie.views.forms import (
        merge_session_with_post,
        BaseFormView,
        )
from autonomie.resources import expense_js


log = logging.getLogger(__name__)


class BookMarkHandler(object):
    """
        Wrapper for expense bookmarks
    """
    def __init__(self, request):
        self.request = request
        session_datas = request.user.session_datas or {}
        expense_datas = session_datas.get('expense', {})
        self.bookmarks = expense_datas.get('bookmarks', {})

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


def expense_options(request):
    """
        Return options related to the expense configuration
    """
    options = dict()

    options["expensetypes"] = [
        {
        "label":u"{0} ({1})".format(e.label, e.code),
        "value":str(e.id)
        }for e in ExpenseType.query()\
                .filter(ExpenseType.active==True)
                .filter(ExpenseType.type=='expense')]

    options["kmtypes"] =  [
        {
        "label":u"{0} ({1})".format(e.label, e.code),
        "value":str(e.id),
        "amount":e.amount
        }for e in ExpenseKmType.query().filter(ExpenseKmType.active==True)]

    options["teltypes"] = [
        {
        "label":u"{0} ({1})".format(e.label, e.code),
        "value":str(e.id),
        "percentage":e.percentage
        }for e in ExpenseTelType.query().filter(ExpenseTelType.active==True)]

    options['categories'] = [{
        'value':'1',
        'label':u"Frais liés au fonctionnement de l'entreprise"
        },
        {
        'value':'2',
        'label':u"Frais concernant directement votre activité auprès de vos \
clients"
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
    form = Form(schema=schema, buttons=(submit_btn,), method='GET',
                            formid='period_form', action=action_url)
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
                .filter(ExpenseSheet.year==year)\
                .filter(ExpenseSheet.month==month)\
                .filter(ExpenseSheet.company_id==cid)\
                .filter(ExpenseSheet.user_id==uid).first()


def get_new_expense_sheet(year, month, cid, uid):
    """
        Return a new expense sheet for the given 4-uple
    """
    expense = ExpenseSheet()
    expense.year = year
    expense.month = month
    expense.company_id = cid
    expense.user_id = uid
    query = ExpenseTelType.query()
    query = query.filter(ExpenseTelType.active==True)
    teltypes = query.filter(ExpenseTelType.initialize==True)
    for type_ in teltypes:
        line = ExpenseLine(type_id=type_.id, ht=0, tva=0,
                description=type_.label)
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
    title = u"Accès aux notes de frais des employés de {0}"\
            .format(request.context.name)
    if not expense_configured():
        return dict(title=title,
            conf_msg=u"La déclaration des notes de frais n'est pas encore \
accessible.")

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
        user_buttons[user.id] = popup.open_btn(css="btn")
    return dict(title=title,
            expense_sheets=expense_sheets,
            user_buttons=user_buttons,
            current_year=datetime.date.today().year)


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
    return HTTPTemporaryRedirect(request.route_path("expense", id=expense.id))


def get_expense_history(expensesheet):
    """
        Return the communication history for a given expensesheet
    """
    return expensesheet.communications


class ExpenseSheetView(BaseFormView):
    """
        ExpenseSheet view
    """
    schema = ExpenseStatusSchema()
    add_template_vars = ('title', 'loadurl', 'period_form', "edit",
                         "communication_history")

    def __init__(self, request):
        super(ExpenseSheetView, self).__init__(request)
        expense_js.need()
        self.month = self.request.context.month
        self.year = self.request.context.year
        self.period_form = self.get_period_form()

    def get_period_form(self):
        """
            Return the form used to ask a period
        """
        cid = self.request.context.company_id
        uid = self.request.context.user_id
        url = self.request.route_url("user_expenses", id=cid, uid=uid)
        return get_period_form(self.request, url)

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
        return u"Notes de frais de {0} pour la période de {1} {2}"\
                .format(format_account(self.request.context.user),
                        month_name(self.month),
                        self.year)

    @property
    def buttons(self):
        """
            Return the buttons used for form submission
        """
        btns = []
        log.debug(u"   + Available actions :")
        for action in self.request.context.get_next_actions():
            log.debug(u"    * {0}".format(action.name))
            if action.allowed(self.request.context, self.request):
                log.debug(u"     -> is allowed for the current user")
                if hasattr(self, "_%s_btn" % action.name):
                    func = getattr(self, "_%s_btn" % action.name)
                    btns.append(func())
        return btns

    def _reset_btn(self):
        """
            Return a reset button
        """
        return Submit(u"Réinitialiser", "reset", name="reset",
                        request=self.request,
                        confirm=u"Êtes-vous sûr de vouloir réinitialiser \
cette feuille de notes de frais (toutes les modifications apportées seront \
perdues) ?")

    def _wait_btn(self):
        """
            Return a button for requesting validation
        """
        return Submit(u"Demander la validation", "wait", request=self.request)

    def _valid_btn(self):
        """
            Return a validation button
        """
        return Submit(u"Valider", "valid", request=self.request)

    def _invalid_btn(self):
        """
            Return an invalidation button
        """
        return Submit(u"Invalider", "invalid", request=self.request)

    def _resulted_btn(self):
        """
            Return a button to set the expense as resulted
        """
        return Submit(u"Notifier le paiement", "resulted", request=self.request)

    @property
    def edit(self):
        """
            return True if the current context is editable by the current user
        """
        return has_permission("edit", self.request.context, self.request)

    @property
    def loadurl(self):
        """
            Returns a json representation of the current expense sheet
        """
        return self.request.route_path("expensejson",
                id=self.request.context.id)

    def before(self, form):
        """
            Prepopulate the form
        """
        self.period_form.set_appstruct(self.request.context.appstruct())
        # Here we override the form counter to avoid field ids conflict
        form.counter = self.period_form.counter
        form.set_appstruct(self.request.context.appstruct())
        # Ici on spécifie un template qui permet de rendre nos boutons de
        # formulaires
        form.widget.template = "autonomie:deform_templates/form.pt"
        btn = ViewLink(u"Revenir à la liste", "view", path="company_expenses",
                id=self.request.context.company.id)
        self.request.actionmenu.add(btn)

    def submit_success(self, appstruct):
        """
            Handle submission of the expense page, only on state change
            validation
        """
        log.debug("Submitting expense sheet status form")

        # Comment is now stored in a specific table
        comment = None
        if appstruct.has_key("comment"):
            comment = appstruct.pop('comment')

        # here we merge all our parameters with the current expensesheet
        merge_session_with_post(self.request.context, appstruct)

        # We modifiy the expense status
        try:
            expense, status = self.set_expense_status(self.request.context)
            self._store_communication(comment)
            self.request.registry.notify(StatusChanged(
                self.request,
                expense,
                status,
                comment,
                ))
        except Forbidden, err:
            self.request.session.flash(err.message, queue='error')


        return HTTPFound(self.request.route_url("expense",
                                                id=self.request.context.id))

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
        expense.set_status(status, self.request, self.request.user.id, **params)
        return expense, status

    def reset_success(self, appstruct):
        """
            Reset an expense
        """
        log.debug(u"Resetting the expense")
        if self.request.context.status == 'draft':
            self.dbsession.delete(self.request.context)
            self.session.flash(u"Votre feuille de notes de frais de {0} {1} a \
bien été réinitialisée".format(month_name(self.month), self.year))
        else:
            self.session.flash(u"Vous n'êtes pas autorisé à réinitialiser \
cette feuille de notes de frais")
        cid = self.request.context.company_id
        uid = self.request.context.user_id
        url = self.request.route_url("user_expenses", id=cid, uid=uid,
                _query=dict(year=self.year, month=self.month))
        return HTTPFound(url)


def expensesheet_json_view(request):
    """
        Return an json encoded expensesheet
    """
    return dict(expense=ExpenseSheetJson(request.context),
                options=expense_options(request))


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
        log.debug("In the get method")
        return self.model_wrapper(self.getOne())

    def post(self):
        """
            Rest post method : add a line
        """
        log.debug("In the post method")
        appstruct = self.request.json_body
        try:
            appstruct = self.schema.deserialize(appstruct)
        except colander.Invalid, err:
            traceback.print_exc()
            log.exception("  - Erreur")
            log.exception(appstruct)
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
        log.debug("In the delete method")
        line = self.getOne()
        self.request.dbsession.delete(line)
        return dict(status="success")

    def put(self):
        """
            Rest put method : update a line
        """
        log.debug("In the put method")
        line = self.getOne()
        appstruct = self.request.json_body
        try:
            appstruct = self.schema.deserialize(appstruct)
        except colander.Invalid, err:
            traceback.print_exc()
            log.exception("  - Erreur")
            log.exception(appstruct)
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



class Expensev1(BaseView):
    """
        Rest api for expense line add
        Here we manage dynamically the targetted expense sheet regarding the
        date of the given expense.
        An expense is included in the month it has been edited
    """
    _schema = ExpenseLineSchema()
    _schema_km = ExpenseKmLineSchema()
    factory = ExpenseLine
    factory_km = ExpenseKmLine
    model_wrapper = ExpenseLineJson
    model_wrapper_km = ExpenseKmLineJson

    def schema(self, appstruct):
        """
            Returns the appropriate schema used to validate input datas
        """
        if self.is_kmline(appstruct):
            return self._schema_km.bind()
        else:
            return self._schema.bind()

    def makeOne(self, appstruct):
        """
            Make a model using the appropriate factory
        """
        if self.is_kmline(appstruct):
            return self.factory_km(**appstruct)
        else:
            return self.factory(**appstruct)

    def wrap(self, model):
        """
            Wrap the model with appropriate json formatter
        """
        if hasattr(model, 'start'):
            return self.model_wrapper_km(model)
        else:
            return self.model_wrapper(model)

    def get_sheet(self, appstruct):
        """
            Return the sheet related to the given appstruct
        """
        uid = self.request.user.id
        # TODO : les utilisateurs avec plusieurs entreprises
        if len(self.request.user.companies) != 1:
            traceback.print_exc()
            log.exception("  - Erreur")
            raise RestError({}, 403)
        cid = self.request.user.companies[0].id
        date = appstruct['date']
        sheet = get_expense_sheet(self.request, date.year, date.month, cid, uid)
        if sheet.status not in ('draft', 'invalid',):
            traceback.print_exc()
            log.exception("  - Erreur")
            raise RestError({}, 403)
        return sheet

    def is_kmline(self, appstruct):
        """
            return True if the current edited line is a km line
        """
        return 'start' in appstruct.keys()

    def getOne(self):
        id_ = self.request.matchdict.get('id')
        line = BaseExpenseLine.get(id_)
        if line is not None:
            return line
        traceback.print_exc()
        log.exception("  - Erreur")
        raise RestError({}, 404)

    def get(self):
        return Apiv1Resp(self.wrap(self.getOne()))

    def addOne(self, edit=False):
        appstruct = self.request.json_body
        schema = self.schema(appstruct)
        try:
            appstruct = schema.deserialize(appstruct)
        except colander.Invalid, err:
            traceback.print_exc()
            log.exception("  - Erreur")
            raise RestError(err.asdict(), 400)
        # Here an error is raised if the next steps are forbidden
        sheet = self.get_sheet(appstruct)
        if edit:
            line = self.getOne()
            line = merge_session_with_post(line, appstruct)
            self.request.dbsession.merge(line)
        else:
            line = self.makeOne(appstruct)
            line.sheet = sheet
            self.request.dbsession.add(line)
        self.request.dbsession.flush()
        return Apiv1Resp(self.wrap(line))

    def post(self):
        return self.addOne()

    def put(self):
        return self.addOne(edit=True)

    def delete(self):
        line = self.getOne()
        self.request.dbsession.delete(line)
        return Apiv1Resp({'message':u"Successfully deleted"})


def expense_optionsv1(request):
    """
        Return the options for expense edition (type of expenses, associated
        datas)
    """
    return dict(status='success', result=expense_options(request))


def excel_filename(request):
    """
        return an excel filename based on the request context
    """
    exp = request.context
    return u"ndf_{0}_{1}_{2}_{3}.xlsx".format(exp.year, exp.month,
            exp.user.lastname, exp.user.firstname)


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
        log.debug(u"In the bookmark edition")

        appstruct = self.request.json_body
        try:
            bookmark = self.schema.deserialize(appstruct)
        except colander.Invalid, err:
            traceback.print_exc()
            log.exception("  - Error in posting bookmark")
            log.exception(appstruct)
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
        log.debug(u"In the bookmark deletion view")

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
    title = u"Notes de frais"
    schema = get_list_schema()
    sort_columns = dict(month=ExpenseSheet.month)
    default_sort = 'month'
    default_direction = 'desc'

    def query(self):
        return ExpenseSheet.query()

    def filter_search(self, query, appstruct):
        search = appstruct['search']
        if search:
            query = query.filter(ExpenseSheet.id==search)
        return query

    def filter_year(self, query, appstruct):
        year = appstruct['year']
        if year:
            query = query.filter(ExpenseSheet.year==year)
        return query

    def filter_month(self, query, appstruct):
        month = appstruct['month']
        if month and month != -1:
            query = query.filter(ExpenseSheet.month==month)
        return query

    def filter_owner(self, query, appstruct):
        user_id = appstruct['owner_id']
        if user_id and user_id != -1:
            query = query.filter(ExpenseSheet.user_id==user_id)
        return query

    def filter_status(self, query, appstruct):
        status = appstruct['status']
        if status != 'all':
            query = query.filter(ExpenseSheet.status==status)
        else:
            interesting_status = [i[1] for i in STATUS_OPTIONS]
            query = query.filter(ExpenseSheet.status.in_(interesting_status))
        return query


def includeme(config):
    """
        Declare all the routes and views related to this module
    """
    # Routes
    traverse = '/companies/{id}'

    config.add_route("expenses", "/expenses")

    config.add_route("company_expenses",
            "/company/{id}/expenses",
            traverse=traverse)

    config.add_route("user_expenses",
            "/company/{id}/{uid}/expenses",
            traverse=traverse)

    traverse = "/expenses/{id}"

    config.add_route("expense",
            "/expenses/{id:\d+}",
            traverse=traverse)
    config.add_route("expensejson",
            "/expenses/{id:\d+}.json",
            traverse=traverse)
    config.add_route("expensexlsx",
            "/expenses/{id:\d+}.xlsx",
            traverse=traverse)
    config.add_route("expenselines",
            "/expenses/{id:\d+}/lines",
            traverse=traverse)
    config.add_route("expenseline",
            "/expenses/{id:\d+}/lines/{lid}",
            traverse=traverse)
    config.add_route("expensekmlines",
            "/expenses/{id:\d+}/kmlines",
            traverse=traverse)
    config.add_route("expensekmline",
            "/expenses/{id:\d+}/kmlines/{lid}",
            traverse=traverse)

    config.add_route("bookmark", "/bookmarks/{id:\d+}")
    config.add_route("bookmarks", "/bookmarks")

    #views
    config.add_view(ExpenseList,
        route_name="expenses",
        permission="admin",
        renderer="treasury/admin_expenses.mako")

    config.add_view(company_expenses_view,
        route_name="company_expenses",
        renderer="treasury/expenses.mako",
        permission="edit")

    config.add_view(expenses_access_view,
        route_name="user_expenses",
        permission="edit")

    config.add_view(ExpenseSheetView,
        route_name="expense",
        renderer="treasury/expense.mako")

    config.add_view(expensesheet_json_view,
        route_name="expensejson",
        xhr=True,
        renderer="json")

    # Excel export
    config.add_view(make_excel_view(excel_filename, ExcelExpense),
            route_name="expensexlsx")

    # Rest interface
    redirect_to_expense = make_redirect_view("expense")
    add_rest_views(config, "expenseline", RestExpenseLine)
    config.add_view(redirect_to_expense, route_name="expenseline")
    config.add_view(redirect_to_expense, route_name="expenselines")
    add_rest_views(config, "expensekmline", RestExpenseKmLine)
    config.add_view(redirect_to_expense, route_name="expensekmline")
    config.add_view(redirect_to_expense, route_name="expensekmlines")

    # Since the edition of bookmarks is done directly on the current user model
    # View rights are sufficient to access those views
    add_rest_views(config, "bookmark", RestBookMarks, edit_rights='view')


    # V1 Rest Api
    config.add_route("expenselinev1s", "/api/v1/expenses")
    config.add_route("expenselinev1", "/api/v1/expenses/{id}",
            traverse='expenselines/{id}')
    config.add_route("expenseoptionsv1", "/api/v1/expenseoptions")

    add_rest_views(config, "expenselinev1", Expensev1)
    config.add_view(expense_optionsv1,
            route_name="expenseoptionsv1",
            renderer="json")
