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
from autonomie.views import (
    DisableView,
    DeleteView,
)
from autonomie.views.files import (
    FileUploadView,
    FileEditView,
    file_dl_view,
)
from autonomie.views.admin.tools import (
    AdminTreeMixin,
    AdminCrudListView,
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


class TemplateUploadView(FileUploadView, AdminTreeMixin):
    title = u"Ajouter un modèle de documents"

    factory = files.Template
    schema = get_template_upload_schema()
    valid_msg = UPLOAD_OK_MSG
    add_template_vars = ('title', 'navigation', 'breadcrumb', 'back_link')

    def before(self, form):
        come_from = self.request.referrer
        log.debug(u"Coming from : %s" % come_from)

        appstruct = {
            'come_from': come_from
        }
        form.set_appstruct(appstruct)


class TemplateEditView(FileEditView, AdminTreeMixin):
    valid_msg = u"Le modèle de document a bien été modifié"
    factory = files.Template
    schema = get_template_upload_schema()
    valid_msg = EDIT_OK_MSG
    add_template_vars = ('title', 'navigation', 'breadcrumb', 'back_link')

    def before(self, form):
        FileEditView.before(self, form)


class TemplateListView(AdminCrudListView):
    """
    Listview of templates
    """
    title = u"Configuration des modèles de documents"
    route_name = TEMPLATE_URL
    columns = (u'Nom du fichier', u'Description', u"Déposé le")

    def stream_actions(self, item):
        yield Link(
            self.request.route_path(TEMPLATE_ITEM_URL, id=item.id),
            u"Télécharger",
            title=u"Télécharger le fichier odt",
            icon=u"download"
        )
        yield Link(
            self.request.route_path(
                TEMPLATE_ITEM_URL, id=item.id, _query={'action': "edit"}
            ),
            u"Modifier",
            title=u"Modifier le modèle",
            icon=u"pencil"
        )
        if item.active:
            yield Link(
                self.request.route_path(
                    TEMPLATE_ITEM_URL, id=item.id, _query={'action': "disable"}
                ),
                u"Désactiver",
                title=u"Désactiver le modèle afin qu'il ne soit plus proposé",
                icon=u"remove"
            )
        else:
            yield Link(
                self.request.route_path(
                    TEMPLATE_ITEM_URL, id=item.id, _query={'action': "disable"}
                ),
                u"Activer",
                title=u"Activer le modèle afin qu'il soit proposé dans "
                u"l'interface",
                icon=u"check"
            )
            yield Link(
                self.request.route_path(
                    TEMPLATE_ITEM_URL, id=item.id, _query={'action': "delete"}
                ),
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

    def get_addurl(self):
        return self.request.route_path(TEMPLATE_URL, _query={'action': 'add'})

    def more_template_vars(self, result):
        result['warn_msg'] = u"Les modèles de document doivent être au format "
        u"odt pour pouvoir être utilisés par Autonomie"
        return result

    def load_items(self):
        templates = files.Template.query()\
            .order_by(desc(files.Template.active))
        return templates


class TemplateDisableView(DisableView):
    enable_msg = u"Le template a bien été activé"
    disable_msg = u"Le template a bien été désactivé"
    redirect_route = TEMPLATE_URL


class TemplateDeleteView(DeleteView):
    delete_msg = u"Le modèle a bien été supprimé"
    redirect_route = TEMPLATE_URL


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
        TemplateUploadView,
        route_name=TEMPLATE_URL,
        parent=TemplateListView,
        request_param="action=add",
    )
    config.add_admin_view(
        file_dl_view,
        route_name=TEMPLATE_ITEM_URL,
    )
    config.add_admin_view(
        TemplateEditView,
        route_name=TEMPLATE_ITEM_URL,
        parent=UserDatasIndexView,
        request_param='action=edit',
    )
    config.add_admin_view(
        TemplateDisableView,
        route_name=TEMPLATE_ITEM_URL,
        request_param='action=disable',
    )
    config.add_admin_view(
        TemplateDeleteView,
        route_name=TEMPLATE_ITEM_URL,
        request_param='action=delete',
    )
