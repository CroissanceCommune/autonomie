# -*- coding: utf-8 -*-
# * File Name : expense.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 15-02-2013
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Expense handling view
"""
import logging
import colander


from fanstatic import Resource
from deform import Form
from pyramid.renderers import render

from autonomie.utils.forms import merge_session_with_post
from autonomie.views.forms.expense import ExpenseStatusSchema
from autonomie.views.forms.expense import PeriodSelectSchema
from autonomie.views.forms.expense import ExpenseLineSchema
from autonomie.views.forms.expense import ExpenseKmLineSchema
from autonomie.views.forms.expense import ExpenseSheetSchema
from autonomie.models.treasury import ExpenseType
from autonomie.models.treasury import ExpenseTelType
from autonomie.models.treasury import ExpenseKmType
from autonomie.models.treasury import ExpenseSheet
from autonomie.models.treasury import ExpenseLine
from autonomie.models.treasury import ExpenseKmLine
from autonomie.views.base import BaseView
from autonomie.views.forms.utils import BaseFormView
from autonomie.utils.rest import RestError
from autonomie.utils.rest import RestJsonRepr
from autonomie.resources import lib_autonomie
from js.jqueryui import effects_highlight
from js.jqueryui import effects_shake
from autonomie.resources import backbone
from autonomie.resources import templates
from autonomie.resources import tools


log = logging.getLogger(__name__)


expense_js = Resource(lib_autonomie, "js/expense.js", depends=[backbone,
    templates, tools, effects_highlight, effects_shake])


def expense_options():
    """
        Return options related to the expense configuration
    """
    options = dict()
    options["expensetypes"] = [{"label":e.label, "value":e.code}
             for e in ExpenseType.query().filter(ExpenseType.type=='expense')]
    options["kmtypes"] =  [{"label":e.label, "value":e.code,
                                        "amount":e.amount}
                                                for e in ExpenseKmType.query()]
    options["teltypes"] = [{"label":e.label, "value":e.code,
                                        "percentage":e.percentage}
                                               for e in ExpenseTelType.query()]
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
    schema = ExpenseKmLineSchema()


class ExpensePage(BaseFormView):
    """
        Display the expense page
    """
    schema = ExpenseStatusSchema()
    period_schema = PeriodSelectSchema()
    title = u"Notes de frais"
    buttons = ()
    add_template_vars = ('title', 'jsoptions', 'expensesheet', 'period_form')

    def __init__(self, request):
        super(ExpensePage, self).__init__(request)
        expense_js.need()
        self.year = None
        self.month = None
        self.period_form = self.get_period_form()
        self.expense = self._expense()

    def get_period_form(self):
        """
            Return the form used for the expense period selection
        """
        schema = self.period_schema.bind(request=self.request)
        form = Form(schema=schema, buttons=(), method='GET',
                                        formid='period_form')
        form.set_appstruct(self.submit_period())
        return form

    def submit_period(self):
        """
            Handle the period form submission
            An expense sheet is related to a period that is selected
            through GET params
        """
        schema = self.period_schema.bind(request=self.request)
        try:
            appstruct = schema.deserialize(self.request.GET)
        except colander.Invalid:
            appstruct = schema.deserialize({})
        self.year = appstruct['year']
        self.month = appstruct['month']
        return appstruct

    def _expense(self):
        """
            Return the expense we are currently editing
            An expense is selected regarding a 4-uple:
                (user_id, company_id, year, month)
        """
        cid = self.request.context.id
        user_id = self.request.matchdict['uid']
        expense = ExpenseSheet.query()\
                .filter(ExpenseSheet.year==self.year)\
                .filter(ExpenseSheet.month==self.month)\
                .filter(ExpenseSheet.company_id==cid)\
                .filter(ExpenseSheet.user_id==user_id).first()
        if not expense:
            # If it has not already been accessed, we create a new one and
            # we flush it to ensure we can access its id in the view
            expense = ExpenseSheet()
            expense.year = self.year
            expense.month = self.month
            expense.company_id = cid
            expense.user_id = user_id
            for type_ in ExpenseTelType.query():
                line = ExpenseLine(code=type_.code, ht=0, tva=0,
                        description=type_.label)
                expense.lines.append(line)
            self.dbsession.add(expense)
            self.dbsession.flush()
        return expense

    @property
    def expensesheet(self):
        """
            Returns a json representation of the current expense sheet
        """
        return render('json', ExpenseSheetJson(self.expense))

    @property
    def jsoptions(self):
        """
            Return the js options needed for the client side app setup
        """
        return render('json', expense_options())

    def before(self, form):
        """
            Prepopulate the form
        """
        # Here we override the form counter to avoid field ids conflict
        form.counter = self.period_form.counter
        form.set_appstruct(self.expense.appstruct())

    def submit_success(self, appstruct):
        """
            Handle submission of the expense status form
        """
        # Maybe one submit func for each available status should be fun
        pass


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
        # Ensure all our colander.deferred values are set
        return self._schema.bind()

    def getOne(self):
        """
            get an expense line
        """
        lid = self.request.matchdict.get('lid')
        expense = self.request.context
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
            import traceback
            traceback.print_exc()
            log.exception("  - Erreur")
            raise RestError(err.asdict(), 400)
        line = self.factory(**appstruct)
        line.sheet = self.request.context
        self.request.dbsession.add(line)
        return self.schema.serialize(appstruct)

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
            import traceback
            traceback.print_exc()
            log.exception("  - Erreur")
            raise RestError(err.asdict(), 400)
        line = merge_session_with_post(line, appstruct)
        self.request.dbsession.merge(line)
        return self.schema.serialize(appstruct)


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


def add_rest_iface(config, route_name, factory):
    config.add_view(factory,
            attr='get',
            route_name=route_name,
            renderer="json",
            request_method='GET',
            permission='view')
    config.add_view(factory,
            attr='post',
            # C pas beau je sais
            route_name=route_name + "s",
            renderer="json",
            request_method='POST',
            permission='add')
    config.add_view(factory,
            attr='put',
            route_name=route_name,
            renderer="json",
            request_method='PUT',
            permission="edit")
    config.add_view(factory,
            attr='delete',
            route_name=route_name,
            renderer="json",
            request_method='DELETE',
            permission="edit")



def includeme(config):
    traverse = '/companies/{id}'
    config.add_route("company_expenses",
            "/company/{id}/{uid}/expenses/",
            traverse=traverse)
    config.add_route("expense",
            "/expenses/{id:\d+}",
            traverse="/expenses/{id}")
    config.add_route("expenselines",
            "/expenses/{id:\d+}/lines/",
            traverse="/expenses/{id}")
    config.add_route("expenseline",
            "/expenses/{id:\d+}/lines/{lid}",
            traverse="/expenses/{id}")

    config.add_route("expensekmlines",
            "/expenses/{id:\d+}/kmlines/",
            traverse="/expenses/{id}")
    config.add_route("expensekmline",
            "/expenses/{id:\d+}/kmlines/{lid}",
            traverse="/expenses/{id}")

    config.add_view(ExpensePage,
            route_name="company_expenses",
            renderer="treasury/expenses.mako")

    add_rest_iface(config, "expenseline", RestExpenseLine)
    add_rest_iface(config, "expensekmline", RestExpenseKmLine)



#    config.add_view(expense_get,
#                    route_name="expense",
#                    renderer="json",
#                    request_method="GET",
#                    xhr=True)
#
##    config.add_view(ExpenseJSON,
#                    route_name="expenses",
#                    renderer="json",
#                    request_method="GET",
#                    xhr=True)
