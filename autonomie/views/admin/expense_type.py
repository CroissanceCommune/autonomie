# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import datetime
from sqlalchemy import (desc, distinct)
from pyramid.httpexceptions import HTTPFound
from autonomie.compute.math_utils import convert_to_int
from autonomie.models.expense.types import (
    ExpenseType,
    ExpenseKmType,
    ExpenseTelType,
)

from autonomie.utils.widgets import Link

from autonomie.views import (
    BaseView,
    DisableView,
    BaseAddView,
    BaseEditView,
)
from autonomie.forms.admin.expense_type import (
    get_expense_type_schema,
    get_expense_kmtype_schema,
    get_expense_teltype_schema,
)

from autonomie.views.admin.tools import (
    AdminCrudListView,
)


def _get_year_from_request(request):
    """
    Retrieve the current year from the request
    Usefull for ExpenseKmType edition

    :param obj request: The Pyramid request object
    :returns: A year
    :rtype: int
    """
    return convert_to_int(request.matchdict['year'], datetime.date.today().year)


class ExpenseKmTypesIndexView(BaseView):
    """
    Entry point to the km expense types configuration
    """

    def _get_menus(self):
        """
        Return the menu entries
        """
        return [
            dict(
                label=u"Retour",
                route_name="admin_expense",
                icon="fa fa-step-backward"
            )
        ]

    def _get_year_options(self):
        """
        Return the year selection options to be provided
        """
        years = [
            a[0]
            for a in self.request.dbsession.query(
                distinct(ExpenseKmType.year)
            )
            if a[0]
        ]
        today = datetime.date.today()
        years.append(today.year)
        years.append(today.year + 1)

        years = list(set(years))
        years.sort()
        return years

    def __call__(self):
        return dict(
            years=self._get_year_options(),
            menus=self._get_menus(),
            admin_path="/admin/expenses/expensekm",
            title=u"Configuration des frais kilométriques"
        )


class ExpenseTypeListView(AdminCrudListView):
    columns = [
        u"Libellé", u"Compte de charge"
    ]
    title = u"Configuration des types de dépenses"
    factory = ExpenseType
    back_route = "admin_expense"

    def stream_columns(self, expense_type):
        """
        Stream a column object (called from within the template)

        :param obj expense_type: The object to display
        :returns: A generator of labels representing the different columns of
        our list
        :rtype: generator
        """
        yield expense_type.label or u"Non renseigné"
        yield expense_type.code or "Aucun"

    @classmethod
    def get_type(cls):
        return cls.factory.__mapper_args__['polymorphic_identity']

    def _get_item_url(self, expense_type, action=None):
        """
        shortcut for route_path calls
        """
        query = dict(self.request.GET)
        if action is not None:
            query['action'] = action

        return self.request.route_path(
            "/admin/expenses/%s/{id}" % self.get_type(),
            id=expense_type.id,
            _query=query,
            **self.request.matchdict
        )

    def stream_actions(self, expense_type):
        """
        Stream the actions available for the given expense_type object
        :param obj expense_type: ExpenseType instance
        :returns: List of 4-uples (url, label, title, icon,)
        """
        yield Link(
            self._get_item_url(expense_type),
            u"Voir/Modifier",
            icon=u"pencil",
        )
        if expense_type.active:
            yield Link(
                self._get_item_url(expense_type, action='disable'),
                u"Désactiver",
                title=u"La TVA n'apparaitra plus dans l'interface",
                icon=u"remove",
            )
        else:
            yield Link(
                self._get_item_url(expense_type, action='disable'),
                u"Activer",
                title=u"La TVA apparaitra dans l'interface",
            )

    def load_items(self, year=None):
        """
        Return the sqlalchemy models representing current queried elements
        :rtype: SQLAlchemy.Query object
        """
        items = self.factory.query().filter(
            self.factory.type == self.get_type()
        ).order_by(desc(self.factory.active)).order_by(self.factory.id)
        return items

    def get_addurl(self):
        """
        Return the url for the add view

        :returns: The url to access the add form
        :rtype: str
        """
        query = dict(self.request.GET)
        query['action'] = 'new'

        return self.request.route_path(
            '/admin/expenses/%s' % self.get_type(),
            _query=query,
            **self.request.matchdict
        )


class ExpenseKmTypeListView(ExpenseTypeListView):
    columns = [
        u"Libellé",
        u"Compte de charge",
        u"Indemnité kilométrique"
    ]

    factory = ExpenseKmType
    back_route = "/admin/expenses/expensekm/"

    @property
    def title(self):
        title = (
            u"Configuration des types de dépenses kilométriques pour "
            u"l'année {0}".format(_get_year_from_request(self.request))
        )
        return title

    def load_items(self, year=None):
        """
        Load the items we will display

        :returns: A SQLAlchemy query
        """
        query = ExpenseTypeListView.load_items(self)
        if year is None:
            year = _get_year_from_request(self.request)
        query = query.filter_by(year=year)
        return query

    def stream_columns(self, expense_type):
        yield expense_type.label or u"Non renseigné"
        yield expense_type.code or "Aucun"
        yield u"%s €/km" % (expense_type.amount or 0)

    def _get_duplicate_url(self):
        """
        Return the duplication url
        """
        return self.request.current_route_path(
            _query={'action': 'duplicate'}
        )

    def _get_duplicate_from_previous_url(self):
        """
        Return the duplicate from previous url
        """
        return self.request.current_route_path(
            _query={'action': 'duplicate', 'from_previous': '1'}
        )

    def get_actions(self, items):
        """
        Return the description of additionnal main actions buttons

        :rtype: generator
        """
        current_year = datetime.date.today().year
        year = _get_year_from_request(self.request)

        # if we've got datas and we're not in the last year
        if items.count() > 0 and year != current_year + 1:
            yield Link(
                self._get_duplicate_url(),
                label=u"Dupliquer cette grille vers l'année suivante "
                u"(%s)" % (year + 1),
                icon=u"fa fa-copy",
                css=u"btn btn-default"
            )

        # If previous year there were some datas configured
        if self.load_items(year - 1).count() > 0:
            yield Link(
                self._get_duplicate_from_previous_url(),
                label=u"Recopier la grille de l'année précédente "
                u"(%s)" % (year - 1),
                icon=u"fa fa-copy",
                css=u"btn btn-default"
            )


class ExpenseTelTypeListView(ExpenseTypeListView):
    columns = [
        u"Libellé",
        u"Compte de charge",
        u"Pourcentage indemnisé"
    ]

    title = u"Configuration des types de dépenses kilométriques"
    factory = ExpenseTelType

    def stream_columns(self, expense_type):
        yield expense_type.label or u"Non renseigné"
        yield expense_type.code or "Aucun"
        yield u"%s %%" % (
            expense_type.percentage or 0
        )


class ExpenseTypeDisableView(DisableView):
    disable_msg = u"L'élément a bien été désactivé"
    enable_msg = u"L'élément a bien été activé"
    factory = ExpenseType

    @classmethod
    def get_type(cls):
        return cls.factory.__mapper_args__['polymorphic_identity']

    @property
    def redirect_route(self):
        return "/admin/expenses/%s" % self.get_type()


class ExpenseKmTypeDisableView(ExpenseTypeDisableView):
    factory = ExpenseKmType

    def redirect(self):
        """
        Custom redirect to keep the 'year' param
        """
        return HTTPFound(
            self.request.route_path(self.redirect_route, year=self.context.year)
        )


class ExpenseTelTypeDisableView(ExpenseTypeDisableView):
    factory = ExpenseTelType


class ExpenseTypeAddView(BaseAddView):
    add_template_vars = ('menus', 'help_msg')
    factory = ExpenseType
    schema = get_expense_type_schema()
    title = u"Ajouter"

    @classmethod
    def get_type(cls):
        return cls.factory.__mapper_args__['polymorphic_identity']

    @property
    def redirect_route(self):
        return "/admin/expenses/%s" % self.get_type()

    @property
    def menus(self):
        return [
            Link(
                self.request.route_path(
                    "/admin/expenses/%s" % (self.get_type()),
                ),
                label=u"Retour",
                icon="fa fa-step-backward"
            )
        ]


class ExpenseKmTypeAddView(ExpenseTypeAddView):
    """
    View used to add Expense Km types
    Custom methods are added here to keep the year param in the url and in the
    form
    """
    factory = ExpenseKmType
    schema = get_expense_kmtype_schema()

    def before(self, form):
        form.set_appstruct({'year': _get_year_from_request(self.request)})

    def redirect(self, model):
        """
        Custom redirect to keep the 'year' param
        """
        return HTTPFound(
            self.request.route_path(self.redirect_route, year=model.year)
        )

    @property
    def menus(self):
        return [
            Link(
                label=u"Retour",
                url=self.request.route_path(
                    "/admin/expenses/expensekm",
                    year=_get_year_from_request(self.request)
                ),
                icon="fa fa-step-backward",
            )
        ]


class ExpenseTelTypeAddView(ExpenseTypeAddView):
    factory = ExpenseTelType
    schema = get_expense_teltype_schema()


class ExpenseTypeEditView(BaseEditView):
    add_template_vars = ('menus', 'help_msg')
    schema = get_expense_type_schema()
    factory = ExpenseType
    title = u"Modifier"

    @classmethod
    def get_type(cls):
        return cls.factory.__mapper_args__['polymorphic_identity']

    @property
    def redirect_route(self):
        return "/admin/expenses/%s" % self.get_type()

    @property
    def menus(self):
        return [
            Link(
                label=u"Retour",
                url=self.request.route_path(
                    "/admin/expenses/%s" % (self.get_type()),
                ),
                icon="fa fa-step-backward"
            )
        ]


class ExpenseKmTypeEditView(ExpenseTypeEditView):
    factory = ExpenseKmType
    schema = get_expense_kmtype_schema()

    def redirect(self):
        """
        Custom redirect to keep the 'year' param
        """
        return HTTPFound(
            self.request.route_path(self.redirect_route, year=self.context.year)
        )

    @property
    def menus(self):
        return [
            Link(
                label=u"Retour",
                icon="fa fa-step-backward",
                url=self.request.route_path(
                    "/admin/expenses/expensekm",
                    year=_get_year_from_request(self.request)
                ),
            )
        ]


class ExpenseTelTypeEditView(ExpenseTypeEditView):
    factory = ExpenseTelType
    schema = get_expense_teltype_schema()


class ExpenseKmTypesDuplicateView(BaseView):
    """
    Expense km list Duplication view

    Allows to duplicate :
        to next (default)

        from previous (if 'from_previous' is set in the GET params
    """
    def load_items(self, year):
        query = ExpenseKmType.query().filter_by(active=True)
        return query.filter_by(year=year)

    def __call__(self):
        if 'from_previous' in self.request.GET:
            new_year = _get_year_from_request(self.request)
            year = new_year - 1
            msg = u"Les données ont bien été réprises"
        else:
            year = _get_year_from_request(self.request)
            new_year = year + 1
            msg = (
                u"Vous avez été redirigé vers la grille des frais de "
                u"l'année %s" % (new_year,)
            )

        for item in self.load_items(year):
            new_item = item.duplicate(new_year)
            self.request.dbsession.merge(new_item)
        self.request.session.flash(msg)
        return HTTPFound(
            self.request.current_route_path(_query={}, year=new_year)
        )


def add_routes(config):
    """
    Add the routes related to the current module
    """
    for factory in ExpenseType, ExpenseTelType:
        type_label = factory.__mapper_args__['polymorphic_identity']
        path = "/admin/expenses/%s" % (type_label)
        config.add_route(path, path)
        path = "/admin/expenses/%s/{id}" % (type_label)
        config.add_route(
            path,
            path,
            traverse="/expense_types/{id}",
        )

    config.add_route(
        '/admin/expenses/expensekm/',
        "/admin/expenses/expensekm/"
    )

    config.add_route(
        '/admin/expenses/expensekm',
        "/admin/expenses/expensekm/{year}"
    )
    config.add_route(
        "/admin/expenses/expensekm/{id}",
        "/admin/expenses/expensekm/{year}/{id}",
        traverse="/expense_types/{id}",
    )


def includeme(config):
    add_routes(config)

    for list_class in (
        ExpenseTypeListView,
        ExpenseKmTypeListView,
        ExpenseTelTypeListView,
    ):
        config.add_view(
            list_class,
            route_name="/admin/expenses/%s" % list_class.get_type(),
            permission="admin",
            renderer='admin/crud_list.mako',
        )

    for add_class in (
        ExpenseTypeAddView,
        ExpenseKmTypeAddView,
        ExpenseTelTypeAddView,
    ):
        config.add_view(
            add_class,
            route_name="/admin/expenses/%s" % add_class.get_type(),
            permission="admin",
            request_param="action=new",
            renderer='admin/crud_add_edit.mako',
        )

    for disable_class in (
        ExpenseTypeDisableView,
        ExpenseKmTypeDisableView,
        ExpenseTelTypeDisableView,
    ):
        config.add_view(
            disable_class,
            route_name="/admin/expenses/%s/{id}" % disable_class.get_type(),
            request_param="action=disable",
            permission="admin",
        )

    for edit_class in (
        ExpenseTypeEditView,
        ExpenseKmTypeEditView,
        ExpenseTelTypeEditView,
    ):
        config.add_view(
            edit_class,
            route_name="/admin/expenses/%s/{id}" % edit_class.get_type(),
            permission="admin",
            renderer='admin/crud_add_edit.mako',
        )

    config.add_view(
        ExpenseKmTypesIndexView,
        route_name="/admin/expenses/expensekm/",
        permission="admin",
        renderer='admin/expense_km_index.mako',
    )

    config.add_view(
        ExpenseKmTypesDuplicateView,
        route_name="/admin/expenses/expensekm",
        request_param="action=duplicate",
        permission="admin",
    )
