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
    CATEGORIES,
)
from autonomie.forms.accounting import (
    get_admin_income_statement_measure_schema,
)
from autonomie.views import (
    BaseView,
    BaseEditView,
    BaseAddView,
    DisableView,
    DeleteView,
)

logger = logging.getLogger(__name__)


def category_list_view(request):
    """
    List categories of Income Statement Measures we can edit

    Categories are hardcoded in the associated models module
    """
    menus = []
    menus.append(
        {
            'label': u"Retour",
            "route_name": "/admin/accounting",
            "title": "",
            "icon": "fa fa-step-backward",
        }
    )

    for category in CATEGORIES:
        label = u'Configuration des indicateurs de type %s' % category
        url = request.route_path(
            "/admin/accounting/income_statement_measure_types/{category}",
            category=category,
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


class MeasureTypeListView(BaseView):
    columns = [
        u"Libellé de l'indicateur", u"Regroupe",
        u"Correspond à un total",
    ]
    title = u"Configuration des indicateurs de compte de résultat"
    factory = IncomeStatementMeasureType

    def __init__(self, *args, **kwargs):
        BaseView.__init__(self, *args, **kwargs)
        self.category = self.request.matchdict['category']
        self.max_order = IncomeStatementMeasureType.get_next_order_by_category(
            self.category
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
        if measure_type.is_total:
            yield u"La somme des indicateurs des catégories %s" % (
                measure_type.categories
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
            "/admin/accounting/income_statement_measure_types/{category}/{id}",
            id=measure_type.id,
            category=measure_type.category,
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
        items = self.factory.query().filter_by(category=self.category)
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
            self.category,
        )
        return result

    def _get_menus(self):
        """
        Return the menu entries
        """
        return [
            dict(
                label=u"Retour",
                route_name="/admin/accounting/income_statement_measure_types",
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
            '/admin/accounting/income_statement_measure_types/'
            '{category}/add',
            category=self.category,
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
        self.category = self.request.matchdict['category']

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
            'category': self.category,
            'order': self.factory.get_next_order_by_category(self.category),
        }

        if 'is_total' in self.request.GET:
            pre_filled['is_total'] = True
            pre_filled['label'] = u"Total %s" % (self.category, )
            pre_filled['categories'] = self.category
            pre_filled['total_type'] = u"categories"

        form.set_appstruct(pre_filled)

    def redirect(self, model=None):
        return HTTPFound(self._redirect_url())

    def _redirect_url(self):
        return self.request.route_path(
            "/admin/accounting/income_statement_measure_types/{category}",
            category=self.category,
        )

    def merge_appstruct(self, appstruct, model):
        """
        Handle specific form keys when setting the new model's datas

        Regarding the type of total we manage (category total or operation
        specific total), we want to set some attributes
        """
        model = BaseAddView.merge_appstruct(self, appstruct, model)
        if 'total_type' in appstruct:
            if appstruct['total_type'] == 'categories':
                model.account_prefix = ''
            else:
                model.categories = ''
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
        self.category = self.request.matchdict['category']

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
            "/admin/accounting/income_statement_measure_types/{category}",
            category=self.category,
        )

    def get_default_appstruct(self):
        result = BaseEditView.get_default_appstruct(self)
        if self.is_total_form():
            if self.context.account_prefix:
                result['total_type'] = 'account_prefix'
            else:
                result['total_type'] = 'categories'
        return result

    def merge_appstruct(self, appstruct, model):
        """
        Handle specific form keys when setting the new model's datas

        Regarding the type of total we manage (category total or operation
        specific total), we want to set some attributes
        """
        model = BaseEditView.merge_appstruct(self, appstruct, model)
        if 'total_type' in appstruct:
            if appstruct['total_type'] == 'categories':
                model.account_prefix = ''
            else:
                model.categories = ''
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


class MeasureDisableView(DisableView):
    """
    View for measure disable/enable
    """
    def redirect(self):
        return HTTPFound(self._redirect_url())

    def _redirect_url(self):
        return self.request.route_path(
            "/admin/accounting/income_statement_measure_types/{category}",
            category=self.context.category,
        )

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
        order = IncomeStatementMeasureType.get_next_order_by_category(
            self.context.category
        )
        self.context.order = order
        self.request.dbsession.merge(self.context)


class MeasureDeleteView(DeleteView):
    """
    View for measure disable/enable
    """
    def __init__(self, *args, **kwargs):
        DeleteView.__init__(self, *args, **kwargs)
        self.category = self.context.category

    def redirect(self):
        return HTTPFound(self._redirect_url())

    def _redirect_url(self):
        return self.request.route_path(
            "/admin/accounting/income_statement_measure_types/{category}",
            category=self.context.category,
        )

    def on_delete(self):
        """
        On disable we set order to -1
        """
        IncomeStatementMeasureType.reorder(self.category)


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
    config.add_route(
        "/admin/accounting/income_statement_measure_types",
        "/admin/accounting/income_statement_measure_types",
    )
    config.add_route(
        "/admin/accounting/income_statement_measure_types/{category}",
        "/admin/accounting/income_statement_measure_types/{category}",
    )
    config.add_route(
        "/admin/accounting/income_statement_measure_types/{category}/add",
        "/admin/accounting/income_statement_measure_types/{category}/add",
    )
    config.add_route(
        "/admin/accounting/income_statement_measure_types/{category}/{id}",
        "/admin/accounting/income_statement_measure_types/{category}/{id}",
        traverse="income_statement_measure_types/{id}",
    )


def add_views(config):
    """
    Add views defined in this module
    """
    config.add_admin_view(
        category_list_view,
        route_name="/admin/accounting/income_statement_measure_types",
        renderer="admin/index.mako",
    )
    config.add_admin_view(
        MeasureTypeListView,
        route_name="/admin/accounting/income_statement_measure_types/"
        "{category}",
        renderer="admin/crud_list.mako",
    )
    config.add_admin_view(
        MeasureTypeAddView,
        route_name="/admin/accounting/income_statement_measure_types/"
        "{category}/add",
        renderer="admin/crud_add_edit.mako",
    )
    config.add_admin_view(
        MeasureTypeEditView,
        route_name="/admin/accounting/income_statement_measure_types/"
        "{category}/{id}",
        renderer="admin/crud_add_edit.mako",
    )
    config.add_admin_view(
        MeasureDisableView,
        route_name="/admin/accounting/income_statement_measure_types/"
        "{category}/{id}",
        request_param="action=disable",
    )
    config.add_admin_view(
        MeasureDeleteView,
        route_name="/admin/accounting/income_statement_measure_types/"
        "{category}/{id}",
        request_param="action=delete",
    )
    config.add_admin_view(
        move_view,
        route_name="/admin/accounting/income_statement_measure_types/"
        "{category}/{id}",
        request_param='action=move',
    )


def includeme(config):
    add_routes(config)
    add_views(config)
