# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
import datetime
import deform
import logging

from collections import OrderedDict
from sqlalchemy import distinct, desc

from autonomie_base.models.base import DBSESSION
from autonomie.models.user.user import User
from autonomie.models.expense.sheet import ExpenseSheet
from autonomie.models.expense.types import (
    ExpenseType,
    ExpenseKmType,
    ExpenseTelType,
)
from autonomie.utils.widgets import (
    PopUp,
)
from autonomie.resources import admin_expense_js
from autonomie.forms.expense import (
    get_list_schema,
)

from autonomie.views import (
    BaseListView,
    submit_btn,
)
from autonomie.views.expenses.utils import get_payment_form

logger = logging.getLogger(__name__)


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
        if month and month not in (-1, colander.null, '-1'):
            query = query.filter(ExpenseSheet.month == month)
        return query

    def filter_owner(self, query, appstruct):
        user_id = appstruct.get('owner_id', None)
        if user_id and user_id not in ('', -1, colander.null):
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
        else:
            query = query.filter(ExpenseSheet.status.in_(('valid', 'wait')))
        return query


def expense_configured():
    """
        Return True if the expenses were already configured
    """
    length = 0
    for factory in (ExpenseType, ExpenseKmType, ExpenseTelType):
        length += factory.query().count()
    return length > 0


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


def get_expensesheet_years(company):
    """
    List of years an expensesheet has been retrieved for
    """
    query = DBSESSION().query(distinct(ExpenseSheet.year)).filter_by(
        company_id=company.id
    )
    years = [data[0] for data in query.order_by(desc(ExpenseSheet.year))]

    today = datetime.date.today()
    if today.year not in years:
        years.insert(0, today.year)
    return years


def get_expensesheet_by_year(company):
    """
        Return expenses stored by year and users for display purpose
    """
    result = OrderedDict()
    for year in get_expensesheet_years(company):
        result[year] = []
        for user in company.employees:
            expenses = [exp for exp in user.expenses
                        if exp.year == year and exp.company_id == company.id]
            result[year].append((user, expenses))

    return result


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

    return dict(
        title=title,
        expense_sheets=expense_sheets,
        current_year=datetime.date.today().year,
        several_users=len(request.context.employees) > 1,
    )


def add_routes(config):
    config.add_route(
        "company_expenses",
        "/company/{id}/expenses",
        traverse='/companies/{id}',
    )


def add_views(config):
    config.add_view(
        ExpenseList,
        route_name="expenses",
        permission="admin.expensesheet",
        renderer="expenses/admin_expenses.mako",
    )

    config.add_view(
        company_expenses_view,
        route_name="company_expenses",
        renderer="expenses/expenses.mako",
        permission="list_expenses",
    )


def includeme(config):
    add_routes(config)
    add_views(config)
