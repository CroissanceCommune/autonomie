# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os
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
)
from autonomie.forms.admin.expense_type import (
    get_expense_type_schema,
    get_expense_kmtype_schema,
    get_expense_teltype_schema,
)
from autonomie.views.admin.expense import (
    ExpenseIndexView,
    EXPENSE_URL,
)
from autonomie.views.admin.tools import (
    AdminCrudListView,
    BaseAdminDisableView,
    BaseAdminAddView,
    BaseAdminEditView,
    AdminTreeMixin
)


EXPENSE_BASETYPE_URL = os.path.join(EXPENSE_URL, "expense")
EXPENSE_BASETYPE_ITEM_URL = os.path.join(EXPENSE_BASETYPE_URL, "{id}")
EXPENSE_TEL_URL = os.path.join(EXPENSE_URL, "expensetel")
EXPENSE_TEL_ITEM_URL = os.path.join(EXPENSE_TEL_URL, "{id}")
EXPENSE_KM_INDEX_URL = os.path.join(EXPENSE_URL, "expensekm")
EXPENSE_KM_URL = os.path.join(EXPENSE_KM_INDEX_URL, "{year}")
EXPENSE_KM_ITEM_URL = os.path.join(EXPENSE_KM_URL, "{id}")


def _get_year_from_request(request):
    """
    Retrieve the current year from the request
    Usefull for ExpenseKmType edition

    :param obj request: The Pyramid request object
    :returns: A year
    :rtype: int
    """
    return convert_to_int(request.matchdict['year'], datetime.date.today().year)


class ExpenseKmTypesIndexView(BaseView, AdminTreeMixin):
    """
    Entry point to the km expense types configuration
    """
    title = u"Types de dépenses kilométriques"
    description = u"Configurer les types de dépenses kilométriques par année"
    route_name = EXPENSE_KM_INDEX_URL

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
            title=self.title,
            breadcrumb=self.breadcrumb,
            back_link=self.back_link,
            years=self._get_year_options(),
            admin_path=EXPENSE_KM_URL,
        )


class ExpenseTypeListView(AdminCrudListView):
    title = u"Types de dépenses"
    route_name = EXPENSE_BASETYPE_URL
    columns = [
        u"Libellé", u"Compte de charge"
    ]
    factory = ExpenseType
    item_route = EXPENSE_BASETYPE_ITEM_URL

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
            self.item_route,
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
        query['action'] = 'add'

        return self.request.current_route_path(
            _query=query,
            **self.request.matchdict
        )


class ExpenseKmTypeListView(ExpenseTypeListView):
    columns = [
        u"Libellé",
        u"Compte de charge",
        u"Indemnité kilométrique"
    ]
    route_name = EXPENSE_KM_URL

    factory = ExpenseKmType
    item_route = EXPENSE_KM_ITEM_URL

    @property
    def title(self):
        title = (
            u"Configuration des types de dépenses kilométriques pour "
            u"l'année {0}".format(_get_year_from_request(self.request))
        )
        return title

    @property
    def tree_url(self):
        return self.request.route_path(
            EXPENSE_KM_URL,
            year=_get_year_from_request(self.request)
        )

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
        if len(items) > 0 and year != current_year + 1:
            if self.load_items(year + 1).count() > 0:
                confirm = (
                    u"Tous les types de frais présentés ici seront "
                    u"copiés vers l'année {}. Des frais sont déjà configurés "
                    u"sur cette année."
                    u" Voulez-vous continuer ?".format(year + 1)
                )
            else:
                confirm = None
            yield Link(
                self._get_duplicate_url(),
                label=u"Dupliquer cette grille vers l'année suivante "
                u"(%s)" % (year + 1),
                icon=u"fa fa-copy",
                css=u"btn btn-default",
                confirm=confirm,
            )

        # If previous year there were some datas configured
        if self.load_items(year - 1).count() > 0:
            yield Link(
                self._get_duplicate_from_previous_url(),
                label=u"Recopier la grille de l'année précédente "
                u"(%s)" % (year - 1),
                icon=u"fa fa-copy",
                css=u"btn btn-default",
                confirm=u"Tous les types de frais de l'année précédente seront "
                u"recopiés ici. Voulez-vous continuer ?"
            )


class ExpenseTelTypeListView(ExpenseTypeListView):
    title = u"Types de dépenses téléphoniques"
    description = u"Configurer des types spécifiques donnant lieu à un \
remboursement en pourcentage de la dépense déclarée"
    route_name = EXPENSE_TEL_URL
    columns = [
        u"Libellé",
        u"Compte de charge",
        u"Pourcentage indemnisé"
    ]

    factory = ExpenseTelType
    item_route = EXPENSE_TEL_ITEM_URL

    def stream_columns(self, expense_type):
        yield expense_type.label or u"Non renseigné"
        yield expense_type.code or "Aucun"
        yield u"%s %%" % (
            expense_type.percentage or 0
        )


class ExpenseTypeDisableView(BaseAdminDisableView):
    disable_msg = u"L'élément a bien été désactivé"
    enable_msg = u"L'élément a bien été activé"
    factory = ExpenseType
    route_name = EXPENSE_BASETYPE_ITEM_URL

    @classmethod
    def get_type(cls):
        return cls.factory.__mapper_args__['polymorphic_identity']


class ExpenseKmTypeDisableView(ExpenseTypeDisableView):
    factory = ExpenseKmType
    route_name = EXPENSE_KM_ITEM_URL


class ExpenseTelTypeDisableView(ExpenseTypeDisableView):
    factory = ExpenseTelType
    route_name = EXPENSE_TEL_ITEM_URL


class ExpenseTypeAddView(BaseAdminAddView):
    title = u"Ajouter"
    factory = ExpenseType
    schema = get_expense_type_schema()
    route_name = EXPENSE_BASETYPE_URL

    @classmethod
    def get_type(cls):
        return cls.factory.__mapper_args__['polymorphic_identity']


class ExpenseKmTypeAddView(ExpenseTypeAddView):
    """
    View used to add Expense Km types
    Custom methods are added here to keep the year param in the url and in the
    form
    """
    factory = ExpenseKmType
    schema = get_expense_kmtype_schema()
    route_name = EXPENSE_KM_URL

    def before(self, form):
        form.set_appstruct({'year': _get_year_from_request(self.request)})


class ExpenseTelTypeAddView(ExpenseTypeAddView):
    factory = ExpenseTelType
    schema = get_expense_teltype_schema()
    route_name = EXPENSE_TEL_URL


class ExpenseTypeEditView(BaseAdminEditView):
    title = u"Modifier"
    schema = get_expense_type_schema()
    factory = ExpenseType
    route_name = EXPENSE_BASETYPE_ITEM_URL

    @classmethod
    def get_type(cls):
        return cls.factory.__mapper_args__['polymorphic_identity']


class ExpenseKmTypeEditView(ExpenseTypeEditView):
    factory = ExpenseKmType
    schema = get_expense_kmtype_schema()
    route_name = EXPENSE_KM_ITEM_URL


class ExpenseTelTypeEditView(ExpenseTypeEditView):
    factory = ExpenseTelType
    schema = get_expense_teltype_schema()
    route_name = EXPENSE_TEL_ITEM_URL


class ExpenseKmTypesDuplicateView(BaseView, AdminTreeMixin):
    """
    Expense km list Duplication view

    Allows to duplicate :
        to next (default)

        from previous (if 'from_previous' is set in the GET params
    """
    route_name = EXPENSE_KM_URL

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
    config.add_route(EXPENSE_BASETYPE_URL, EXPENSE_BASETYPE_URL)
    config.add_route(
        EXPENSE_BASETYPE_ITEM_URL,
        EXPENSE_BASETYPE_ITEM_URL,
        traverse="/expense_types/{id}",
    )
    config.add_route(EXPENSE_TEL_URL, EXPENSE_TEL_URL)
    config.add_route(
        EXPENSE_TEL_ITEM_URL,
        EXPENSE_TEL_ITEM_URL,
        traverse="/expense_types/{id}",
    )

    config.add_route(EXPENSE_KM_INDEX_URL, EXPENSE_KM_INDEX_URL)
    config.add_route(EXPENSE_KM_URL, EXPENSE_KM_URL)
    config.add_route(
        EXPENSE_KM_ITEM_URL,
        EXPENSE_KM_ITEM_URL,
        traverse="/expense_types/{id}",
    )


def includeme(config):
    add_routes(config)
    # BASE TYPES
    config.add_admin_view(
        ExpenseTypeListView,
        parent=ExpenseIndexView,
        renderer='admin/crud_list.mako',
    )
    config.add_admin_view(
        ExpenseTypeAddView,
        parent=ExpenseTypeListView,
        request_param="action=add",
        renderer='admin/crud_add_edit.mako',
    )
    config.add_admin_view(
        ExpenseTypeEditView,
        parent=ExpenseTypeListView,
        renderer='admin/crud_add_edit.mako',
    )
    config.add_admin_view(
        ExpenseTypeDisableView,
        parent=ExpenseTypeListView,
        request_param="action=disable",
    )

    # TEL TYPES
    config.add_admin_view(
        ExpenseTelTypeListView,
        parent=ExpenseIndexView,
        renderer='admin/crud_list.mako',
    )
    config.add_admin_view(
        ExpenseTelTypeAddView,
        parent=ExpenseTelTypeListView,
        request_param="action=add",
        renderer='admin/crud_add_edit.mako',
    )
    config.add_admin_view(
        ExpenseTelTypeEditView,
        parent=ExpenseTelTypeListView,
        renderer='admin/crud_add_edit.mako',
    )
    config.add_admin_view(
        ExpenseTelTypeDisableView,
        parent=ExpenseTelTypeListView,
        request_param="action=disable",
    )
    # KMTYPES
    config.add_admin_view(
        ExpenseKmTypesIndexView,
        parent=ExpenseIndexView,
        renderer='admin/expense_km_index.mako',
    )

    config.add_admin_view(
        ExpenseKmTypesDuplicateView,
        request_param="action=duplicate",
        permission="admin",
    )
    config.add_admin_view(
        ExpenseKmTypeListView,
        parent=ExpenseKmTypesIndexView,
        renderer='admin/crud_list.mako',
    )
    config.add_admin_view(
        ExpenseKmTypeAddView,
        parent=ExpenseKmTypeListView,
        request_param="action=add",
        renderer='admin/crud_add_edit.mako',
    )
    config.add_admin_view(
        ExpenseKmTypeEditView,
        parent=ExpenseKmTypeListView,
        renderer='admin/crud_add_edit.mako',
    )
    config.add_admin_view(
        ExpenseKmTypeDisableView,
        parent=ExpenseKmTypeListView,
        request_param="action=disable",
    )
