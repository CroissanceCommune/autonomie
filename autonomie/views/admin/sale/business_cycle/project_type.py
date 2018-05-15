# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os
from pyramid.httpexceptions import HTTPFound

from autonomie.models.project.types import (
    ProjectType,
    SubProjectType,
)

from autonomie.utils.widgets import Link
from autonomie.forms.admin.project import (
    get_admin_project_type_schema,
    get_admin_subproject_type_schema,
)
from autonomie.views import BaseView
from autonomie.views.admin.tools import (
    AdminCrudListView,
    BaseAdminDisableView,
    BaseAdminDeleteView,
    BaseAdminEditView,
    BaseAdminAddView,
    AdminTreeMixin,
)

from autonomie.views.admin.sale.business_cycle import (
    BusinessCycleIndexView,
    BUSINESS_URL
)

PROJECT_TYPE_URL = os.path.join(BUSINESS_URL, "project_types")
PROJECT_TYPE_ITEM_URL = os.path.join(PROJECT_TYPE_URL, "{id}")
SUBPROJECT_TYPE_URL = os.path.join(BUSINESS_URL, "subproject_types")
SUBPROJECT_TYPE_ITEM_URL = os.path.join(SUBPROJECT_TYPE_URL, "{id}")


class ProjectTypeListView(AdminCrudListView):
    title = u"Types de projet"
    description = u"Configurer les types de projet proposés aux entrepreneurs \
ceux-ci servent de base pour la configuration des cycles d'affaire."
    route_name = PROJECT_TYPE_URL
    item_route_name = PROJECT_TYPE_ITEM_URL
    columns = [
        u'Libellé',
        u"Nécessite des droits particuliers",
        u"Type de projet par défaut ?",
    ]
    factory = ProjectType

    def stream_columns(self, type_):
        yield type_.label
        if type_.private:
            yield u"<i class='glyphicon glyphicon-ok-sign'></i>"
        else:
            yield u""
        if type_.default:
            yield u"<i class='glyphicon glyphicon-ok-sign'></i>&nbsp;"
            u"Type par défaut"
        else:
            yield u""

    def stream_actions(self, type_):
        if type_.editable:
            yield Link(
                self._get_item_url(type_),
                u"Voir/Modifier",
                icon=u"pencil",
            )
        if type_.active:
            yield Link(
                self._get_item_url(type_, action='disable'),
                u"Désactiver",
                title=u"Ce type de projet ne sera plus proposé aux "
                u"utilisateurs",
                icon=u"remove",
            )
        else:
            yield Link(
                self._get_item_url(type_, action='disable'),
                u"Activer",
                title=u"Ce type de projet sera proposé aux utilisateurs",
                icon=u"check-square-o",
            )

        if not type_.default:
            yield Link(
                self._get_item_url(type_, action='set_default'),
                label=u"Définir comme type par défaut",
                title=u"Le type sera sélectionné par défaut à la création "
                u"d'un projet",
            )

        if not type_.is_used():
            yield Link(
                self._get_item_url(type_, action='delete'),
                u"Supprimer",
                title=u"Supprimer ce type de projet",
                icon=u"trash",
                confirm=u"Êtes-vous sûr de vouloir supprimer cet élément ?"
            )

    def load_items(self):
        """
        Return the sqlalchemy models representing current queried elements
        :rtype: SQLAlchemy.Query object
        """
        items = ProjectType.query()
        items = items.order_by(self.factory.default).order_by(self.factory.name)
        return items


class ProjectTypeDisableView(BaseAdminDisableView):
    """
    View for ProjectType disable/enable
    """
    route_name = PROJECT_TYPE_ITEM_URL


class ProjectTypeDeleteView(BaseAdminDeleteView):
    """
    ProjectType deletion view
    """
    route_name = PROJECT_TYPE_ITEM_URL


class ProjectTypeAddView(BaseAdminAddView):
    title = u"Ajouter"
    route_name = PROJECT_TYPE_URL
    factory = ProjectType
    schema = get_admin_project_type_schema()


class ProjectTypeEditView(BaseAdminEditView):
    route_name = PROJECT_TYPE_ITEM_URL
    factory = ProjectType
    schema = get_admin_project_type_schema()

    @property
    def title(self):
        return u"Modifier le type de projet '{0}'".format(self.context.label)


class ProjectTypeSetDefaultView(BaseView, AdminTreeMixin):
    """
    Set the given tva as default
    """
    route_name = PROJECT_TYPE_ITEM_URL

    def __call__(self):
        for item in ProjectType.query():
            item.default = False
            self.request.dbsession.merge(item)
        self.context.default = True
        self.request.dbsession.merge(item)
        return HTTPFound(self.back_link)


class SubProjectTypeListView(AdminCrudListView):
    title = u"Types d'affaire"
    description = u"""Configurer les types d'affaires proposés aux
    entrepreneurs. Les types d'affaire permettent de spécifier des règles
    (documents requis ...) spécifiques.
    """
    factory = SubProjectType
    route_name = SUBPROJECT_TYPE_URL
    item_route_name = SUBPROJECT_TYPE_ITEM_URL
    columns = [
        u'Libellé',
        u"Nécessite des droits particuliers",
        u"Par défaut pour les projets de type",
        u"Sélectionnable pour les projets de type",
    ]

    def stream_columns(self, type_):
        yield type_.label
        if type_.private:
            yield u"<i class='glyphicon glyphicon-ok-sign'></i>"
        else:
            yield u""
        if type_.project_type:
            yield type_.project_type.label
        else:
            yield u""

        yield u",".join([t.label for t in type_.other_project_types])

    def stream_actions(self, type_):
        if type_.editable:
            yield Link(
                self._get_item_url(type_),
                u"Voir/Modifier",
                icon=u"pencil",
            )
        if type_.active:
            yield Link(
                self._get_item_url(type_, action='disable'),
                u"Désactiver",
                title=u"Ce type de sous-projet ne sera plus proposé aux "
                u"utilisateurs",
                icon=u"remove",
            )
        else:
            yield Link(
                self._get_item_url(type_, action='disable'),
                u"Activer",
                title=u"Ce type de sous-projet sera proposé aux utilisateurs",
                icon=u"check-square-o",
            )

        if not type_.is_used():
            yield Link(
                self._get_item_url(type_, action='delete'),
                u"Supprimer",
                title=u"Supprimer ce type de sous-projet",
                icon=u"trash",
                confirm=u"Êtes-vous sûr de vouloir supprimer cet élément ?"
            )

    def load_items(self):
        items = SubProjectType.query()
        items = items.order_by(self.factory.name)
        return items


class SubProjectTypeDisableView(BaseAdminDisableView):
    """
    View for SubProjectType disable/enable
    """
    route_name = SUBPROJECT_TYPE_ITEM_URL


class SubProjectTypeDeleteView(BaseAdminDeleteView):
    """
    SubProjectType deletion view
    """
    route_name = SUBPROJECT_TYPE_ITEM_URL


class SubProjectTypeAddView(BaseAdminAddView):
    title = u"Ajouter"
    route_name = SUBPROJECT_TYPE_URL
    factory = SubProjectType
    schema = get_admin_subproject_type_schema()


class SubProjectTypeEditView(BaseAdminEditView):
    route_name = SUBPROJECT_TYPE_ITEM_URL
    factory = SubProjectType
    schema = get_admin_subproject_type_schema()

    @property
    def title(self):
        return u"Modifier le type de sous-projet '{0}'".format(
            self.context.label
        )


def includeme(config):
    config.add_route(
        PROJECT_TYPE_URL,
        PROJECT_TYPE_URL
    )
    config.add_route(
        PROJECT_TYPE_ITEM_URL,
        PROJECT_TYPE_ITEM_URL,
        traverse="/project_types/{id}"
    )
    config.add_route(
        SUBPROJECT_TYPE_URL,
        SUBPROJECT_TYPE_URL
    )
    config.add_route(
        SUBPROJECT_TYPE_ITEM_URL,
        SUBPROJECT_TYPE_ITEM_URL,
        traverse="/sub_project_types/{id}"
    )

    config.add_admin_view(
        ProjectTypeListView,
        parent=BusinessCycleIndexView,
        renderer="admin/crud_list.mako",
    )

    config.add_admin_view(
        ProjectTypeAddView,
        parent=ProjectTypeListView,
        renderer="admin/crud_add_edit.mako",
        request_param="action=add",
    )
    config.add_admin_view(
        ProjectTypeEditView,
        parent=ProjectTypeListView,
        renderer="admin/crud_add_edit.mako",
    )
    config.add_admin_view(
        ProjectTypeDisableView,
        parent=ProjectTypeListView,
        request_param="action=disable",
    )
    config.add_admin_view(
        ProjectTypeDeleteView,
        parent=ProjectTypeListView,
        request_param="action=delete",
    )
    config.add_admin_view(
        ProjectTypeSetDefaultView,
        parent=ProjectTypeListView,
        request_param="action=set_default",
    )

    config.add_admin_view(
        SubProjectTypeListView,
        parent=BusinessCycleIndexView,
        renderer="admin/crud_list.mako",
    )

    config.add_admin_view(
        SubProjectTypeAddView,
        parent=SubProjectTypeListView,
        renderer="admin/crud_add_edit.mako",
        request_param="action=add",
    )
    config.add_admin_view(
        SubProjectTypeEditView,
        parent=SubProjectTypeListView,
        renderer="admin/crud_add_edit.mako",
    )
    config.add_admin_view(
        SubProjectTypeDisableView,
        parent=SubProjectTypeListView,
        request_param="action=disable",
    )
    config.add_admin_view(
        SubProjectTypeDeleteView,
        parent=SubProjectTypeListView,
        request_param="action=delete",
    )
