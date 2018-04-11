# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import os
from sqlalchemy import desc
from autonomie.models import files
from autonomie.forms.files import get_template_upload_schema
from autonomie.utils.widgets import Link
from autonomie.utils.strings import format_date
from autonomie.views.files import (
    FileUploadView,
    FileEditView,
    file_dl_view,
)
from autonomie.views.admin.tools import (
    AdminTreeMixin,
    AdminCrudListView,
    BaseAdminDisableView,
    BaseAdminDeleteView,
)
from autonomie.views.admin.userdatas import (
    USERDATAS_URL,
    UserDatasIndexView,
)


log = logging.getLogger(__name__)


UPLOAD_OK_MSG = u"Le modèle de document a bien été ajouté"
EDIT_OK_MSG = u"Le modèle de document a bien été modifié"


TEMPLATE_URL = os.path.join(USERDATAS_URL, 'templates')
TEMPLATE_ITEM_URL = os.path.join(TEMPLATE_URL, '{id}')


class TemplateListView(AdminCrudListView):
    """
    Listview of templates
    """
    title = u"Configuration des modèles de documents"
    route_name = TEMPLATE_URL
    item_route_name = TEMPLATE_ITEM_URL
    columns = (u'Nom du fichier', u'Description', u"Déposé le")

    def stream_actions(self, item):
        yield Link(
            self._get_item_url(item),
            u"Télécharger",
            title=u"Télécharger le fichier odt",
            icon=u"download"
        )
        yield Link(
            self._get_item_url(item, action='edit'),
            u"Modifier",
            title=u"Modifier le modèle",
            icon=u"pencil"
        )
        if item.active:
            yield Link(
                self._get_item_url(item, action='disable'),
                u"Désactiver",
                title=u"Désactiver le modèle afin qu'il ne soit plus proposé",
                icon=u"remove"
            )
        else:
            yield Link(
                self._get_item_url(item, action='disable'),
                u"Activer",
                title=u"Activer le modèle afin qu'il soit proposé dans "
                u"l'interface",
                icon=u"check"
            )
            yield Link(
                self._get_item_url(item, action='delete'),
                u"Supprimer",
                title=u"Supprimer définitivement le modèle",
                confirm=u"Êtes-vous sûr de vouloir supprimer ce modèle ?",
                icon=u"trash",
                css="label-warning",
            )

    def stream_columns(self, item):
        yield item.name
        yield item.description
        yield format_date(item.updated_at)

    def more_template_vars(self, result):
        result['warn_msg'] = u"Les modèles de document doivent être au format "
        u"odt pour pouvoir être utilisés par Autonomie"
        return result

    def load_items(self):
        templates = files.Template.query()\
            .order_by(desc(files.Template.active))
        return templates


class TemplateAddView(FileUploadView, AdminTreeMixin):
    title = u"Ajouter un modèle de documents"
    route_name = TEMPLATE_URL
    factory = files.Template
    schema = get_template_upload_schema()
    valid_msg = UPLOAD_OK_MSG
    add_template_vars = ('title', 'breadcrumb', 'back_link')

    def before(self, form):
        come_from = self.request.referrer
        log.debug(u"Coming from : %s" % come_from)

        appstruct = {
            'come_from': come_from
        }
        form.set_appstruct(appstruct)


class TemplateEditView(FileEditView, AdminTreeMixin):
    route_name = TEMPLATE_ITEM_URL
    valid_msg = u"Le modèle de document a bien été modifié"
    factory = files.Template
    schema = get_template_upload_schema()
    valid_msg = EDIT_OK_MSG
    add_template_vars = ('title', 'breadcrumb', 'back_link')

    def before(self, form):
        FileEditView.before(self, form)


class TemplateDisableView(BaseAdminDisableView):
    route_name = TEMPLATE_ITEM_URL
    enable_msg = u"Le template a bien été activé"
    disable_msg = u"Le template a bien été désactivé"


class TemplateDeleteView(BaseAdminDeleteView):
    route_name = TEMPLATE_ITEM_URL
    delete_msg = u"Le modèle a bien été supprimé"


def includeme(config):
    config.add_route(TEMPLATE_URL, TEMPLATE_URL)
    config.add_route(
        TEMPLATE_ITEM_URL,
        TEMPLATE_ITEM_URL,
        traverse="templates/{id}"
    )

    config.add_admin_view(
        TemplateListView,
        parent=UserDatasIndexView,
        renderer="autonomie:templates/admin/crud_list.mako"
    )
    config.add_admin_view(
        TemplateAddView,
        parent=TemplateListView,
        request_param="action=add",
    )
    config.add_admin_view(
        file_dl_view,
        route_name=TEMPLATE_ITEM_URL,
    )
    config.add_admin_view(
        TemplateEditView,
        parent=TemplateListView,
        request_param='action=edit',
    )
    config.add_admin_view(
        TemplateDisableView,
        parent=TemplateListView,
        request_param='action=disable',
    )
    config.add_admin_view(
        TemplateDeleteView,
        parent=TemplateListView,
        request_param='action=delete',
    )
