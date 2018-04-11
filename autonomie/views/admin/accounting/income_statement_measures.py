# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os
import logging
from sqlalchemy import asc
from pyramid.httpexceptions import HTTPFound

from autonomie.models.accounting.income_statement_measures import (
    IncomeStatementMeasureType,
    IncomeStatementMeasureTypeCategory,
)
from autonomie.utils.widgets import Link
from autonomie.forms.accounting import (
    get_admin_income_statement_measure_schema,
    get_admin_income_statement_category_schema
)
from autonomie.views.admin.accounting import (
    AccountingIndexView,
    ACCOUNTING_URL,
)
from autonomie.views import (
    BaseView,
)
from autonomie.views.admin.tools import (
    AdminCrudListView,
    BaseAdminIndexView,
    AdminTreeMixin,
    BaseAdminEditView,
    BaseAdminAddView,
    BaseAdminDisableView,
    BaseAdminDeleteView,
)

logger = logging.getLogger(__name__)

BASE_URL = os.path.join(ACCOUNTING_URL, "income_statement_measures")

CATEGORY_URL = BASE_URL + "/categories"
CATEGORY_TYPE_ITEM_URL = CATEGORY_URL + "/{id}"

TYPE_INDEX_URL = BASE_URL + "/types"
TYPE_CATEGORY_URL = TYPE_INDEX_URL + "/{category_id}"
TYPE_ITEM_URL = TYPE_CATEGORY_URL + "/{id}"


class IncomeStatementMeasureIndexView(BaseAdminIndexView):
    title = u"Comptes de résultat"
    route_name = BASE_URL


class CategoryListView(AdminCrudListView):
    columns = [u"Libellé de la catégorie", ]
    title = u"Catégories d'indicateurs de compte de résultat"
    route_name = CATEGORY_URL
    item_route_name = CATEGORY_TYPE_ITEM_URL
    factory = IncomeStatementMeasureTypeCategory

    def __init__(self, *args, **kwargs):
        AdminCrudListView.__init__(self, *args, **kwargs)
        self.max_order = IncomeStatementMeasureTypeCategory.get_next_order() - 1

    def stream_columns(self, measure_type):
        """
        Stream a column object (called from within the template)

        :param obj measure_type: The object to display
        :returns: A generator of labels representing the different columns of
        our list
        :rtype: generator
        """
        yield measure_type.label

    def stream_actions(self, category):
        """
        Stream the actions available for the given category object
        :param obj catgegory: IncomeStatementMeasureTypeCategory instance
        :returns: List of 4-uples (url, label, title, icon,)
        """
        if category.active:
            yield Link(
                self._get_item_url(category),
                u"Voir/Modifier",
                icon=u"pencil",
            )
            move_url = self._get_item_url(category, action="move")
            if category.order > 0:
                yield Link(
                    move_url + "&direction=up",
                    u"Remonter",
                    title=u"Remonter dans l'ordre des catégories",
                    icon=u"arrow-circle-o-up"
                )
            if category.order < self.max_order:
                yield Link(
                    move_url + "&direction=down",
                    u"Redescendre",
                    title=u"Redescendre dans l'ordre des catégories",
                    icon=u"arrow-circle-o-down"
                )

            yield Link(
                self._get_item_url(category, action='disable'),
                u"Désactiver",
                title=u"Les informations associés aux indicateur de cette "
                u"catégorie ne seront plus affichées",
                icon=u"remove",
            )
        else:
            yield Link(
                self._get_item_url(category, action='disable'),
                u"Activer",
                title=u"Les informations générés depuis les indicateurs de "
                u"cette catégorie seront affichées",
                icon=u"check-square-o",
            )
            yield Link(
                self._get_item_url(category, action='delete'),
                u"Supprimer",
                title=u"Supprimer cet indicateurs et les entrées associées",
                icon=u"trash",
                confirm=u"Êtes-vous sûr de vouloir supprimer "
                u"cet élément ? Tous les éléments dans les comptes de résultat "
                u"ayant été générés depuis des indicateurs seront  également "
                u"supprimés.",
            )

    def load_items(self):
        """
        Return the sqlalchemy models representing current queried elements
        :rtype: SQLAlchemy.Query object
        """
        items = self.factory.query()
        items = items.order_by(asc(self.factory.order))
        return items

    def more_template_vars(self, result):
        """
        Hook allowing to add datas to the templating context
        """
        result['help_msg'] = u"""Les catégories ci-dessous sont utilisées pour
        regrouper des éléments dans la configuration des comptes de résultats
        des entrepreneurs. Elles permettent la configuration de totaux."""
        return result


class CategoryAddView(BaseAdminAddView):
    title = u"Ajouter"
    route_name = CATEGORY_URL

    factory = IncomeStatementMeasureTypeCategory
    schema = get_admin_income_statement_category_schema()

    def before(self, form):
        pre_filled = {
            'order': self.factory.get_next_order()
        }
        form.set_appstruct(pre_filled)


class CategoryEditView(BaseAdminEditView):
    factory = IncomeStatementMeasureTypeCategory
    route_name = CATEGORY_TYPE_ITEM_URL
    schema = get_admin_income_statement_category_schema()

    @property
    def title(self):
        return u"Modifier la catégorie '{0}'".format(self.context.label)


class CategoryDisableView(BaseAdminDisableView):
    """
    View for measure disable/enable
    """
    route_name = CATEGORY_TYPE_ITEM_URL

    def on_disable(self):
        """
        On disable we set order to -1
        """
        self.context.order = -1
        self.request.dbsession.merge(self.context)

    def on_enable(self):
        """
        on enable we set order to 1
        """
        order = IncomeStatementMeasureTypeCategory.get_next_order()
        self.context.order = order
        self.request.dbsession.merge(self.context)


class CategoryDeleteView(BaseAdminDeleteView):
    """
    Category deletion view
    """
    route_name = CATEGORY_TYPE_ITEM_URL

    def on_delete(self):
        """
        On disable we reset the order
        """
        IncomeStatementMeasureTypeCategory.reorder()


class TypeListIndexView(BaseView, AdminTreeMixin):
    title = u"Indicateurs de Compte de résultat"
    route_name = TYPE_INDEX_URL
    help_message = u"""Les indicateurs de comptes de résultat permettent de
    regrouper les écritures comptables derrière un même libellé afin de les
    regrouper au sein d'un tableau annuel présentant le compte de résultat
    de chaque entreprise.<br />
    Les indicateurs sont divisés en 4 catégories (dans l'ordre de
    présentation )<br />
    <ul>
    <li>Produits</li>
    <li>Achats</li>
    <li>Charges</li>
    <li>Salaires et Cotisations</li>
    </ul>
    Depuis cette interface, vous pouvez configurer, par
    catégorie, l'ensemble des indicateurs qui composeront les comptes de
    résultat de vos entrepreneurs."""

    def __call__(self):
        navigation = []
        for category in IncomeStatementMeasureTypeCategory.get_categories():
            label = u'Indicateurs de type %s' % category.label
            url = self.request.route_path(
                TYPE_CATEGORY_URL,
                category_id=category.id,
            )
            navigation.append(dict(label=label, url=url, icon="fa fa-braille"))

        return dict(
            title=self.title,
            help_message=self.help_message,
            navigation=navigation,
            breadcrumb=self.breadcrumb,
            back_link=self.back_link
        )


def _get_category_id_from_request(request):
    """
    Extract the category id from the given request

    :param obj request: The pyramid request object
    :returns: A category id
    :rtype: int
    """
    if isinstance(request.context, IncomeStatementMeasureTypeCategory):
        return request.context.id
    else:
        return request.context.category_id


class MeasureTypeListView(AdminCrudListView):
    columns = [
        u"Libellé de l'indicateur", u"Regroupe",
        u"Correspond à un total",
    ]
    title = u"Indicateurs de compte de résultat"
    factory = IncomeStatementMeasureType
    route_name = TYPE_CATEGORY_URL

    def __init__(self, *args, **kwargs):
        AdminCrudListView.__init__(self, *args, **kwargs)
        self.max_order = IncomeStatementMeasureType.get_next_order_by_category(
            self.context.id
        ) - 1

    @property
    def url(self):
        return self.request.route_path(
            TYPE_CATEGORY_URL,
            category_id=_get_category_id_from_request(self.request)
        )

    def stream_columns(self, measure_type):
        """
        Stream a column object (called from within the template)

        :param obj measure_type: The object to display
        :returns: A generator of labels representing the different columns of
        our list
        :rtype: generator
        """
        yield measure_type.label
        if measure_type.computed_total:
            if measure_type.total_type == 'categories':
                yield u"La somme des indicateurs des catégories %s" % (
                    measure_type.account_prefix,
                )
            elif measure_type.total_type == 'complex_total':
                yield u"Le résultat de l'opération : '%s'" % (
                    measure_type.account_prefix,
                )
        else:
            yield u"Les comptes : %s" % measure_type.account_prefix
        if measure_type.is_total:
            yield "<div class='text-center'><i class='fa fa-check'></i></div>"
        else:
            yield "<div class='text-center'><i class='fa fa-close'></i></div>"

    def _get_item_url(self, measure_type, action=None):
        """
        shortcut for route_path calls
        """
        query = dict(self.request.GET)
        if action is not None:
            query['action'] = action

        return self.request.route_path(
            TYPE_ITEM_URL,
            id=measure_type.id,
            category_id=measure_type.category_id,
            _query=query,
        )

    def stream_actions(self, measure_type):
        """
        Stream the actions available for the given measure_type object
        :param obj measure_type: TreasuryMeasureType instance
        :returns: List of 4-uples (url, label, title, icon,)
        """
        if measure_type.active:
            yield Link(
                self._get_item_url(measure_type),
                u"Voir/Modifier",
                icon=u"pencil",
            )
            move_url = self._get_item_url(measure_type, action="move")
            if measure_type.order > 0:
                yield Link(
                    move_url + "&direction=up",
                    u"Remonter",
                    title=u"Remonter dans l'ordre des indicateurs",
                    icon=u"arrow-circle-o-up"
                )
            if measure_type.order < self.max_order:
                yield Link(
                    move_url + "&direction=down",
                    u"Redescendre",
                    title=u"Redescendre dans l'ordre des indicateurs",
                    icon=u"arrow-circle-o-down"
                )

            yield Link(
                self._get_item_url(measure_type, action='disable'),
                u"Désactiver",
                title=u"Les informations associés à cet indicateur ne seront "
                u"plus affichées",
                icon=u"remove",
            )
        else:
            yield Link(
                self._get_item_url(measure_type, action='disable'),
                u"Activer",
                title=u"Les informations générés depuis cet indicateur seront "
                u"affichées",
                icon=u"check-square-o",
            )
            yield Link(
                self._get_item_url(measure_type, action='delete'),
                u"Supprimer",
                title=u"Supprimer cet indicateurs et les entrées associées",
                icon=u"trash",
                confirm=u"Êtes-vous sûr de vouloir supprimer "
                u"cet élément ? Tous les éléments dans les comptes de résultat "
                u"ayant été générés depuis cet indicateur seront  également "
                u"supprimés.",
            )

    def load_items(self, year=None):
        """
        Return the sqlalchemy models representing current queried elements
        :rtype: SQLAlchemy.Query object
        """
        items = self.factory.query().filter_by(category_id=self.context.id)
        items = items.order_by(asc(self.factory.order))
        return items

    def more_template_vars(self, result):
        """
        Hook allowing to add datas to the templating context
        """
        result['help_msg'] = u"""Les définitions ci-dessous indiquent quelles
        écritures sont utilisées pour le calcul des indicateurs de la section
        %s des comptes de résultat des entrepreneurs.<br />
        Les indicateurs seront présentés dans l'ordre.<br />
        Certains indicateurs sont des totaux, ils seront alors mis en évidence
        dans l'interface""" % (
            self.context.label,
        )
        return result

    def get_actions(self, items):
        """
        Return the description of additionnal main actions buttons

        :rtype: list
        """
        yield Link(
            self.get_addurl() + "?is_total=1",
            u"Ajouter un total",
            title=u"Ajouter un indicateur de type total qui sera mis en "
            u"évidence dans l'interface",
            icon=u"plus-circle",
            css=u"btn btn-default secondary-action",
        )

    def get_addurl(self):
        return self.request.route_path(
            TYPE_CATEGORY_URL + '/add',
            category_id=self.context.id,
        )


class MeasureTypeAddView(BaseAdminAddView):
    title = u"Ajouter"
    route_name = TYPE_CATEGORY_URL + "/add"
    _schema = None
    factory = IncomeStatementMeasureType

    def is_total_form(self):
        return "is_total" in self.request.GET

    @property
    def schema(self):
        if self._schema is None:
            if self.is_total_form():
                self._schema = get_admin_income_statement_measure_schema(
                    total=True
                )
            else:
                self._schema = get_admin_income_statement_measure_schema()
        return self._schema

    @schema.setter
    def schema(self, value):
        self._schema = value

    def before(self, form):
        """
        Launched before the form is used

        :param obj form: The form object
        """
        pre_filled = {
            'category_id': self.context.id,
            'order': self.factory.get_next_order_by_category(self.context.id),
        }

        if 'is_total' in self.request.GET:
            pre_filled['is_total'] = True
            pre_filled['label'] = u"Total %s" % (self.context.label, )
            pre_filled['categories'] = "%s" % self.context.label
            pre_filled['total_type'] = u"categories"

        form.set_appstruct(pre_filled)

    def merge_appstruct(self, appstruct, model):
        """
        Handle specific form keys when setting the new model's datas

        Regarding the type of total we manage (category total or operation
        specific total), we want to set some attributes
        """
        model = BaseAdminAddView.merge_appstruct(self, appstruct, model)
        if 'total_type' in appstruct:
            total_type = appstruct['total_type']
            model.account_prefix = appstruct[total_type]

        return model


class MeasureTypeEditView(BaseAdminEditView):
    route_name = TYPE_ITEM_URL
    _schema = None
    factory = IncomeStatementMeasureType

    @property
    def title(self):
        return u"Modifier la définition de l'indicateur '{0}'".format(
            self.context.label
        )

    def is_total_form(self):
        return self.context.is_total

    @property
    def schema(self):
        if self._schema is None:
            if self.is_total_form():
                self._schema = get_admin_income_statement_measure_schema(
                    total=True
                )
            else:
                self._schema = get_admin_income_statement_measure_schema()
        return self._schema

    @schema.setter
    def schema(self, value):
        self._schema = value

    def get_default_appstruct(self):
        result = BaseAdminEditView.get_default_appstruct(self)
        if self.is_total_form():
            result['total_type'] = self.context.total_type
            result['account_prefix'] = ''
            result[self.context.total_type] = self.context.account_prefix
        return result

    def merge_appstruct(self, appstruct, model):
        """
        Handle specific form keys when setting the new model's datas

        Regarding the type of total we manage (category total or operation
        specific total), we want to set some attributes
        """
        model = BaseAdminEditView.merge_appstruct(self, appstruct, model)
        if 'total_type' in appstruct:
            total_type = appstruct['total_type']
            model.account_prefix = appstruct[total_type]

        return model


class MeasureDisableView(CategoryDisableView):
    route_name = TYPE_ITEM_URL

    def on_enable(self):
        """
        on enable we set order to 1
        """
        order = IncomeStatementMeasureType.get_next_order_by_category(
            self.context.category_id
        )
        self.context.order = order
        self.request.dbsession.merge(self.context)


class MeasureDeleteView(CategoryDeleteView):
    """
    View for measure disable/enable
    """
    route_name = TYPE_ITEM_URL

    def on_delete(self):
        """
        On disable we reset the order
        """
        IncomeStatementMeasureType.reorder(self.context.category_id)


def move_view(context, request):
    """
    Reorder the current context moving it up in the category's hierarchy

    :param obj context: The given IncomeStatementMeasureType instance
    """
    action = request.params['direction']
    if action == 'up':
        context.move_up()
    else:
        context.move_down()
    return HTTPFound(request.referer)


def add_routes(config):
    """
    Add routes related to this module
    """
    config.add_route(BASE_URL, BASE_URL)
    config.add_route(CATEGORY_URL, CATEGORY_URL)
    config.add_route(
        CATEGORY_TYPE_ITEM_URL,
        CATEGORY_TYPE_ITEM_URL,
        traverse="/income_statement_measure_categories/{id}"
    )

    config.add_route(TYPE_INDEX_URL, TYPE_INDEX_URL)
    config.add_route(
        TYPE_CATEGORY_URL,
        TYPE_CATEGORY_URL,
        traverse="/income_statement_measure_categories/{category_id}",
    )
    config.add_route(
        TYPE_CATEGORY_URL + "/add", TYPE_CATEGORY_URL + "/add",
        traverse="/income_statement_measure_categories/{category_id}",
    )
    config.add_route(
        TYPE_ITEM_URL,
        TYPE_ITEM_URL,
        traverse="income_statement_measure_types/{id}",
    )


def add_views(config):
    """
    Add views defined in this module
    """
    config.add_admin_view(
        IncomeStatementMeasureIndexView, parent=AccountingIndexView,
    )
    config.add_admin_view(
        CategoryListView,
        parent=IncomeStatementMeasureIndexView,
        renderer="admin/crud_list.mako",
    )
    config.add_admin_view(
        CategoryAddView,
        parent=CategoryListView,
        renderer="admin/crud_add_edit.mako",
        request_param="action=add",
    )
    config.add_admin_view(
        CategoryEditView,
        parent=CategoryListView,
        renderer="admin/crud_add_edit.mako",
    )
    config.add_admin_view(
        CategoryDisableView,
        parent=CategoryListView,
        request_param="action=disable",
    )
    config.add_admin_view(
        CategoryDeleteView,
        parent=CategoryListView,
        request_param="action=delete",
    )
    config.add_admin_view(
        move_view,
        route_name=CATEGORY_TYPE_ITEM_URL,
        request_param='action=move',
    )
    config.add_admin_view(
        TypeListIndexView,
        parent=IncomeStatementMeasureIndexView,
    )
    config.add_admin_view(
        MeasureTypeListView,
        parent=TypeListIndexView,
        renderer="admin/crud_list.mako",
    )
    config.add_admin_view(
        MeasureTypeAddView,
        parent=MeasureTypeListView,
        renderer="admin/crud_add_edit.mako",
    )
    config.add_admin_view(
        MeasureTypeEditView,
        parent=MeasureTypeListView,
        renderer="admin/crud_add_edit.mako",
    )
    config.add_admin_view(
        MeasureDisableView,
        parent=MeasureTypeListView,
        request_param="action=disable",
    )
    config.add_admin_view(
        MeasureDeleteView,
        parent=MeasureTypeListView,
        request_param="action=delete",
    )
    config.add_admin_view(
        move_view,
        route_name=TYPE_ITEM_URL,
        request_param='action=move',
    )


def includeme(config):
    add_routes(config)
    add_views(config)
