# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from sqlalchemy import desc

from autonomie.models.expense import (
    ExpenseType,
    ExpenseKmType,
    ExpenseTelType,
)

from autonomie.views import (
    BaseView,
    DisableView,
    BaseAddView,
    BaseEditView,
)
from autonomie.views import render_api
from autonomie.forms.admin import get_admin_schema
TEMPLATES_URL = 'autonomie:deform_templates/'


class ExpenseTypeListView(BaseView):
    columns = [
        u"Libellé", u"Compte de charge"
    ]
    title = u"Configuration des types de dépenses"
    factory = ExpenseType

    def stream_columns(self, expense_type):
        """
        Stream the table datas for the given item
        :param obj expense_type: The ExpenseType object to stream
        :returns: List of labels
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
        query = None
        if action is not None:
            query = {'action': action}

        return self.request.route_path(
            "/admin/expenses/%s/" % self.get_type(),
            id=expense_type.id,
            _query=query
        )

    def stream_actions(self, expense_type):
        """
        Stream the actions available for the given expense_type object
        :param obj expense_type: ExpenseType instance
        :returns: List of 4-uples (url, label, title, icon,)
        """
        yield (
            self._get_item_url(expense_type),
            u"Voir/Modifier",
            u"Voir/Modifier",
            u"pencil",
        )
        if expense_type.active:
            yield (
                self._get_item_url(expense_type, action='disable'),
                u"Désactiver",
                u"La TVA n'apparaitra plus dans l'interface",
                u"remove",
            )
        else:
            yield (
                self._get_item_url(expense_type, action='disable'),
                u"Activer",
                u"La TVA apparaitra plus dans l'interface",
                u"",
            )

    def __call__(self):
        menus = [dict(label=u"Retour", path="admin_expense",
                      icon="fa fa-step-backward")]

        items = self.factory.query().filter(
            self.factory.type == self.get_type()
        ).order_by(desc(self.factory.active)).all()

        return dict(
            items=items,
            columns=self.columns,
            stream_columns=self.stream_columns,
            stream_actions=self.stream_actions,
            title=self.title,
            menus=menus,
            addurl=self.request.route_path(
                '/admin/expenses/%s' % self.get_type(),
                _query=dict(action="new")
            ),
        )


class ExpenseKmTypeListView(ExpenseTypeListView):
    columns = [
        u"Libellé",
        u"Compte de charge",
        u"Indemnité kilométrique"
    ]

    title = u"Configuration des types de dépenses kilométriques"
    factory = ExpenseKmType

    def stream_columns(self, expense_type):
        yield expense_type.label or u"Non renseigné"
        yield expense_type.code or "Aucun"
        yield u"%s €/km" % (
            expense_type.amount or 0
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


class ExpenseTelTypeDisableView(ExpenseTypeDisableView):
    factory = ExpenseTelType


class ExpenseTypeAddView(BaseAddView):
    add_template_vars = ('menus', 'help_msg')
    factory = ExpenseType
    schema = get_admin_schema(ExpenseType)
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
            dict(
                label=u"Retour",
                path="/admin/expenses/%s" % (self.get_type()),
                icon="fa fa-step-backward"
            )
        ]


class ExpenseKmTypeAddView(ExpenseTypeAddView):
    factory = ExpenseKmType
    schema = get_admin_schema(ExpenseKmType)


class ExpenseTelTypeAddView(ExpenseTypeAddView):
    factory = ExpenseTelType
    schema = get_admin_schema(ExpenseTelType)


class ExpenseTypeEditView(BaseEditView):
    add_template_vars = ('menus', 'help_msg')
    schema = get_admin_schema(ExpenseType)
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
            dict(
                label=u"Retour",
                path="/admin/expenses/%s" % (self.get_type()),
                icon="fa fa-step-backward"
            )
        ]


class ExpenseKmTypeEditView(ExpenseTypeEditView):
    factory = ExpenseKmType
    schema = get_admin_schema(ExpenseKmType)


class ExpenseTelTypeEditView(ExpenseTypeEditView):
    factory = ExpenseTelType
    schema = get_admin_schema(ExpenseTelType)


def add_routes(config):
    """
    Add the routes related to the current module
    """
    for factory in ExpenseType, ExpenseKmType, ExpenseTelType:
        type_label = factory.__mapper_args__['polymorphic_identity']
        path = "/admin/expenses/%s" % (type_label)
        config.add_route(path, path)
        path = "/admin/expenses/%s/" % (type_label)
        config.add_route(
            path,
            '%s{id}' % path,
            traverse="/expense_types_%ss/{id}" % type_label,
        )


def includeme(config):
    add_routes(config)

    for list_class in (
        ExpenseTypeListView,
        ExpenseKmTypeListView,
        ExpenseTelTypeListView,
    ):
        print(list_class.get_type())
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
            route_name="/admin/expenses/%s/" % disable_class.get_type(),
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
            route_name="/admin/expenses/%s/" % edit_class.get_type(),
            permission="admin",
            renderer='admin/crud_add_edit.mako',
        )
