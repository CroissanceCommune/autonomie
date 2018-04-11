# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os
from autonomie.models.project.types import ProjectType

from autonomie.utils.widgets import Link
from autonomie.forms.admin.project import get_admin_project_type_schema
from autonomie.views.admin.tools import (
    AdminCrudListView,
    BaseAdminDisableView,
    BaseAdminDeleteView,
    BaseAdminEditView,
    BaseAdminAddView,
)

from autonomie.views.admin.sale.business_cycle import (
    BusinessCycleIndexView,
    BUSINESS_URL
)

BASE_URL = os.path.join(BUSINESS_URL, "project_types")
ITEM_URL = os.path.join(BASE_URL, "{id}")


class ProjectTypeListView(AdminCrudListView):
    title = u"Types de projets"
    description = u"Configurer les types de projets proposés aux entrepreneurs \
ceux-ci servent de base pour la configuration des cycles d'affaire."
    route_name = BASE_URL
    item_route_name = ITEM_URL
    columns = [
        u'Libellé',
        u"Nom interne",
        u"Nécessite des droits particuliers",
        u"Type de projet par défaut ?",
    ]
    factory = ProjectType

    def stream_columns(self, type_):
        yield type_.label
        yield type_.name
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

        if not type_.is_used():
            yield Link(
                self._get_item_url(type_, action='delete'),
                u"Supprimer",
                title=u"Supprimer ce type de projet",
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
        items = ProjectType.query()
        items = items.order_by(self.factory.default).order_by(self.factory.name)
        return items


class ProjectTypeDisableView(BaseAdminDisableView):
    """
    View for ProjectType disable/enable
    """
    pass


class ProjectTypeDeleteView(BaseAdminDeleteView):
    """
    ProjectType deletion view
    """
    pass


class ProjectTypeAddView(BaseAdminAddView):
    title = u"Ajouter"
    route_name = BASE_URL
    factory = ProjectType
    schema = get_admin_project_type_schema()


class ProjectTypeEditView(BaseAdminEditView):
    route_name = ITEM_URL
    factory = ProjectType
    schema = get_admin_project_type_schema()

    @property
    def title(self):
        return u"Modifier le type de projet '{0}'".format(self.context.label)


def includeme(config):
    config.add_route(BASE_URL, BASE_URL)
    config.add_route(ITEM_URL, ITEM_URL, traverse="/project_types/{id}")

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
