# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
from sqlalchemy import asc
from pyramid.httpexceptions import HTTPFound

from autonomie.models.accounting.income_statement_measures import (
    IncomeStatementMeasureType,
    IncomeStatementMeasureTypeCategory,
)
from autonomie.forms.accounting import (
    get_admin_income_statement_measure_schema,
    get_admin_income_statement_category_schema
)
from autonomie.views import (
    BaseView,
    BaseEditView,
    BaseAddView,
    DisableView,
    DeleteView,
)

logger = logging.getLogger(__name__)

BASE_URL = u"/admin/accounting/income_statement_measures"

CATEGORY_CONFIG_URL = BASE_URL + "/categories"
CATEGORY_URL = CATEGORY_CONFIG_URL + "/{id}"

TYPE_URL = BASE_URL + "/types"
TYPE_CATEGORY_URL = TYPE_URL + "/{category_id}"
ITEM_URL = TYPE_CATEGORY_URL + "/{id}"


def index_view(request):
    menus = []
    for label, route, title, icon in (
        (u"Retour", "/admin/accounting", "", "fa fa-step-backward"),
        (
            u"Configuration des catégories d'indicateurs de Comptes de "
            u"résultat",
            CATEGORY_CONFIG_URL,
            u"Définition des catégories permettant de faciliter la "
            u"configuration des indicateurs de Comptes de résultat",
            "fa fa-braille",
        ),
        (
            u"Configuration des indicateurs de Comptes de résultat",
            TYPE_URL,
            u"Définition des codes comptables utilisés pour le calcul des "
            u"Comptes de résultat",
            "fa fa-braille",
        ),
    ):
        menus.append(
            dict(label=label, route_name=route, title=title, icon=icon)
        )
    return dict(
        title=u"Configuration de la génération des États de trésorerie",
        menus=menus
    )


def type_category_list_view(request):
    """
    List categories of Income Statement Measures we can edit
    """
    menus = []
    menus.append(
        {
            'label': u"Retour",
            "route_name": BASE_URL,
            "title": "",
            "icon": "fa fa-step-backward",
        }
    )

    for category in IncomeStatementMeasureTypeCategory.get_categories():
        label = u'Configuration des indicateurs de type %s' % category.label
        url = request.route_path(
            TYPE_CATEGORY_URL,
            category_id=category.id,
        )
        menus.append(dict(label=label, url=url, icon="fa fa-braille"))

    return dict(
        title=u"Configuration des indicateurs de Compte de résultat",
        help_message=u"""Les indicateurs de comptes de résultat permettent de
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
        résultat de vos entrepreneurs.""",
        menus=menus
    )


class CategoryListView(BaseView):
    columns = [u"Libellé de la catégorie", ]
    title = u"Configuration des catégories d'indicateurs de compte de résultat"
    factory = IncomeStatementMeasureTypeCategory

    def __init__(self, *args, **kwargs):
        BaseView.__init__(self, *args, **kwargs)
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

    def _get_item_url(self, category, action=None):
        """
        shortcut for route_path calls
        """
        query = dict(self.request.GET)
        if action is not None:
            query['action'] = action

        return self.request.route_path(
            CATEGORY_URL,
            id=category.id,
            _query=query,
        )

    def stream_actions(self, category):
        """
        Stream the actions available for the given category object
        :param obj catgegory: IncomeStatementMeasureTypeCategory instance
        :returns: List of 4-uples (url, label, title, icon,)
        """
        if category.active:
            yield (
                self._get_item_url(category),
                u"Voir/Modifier",
                u"Voir/Modifier",
                u"pencil",
            )
            move_url = self._get_item_url(category, action="move")
            if category.order > 0:
                yield (
                    move_url + "&direction=up",
                    u"Remonter",
                    u"Remonter dans l'ordre des catégories",
                    u"fa fa-arrow-circle-o-up"
                )
            if category.order < self.max_order:
                yield (
                    move_url + "&direction=down",
                    u"Redescendre",
                    u"Redescendre dans l'ordre des catégories",
                    u"fa fa-arrow-circle-o-down"
                )

            yield (
                self._get_item_url(category, action='disable'),
                u"Désactiver",
                u"Les informations associés aux indicateur de cette catégorie "
                u"ne seront plus affichées",
                u"remove",
            )
        else:
            yield (
                self._get_item_url(category, action='disable'),
                u"Activer",
                u"Les informations générés depuis les indicateurs de cette "
                u"catégorie seront affichées",
                u"fa fa-check-square-o",
            )
            yield(
                self._get_item_url(category, action='delete'),
                u"Supprimer",
                u"Supprimer cet indicateurs et les entrées associées",
                u"fa fa-trash",
                u"return window.confirm('Êtes-vous sûr de vouloir supprimer "
                u"cet élément ? Tous les éléments dans les comptes de résultat "
                u"ayant été générés depuis des indicateurs seront  également "
                u"supprimés.')",
            )

    def _load_items(self, year=None):
        """
        Return the sqlalchemy models representing current queried elements
        :rtype: SQLAlchemy.Query object
        """
        items = self.factory.query()
        items = items.order_by(asc(self.factory.order))
        return items

    def _more_template_vars(self, result):
        """
        Hook allowing to add datas to the templating context
        """
        result['help_msg'] = u"""Les catégories ci-dessous sont utilisées pour
        regrouper des éléments dans la configuration des comptes de résultats
        des entrepreneurs. Elles permettent la configuration de totaux."""
        return result

    def _get_menus(self):
        """
        Return the menu entries
        """
        return [
            dict(
                label=u"Retour",
                route_name=BASE_URL,
                icon="fa fa-step-backward"
            )
        ]

    @property
    def addurl(self):
        return self.request.route_path(
            CATEGORY_CONFIG_URL, _query={'action': "add"}
        )

    def __call__(self):
        menus = self._get_menus()

        items = self._load_items()

        result = dict(
            items=items,
            columns=self.columns,
            stream_columns=self.stream_columns,
            stream_actions=self.stream_actions,
            title=self.title,
            menus=menus,
            addurl=self.addurl,
        )
        self._more_template_vars(result)

        return result


class CategoryDisableView(DisableView):
    """
    View for measure disable/enable
    """
    def redirect(self):
        return HTTPFound(self._redirect_url())

    def _redirect_url(self):
        return self.request.route_path(CATEGORY_CONFIG_URL)

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


class CategoryDeleteView(DeleteView):
    """
    Category deletion view
    """

    def redirect(self):
        return HTTPFound(self._redirect_url())

    def _redirect_url(self):
        return self.request.route_path(CATEGORY_CONFIG_URL)

    def on_delete(self):
        """
        On disable we reset the order
        """
        IncomeStatementMeasureTypeCategory.reorder()


class CategoryAddView(BaseAddView):
    add_template_vars = ('menus', 'help_msg')
    factory = IncomeStatementMeasureTypeCategory
    title = u"Ajouter"
    schema = get_admin_income_statement_category_schema()

    def before(self, form):
        pre_filled = {
            'order': self.factory.get_next_order()
        }
        form.set_appstruct(pre_filled)

    def redirect(self, model=None):
        return HTTPFound(self._redirect_url())

    def _redirect_url(self):
        return self.request.route_path(CATEGORY_CONFIG_URL)

    @property
    def menus(self):
        return [
            dict(
                label=u"Retour",
                url=self._redirect_url(),
                icon="fa fa-step-backward"
            )
        ]


class CategoryEditView(BaseEditView):
    add_template_vars = ('menus', 'help_msg')
    factory = IncomeStatementMeasureTypeCategory
    schema = get_admin_income_statement_category_schema()

    @property
    def title(self):
        return u"Modifier la catégorie '{0}'".format(self.context.label)

    def redirect(self, model=None):
        return HTTPFound(self._redirect_url())

    def _redirect_url(self):
        return self.request.route_path(CATEGORY_CONFIG_URL)

    @property
    def menus(self):
        return [
            dict(
                label=u"Retour",
                url=self._redirect_url(),
                icon="fa fa-step-backward",
            )
        ]


class MeasureTypeListView(BaseView):
    columns = [
        u"Libellé de l'indicateur", u"Regroupe",
        u"Correspond à un total",
    ]
    title = u"Configuration des indicateurs de compte de résultat"
    factory = IncomeStatementMeasureType

    def __init__(self, *args, **kwargs):
        BaseView.__init__(self, *args, **kwargs)
        self.max_order = IncomeStatementMeasureType.get_next_order_by_category(
            self.context.id
        ) - 1

    def stream_columns(self, measure_type):
        """
        Stream a column object (called from within the template)

        :param obj measure_type: The object to display
        :returns: A generator of labels representing the different columns of
        our list
        :rtype: generator
        """
        yield measure_type.label
        if measure_type.compiled_total:
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
            ITEM_URL,
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
            yield (
                self._get_item_url(measure_type),
                u"Voir/Modifier",
                u"Voir/Modifier",
                u"pencil",
            )
            move_url = self._get_item_url(measure_type, action="move")
            if measure_type.order > 0:
                yield (
                    move_url + "&direction=up",
                    u"Remonter",
                    u"Remonter dans l'ordre des indicateurs",
                    u"fa fa-arrow-circle-o-up"
                )
            if measure_type.order < self.max_order:
                yield (
                    move_url + "&direction=down",
                    u"Redescendre",
                    u"Redescendre dans l'ordre des indicateurs",
                    u"fa fa-arrow-circle-o-down"
                )

            yield (
                self._get_item_url(measure_type, action='disable'),
                u"Désactiver",
                u"Les informations associés à cet indicateur ne seront "
                u"plus affichées",
                u"remove",
            )
        else:
            yield (
                self._get_item_url(measure_type, action='disable'),
                u"Activer",
                u"Les informations générés depuis cet indicateur seront "
                u"affichées",
                u"fa fa-check-square-o",
            )
            yield(
                self._get_item_url(measure_type, action='delete'),
                u"Supprimer",
                u"Supprimer cet indicateurs et les entrées associées",
                u"fa fa-trash",
                u"return window.confirm('Êtes-vous sûr de vouloir supprimer "
                u"cet élément ? Tous les éléments dans les comptes de résultat "
                u"ayant été générés depuis cet indicateur seront  également "
                u"supprimés.')",
            )

    def _load_items(self, year=None):
        """
        Return the sqlalchemy models representing current queried elements
        :rtype: SQLAlchemy.Query object
        """
        items = self.factory.query().filter_by(category_id=self.context.id)
        items = items.order_by(asc(self.factory.order))
        return items

    def _more_template_vars(self, result):
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

    def _get_menus(self):
        """
        Return the menu entries
        """
        return [
            dict(
                label=u"Retour",
                route_name=TYPE_URL,
                icon="fa fa-step-backward"
            )
        ]

    def _get_actions(self, items):
        """
        Return the description of additionnal main actions buttons

        :rtype: list
        """
        yield (
            self.addurl + "?is_total=1",
            u"Ajouter un total",
            u"Ajouter un indicateur de type total qui sera mis en évidence "
            u"dans l'interface",
            u"fa fa-plus-circle",
            u"btn btn-default secondary-action",
        )

    @property
    def addurl(self):
        return self.request.route_path(
            TYPE_CATEGORY_URL + '/add',
            category_id=self.context.id,
        )

    def __call__(self):
        menus = self._get_menus()

        items = self._load_items()

        result = dict(
            items=items,
            columns=self.columns,
            stream_columns=self.stream_columns,
            stream_actions=self.stream_actions,
            title=self.title,
            menus=menus,
            actions=self._get_actions(items),
            addurl=self.addurl,
        )
        self._more_template_vars(result)

        return result


class MeasureTypeAddView(BaseAddView):
    add_template_vars = ('menus', 'help_msg')
    factory = IncomeStatementMeasureType
    title = u"Ajouter"
    _schema = None

    def __init__(self, *args, **kwargs):
        BaseAddView.__init__(self, *args, **kwargs)

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

    def redirect(self, model=None):
        return HTTPFound(self._redirect_url())

    def _redirect_url(self):
        return self.request.route_path(
            TYPE_CATEGORY_URL,
            category_id=self.context.id,
        )

    def merge_appstruct(self, appstruct, model):
        """
        Handle specific form keys when setting the new model's datas

        Regarding the type of total we manage (category total or operation
        specific total), we want to set some attributes
        """
        model = BaseAddView.merge_appstruct(self, appstruct, model)
        if 'total_type' in appstruct:
            total_type = appstruct['total_type']
            model.account_prefix = appstruct[total_type]

        return model

    @property
    def menus(self):
        return [
            dict(
                label=u"Retour",
                url=self._redirect_url(),
                icon="fa fa-step-backward"
            )
        ]


class MeasureTypeEditView(BaseEditView):
    add_template_vars = ('menus', 'help_msg')
    _schema = None
    factory = IncomeStatementMeasureType

    def __init__(self, *args, **kwargs):
        BaseEditView.__init__(self, *args, **kwargs)

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

    @property
    def title(self):
        return u"Modifier la définition de l'indicateur '{0}'".format(
            self.context.label
        )

    def redirect(self):
        return HTTPFound(self._redirect_url())

    def _redirect_url(self):
        return self.request.route_path(
            TYPE_CATEGORY_URL,
            category_id=self.context.category.id,
        )

    def get_default_appstruct(self):
        result = BaseEditView.get_default_appstruct(self)
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
        model = BaseEditView.merge_appstruct(self, appstruct, model)
        if 'total_type' in appstruct:
            total_type = appstruct['total_type']
            model.account_prefix = appstruct[total_type]

        return model

    @property
    def menus(self):
        return [
            dict(
                label=u"Retour",
                url=self._redirect_url(),
                icon="fa fa-step-backward",
            )
        ]


class MeasureDisableView(CategoryDisableView):

    def on_enable(self):
        """
        on enable we set order to 1
        """
        order = IncomeStatementMeasureType.get_next_order_by_category(
            self.context.category_id
        )
        self.context.order = order
        self.request.dbsession.merge(self.context)

    def _redirect_url(self):
        return self.request.route_path(
            TYPE_CATEGORY_URL,
            category_id=self.context.category_id,
        )


class MeasureDeleteView(CategoryDeleteView):
    """
    View for measure disable/enable
    """
    def _redirect_url(self):
        return self.request.route_path(
            TYPE_CATEGORY_URL,
            category_id=self.context.category.id,
        )

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
    config.add_route(CATEGORY_CONFIG_URL, CATEGORY_CONFIG_URL)
    config.add_route(
        CATEGORY_URL,
        CATEGORY_URL,
        traverse="/income_statement_measure_categories/{id}"
    )

    config.add_route(TYPE_URL, TYPE_URL)
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
        ITEM_URL,
        ITEM_URL,
        traverse="income_statement_measure_types/{id}",
    )


def add_views(config):
    """
    Add views defined in this module
    """
    config.add_admin_view(
        index_view, route_name=BASE_URL, renderer="admin/index.mako"
    )
    config.add_admin_view(
        CategoryListView,
        route_name=CATEGORY_CONFIG_URL,
        renderer="admin/crud_list.mako",
    )
    config.add_admin_view(
        CategoryAddView,
        route_name=CATEGORY_CONFIG_URL,
        renderer="admin/crud_add_edit.mako",
        request_param="action=add",
    )
    config.add_admin_view(
        CategoryEditView,
        route_name=CATEGORY_URL,
        renderer="admin/crud_add_edit.mako",
    )
    config.add_admin_view(
        CategoryDisableView,
        route_name=CATEGORY_URL,
        request_param="action=disable",
    )
    config.add_admin_view(
        CategoryDeleteView,
        route_name=CATEGORY_URL,
        request_param="action=delete",
    )
    config.add_admin_view(
        move_view,
        route_name=CATEGORY_URL,
        request_param='action=move',
    )

    config.add_admin_view(
        type_category_list_view,
        route_name=TYPE_URL,
        renderer="admin/index.mako",
    )
    config.add_admin_view(
        MeasureTypeListView,
        route_name=TYPE_CATEGORY_URL,
        renderer="admin/crud_list.mako",
    )
    config.add_admin_view(
        MeasureTypeAddView,
        route_name=TYPE_CATEGORY_URL + "/add",
        renderer="admin/crud_add_edit.mako",
    )
    config.add_admin_view(
        MeasureTypeEditView,
        route_name=ITEM_URL,
        renderer="admin/crud_add_edit.mako",
    )
    config.add_admin_view(
        MeasureDisableView,
        route_name=ITEM_URL,
        request_param="action=disable",
    )
    config.add_admin_view(
        MeasureDeleteView,
        route_name=ITEM_URL,
        request_param="action=delete",
    )
    config.add_admin_view(
        move_view,
        route_name=ITEM_URL,
        request_param='action=move',
    )


def includeme(config):
    add_routes(config)
    add_views(config)
