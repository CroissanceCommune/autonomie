# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os

from sqlalchemy import desc
from sqlalchemy.orm import load_only

from autonomie.models.files import FileType

from autonomie.utils.widgets import Link
from autonomie.forms.admin.main.files import (
    get_admin_file_type_schema
)
from autonomie.views.admin.tools import (
    AdminCrudListView,
    BaseAdminAddView,
    BaseAdminEditView,
    BaseAdminDisableView,
    BaseAdminDeleteView,
)
from autonomie.views.admin.main import (
    MAIN_ROUTE,
    MainIndexView,
)

FILE_TYPE_ROUTE = os.path.join(MAIN_ROUTE, "file_types")
FILE_TYPE_ITEM_ROUTE = os.path.join(FILE_TYPE_ROUTE, "{id}")


class FileTypeListView(AdminCrudListView):
    title = u"Type de fichiers déposables dans Autonomie"
    description = u"Configurer les types de fichier proposés lors du dépôt de \
fichier dans Autonomie"

    route_name = FILE_TYPE_ROUTE
    item_route_name = FILE_TYPE_ITEM_ROUTE
    columns = [
        u"Libellé",
    ]
    factory = FileType

    @property
    def help_msg(self):
        from autonomie.views.admin.sale.business_cycle.file_types import (
            BUSINESS_FILETYPE_URL,
        )
        return u"""
    Configurez les types de fichier proposés dans les formulaires de dépôt de
    fichier (notes de dépenses, rendez-vous, projets, affaires, devis, factures
    ...).<br />
    Ces types sont également utilisés pour requérir des fichiers (par exemple
    les feuilles d'émargement pour les formations).<br />
    Pour cela, vous devez indiquer quel types de fichier sont requis par type
    d'affaires.<br /> <a class='link'
    href='{0}'>Configuration générale -> Module Ventes -> Cycle d'affaires ->
    Configuration des fichiers obligatoires/facultatives</a>
    """.format(self.request.route_path(BUSINESS_FILETYPE_URL))

    def stream_columns(self, item):
        yield item.label

    def stream_actions(self, item):
        yield Link(
            self._get_item_url(item),
            u"Voir/Modifier",
            icon=u"pencil",
        )
        if item.active:
            yield Link(
                self._get_item_url(item, action='disable'),
                u"Désactiver",
                title=u"Ce type de document ne sera plus proposé dans les "
                u"formulaires",
                icon=u"remove",
            )
        else:
            yield Link(
                self._get_item_url(item, action='disable'),
                u"Activer",
                icon=u"check-square-o",
            )
        if not item.is_used:
            yield Link(
                self._get_item_url(item, action='delete'),
                u"Supprimer",
                icon=u"trash",
            )

    def load_items(self):
        """
        Return the sqlalchemy models representing current queried elements
        :rtype: SQLAlchemy.Query object
        """
        items = self.request.dbsession.query(FileType).options(
            load_only('label',)
        )
        items = items.order_by(desc(self.factory.active))
        return items

    def more_template_vars(self, result):
        result['help_msg'] = self.help_msg
        return result


class FileTypeAddView(BaseAdminAddView):
    title = u"Ajouter"
    route_name = FILE_TYPE_ROUTE
    factory = FileType
    schema = get_admin_file_type_schema()


class FileTypeEditView(BaseAdminEditView):
    route_name = FILE_TYPE_ITEM_ROUTE
    factory = FileType
    schema = get_admin_file_type_schema()

    help_msg = FileTypeListView.help_msg

    @property
    def title(self):
        return u"Modifier le type de fichier '{0}'".format(self.context.label)


class FileTypeDisableView(BaseAdminDisableView):
    """
    View for FileType disable/enable
    """
    route_name = FILE_TYPE_ITEM_ROUTE


class FileTypeDeleteView(BaseAdminDeleteView):
    """
    View for FileType deletion
    """
    route_name = FILE_TYPE_ITEM_ROUTE


def includeme(config):
    config.add_route(
        FILE_TYPE_ROUTE,
        FILE_TYPE_ROUTE
    )
    config.add_route(
        FILE_TYPE_ITEM_ROUTE,
        FILE_TYPE_ITEM_ROUTE,
        traverse="/file_types/{id}"
    )
    config.add_admin_view(
        FileTypeListView,
        parent=MainIndexView,
        renderer="admin/crud_list.mako",
    )
    config.add_admin_view(
        FileTypeAddView,
        parent=FileTypeListView,
        renderer="admin/crud_add_edit.mako",
        request_param="action=add",
    )
    config.add_admin_view(
        FileTypeEditView,
        parent=FileTypeListView,
        renderer="admin/crud_add_edit.mako",
    )
    config.add_admin_view(
        FileTypeDisableView,
        parent=FileTypeListView,
        request_param="action=disable",
    )
    config.add_admin_view(
        FileTypeDeleteView,
        parent=FileTypeListView,
        request_param="action=delete",
    )
