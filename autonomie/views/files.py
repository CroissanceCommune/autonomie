# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
#

"""
    views related to the file model

    Download
    Add
    Edit
    Delete

"""
import logging
from pyramid.httpexceptions import HTTPFound

from autonomie.export.utils import write_file_to_request
from autonomie.utils.widgets import ViewLink
from autonomie.models import DBSESSION
from autonomie.models.files import File
from autonomie import forms
from autonomie.forms.files import FileUploadSchema
from autonomie.resources import fileupload_js
from autonomie.views import (
    BaseFormView,
    merge_session_with_post,
)


UPLOAD_MISSING_DATAS_MSG = u"Des informations sont manquantes pour \
l'adjonction de fichiers"


UPLOAD_OK_MSG = u"Le fichier a bien été adjoint au document"
EDIT_OK_MSG = u"Le fichier a bien été adjoint au document"


log = logging.getLogger(__name__)


NODE_TYPE_LABEL = {
    'project': u'projet',
    'estimation': u'document',
    'invoice': u'document',
    'cancelinvoice': u'document',
    'activity': u'rendez-vous',
    }



def file_dl_view(context, request):
    """
    download view for a given file
    """
    write_file_to_request(
            request,
            context.name,
            context,
            context.mimetype,
            )
    return request.response


def file_view(context, request):
    """
    simple view for a given file, displays information related to this file
    """
    populate_actionmenu(context, request)
    return dict(
            title=u"Fichier {0}".format(context.name),
            file=context,
            )


class FileUploadView(BaseFormView):
    """
    Form view for file upload

    Current context for this view is the document the file should be attached to
    (Invoice, Estimation...)

    By getting the referrer url from the request object, we provide the
    redirection to the original page when the file is added

    """
    factory = File
    schema = FileUploadSchema()
    title = u"Téléverser un fichier"
    valid_msg = UPLOAD_OK_MSG

    def _parent_id(self):
        """
            Returns the file parent's id
        """
        return self.request.context.id

    def before(self, form):
        fileupload_js.need()

        come_from = self.request.referrer
        parent_id = self._parent_id()

        appstruct = {
                'parent_id': parent_id,
                'come_from': come_from,
                }
        form.set_appstruct(appstruct)


    def persist_to_database(self, appstruct):
        """
            Execute actions on the database
        """
        # Inserting in the database
        file_object = self.factory()
        merge_session_with_post(file_object, appstruct)
        self.request.dbsession.add(file_object)
        self.request.session.flash(self.valid_msg)

    def submit_success(self, appstruct):
        """
            Insert data in the database
        """
        log.debug(u"A file has been uploaded (add or edit)")

        come_from = appstruct.pop('come_from')
        appstruct.pop("filetype", '')

        appstruct = forms.flatten_appstruct(appstruct)


        self.persist_to_database(appstruct)

        # Clear all informations stored in session by the tempstore used for the
        # file upload widget
        self.request.session.pop('substanced.tempstore')
        self.request.session.changed()
        return HTTPFound(come_from)


class FileEditView(FileUploadView):
    """
        View for file object modification

        Current context is the file itself
    """
    valid_msg = EDIT_OK_MSG

    @property
    def title(self):
        """
            The form title
        """
        return u"Modifier le fichier {0}".format(self.request.context.name)

    def format_dbdatas(self):
        """
            format the database file object to match the form schema
        """
        filedict = self.request.context.appstruct()

        filedict['upload'] = {
            'filename': filedict['name'],
            'uid': str(self.request.context.id),
            'preview_url': self.request.route_url(
                'file',
                id=self.request.context.id,
                _query={'action': 'download'}
            )
        }
        # Since data is a deferred column it should not be present in the output
        # If in the request lifecycle, this column was already accessed, it will
        # be present and should be poped out (no need for it in this form)
        filedict.pop('data', None)
        filedict.pop('mimetype')
        filedict.pop('size')
        return filedict

    def before(self, form):
        fileupload_js.need()

        come_from = self.request.referrer


        appstruct = {
                'come_from': come_from
                }
        appstruct.update(self.format_dbdatas())
        form.set_appstruct(appstruct)

    def persist_to_database(self, appstruct):
        merge_session_with_post(self.request.context, appstruct)
        self.request.dbsession.merge(self.request.context)
        self.request.session.flash(self.valid_msg)


def get_add_file_link(request):
    """
        Add a button for file attachment
    """
    context = request.context
    return ViewLink(
            u"Attacher un fichier",
            "edit",
            path=context.type_,
            id=context.id,
            _query=dict(action="attach_file")
            )


def populate_actionmenu(context, request):
    """
        Add menu items
    """
    type_label = NODE_TYPE_LABEL.get(context.parent.type_, u'précédent')
    label = u"Revenir au {0}".format(type_label)
    request.actionmenu.add(
        ViewLink(
            label,
            perm='view',
            path=context.parent.type_,
            id=context.parent.id)
        )
    request.actionmenu.add(
        ViewLink(
            u"Éditer",
            perm=u'edit',
            path="file",
            id=context.id,
            _query=dict(action='edit'),
            )
        )
    request.actionmenu.add(
        ViewLink(
            u"Supprimer le fichier",
            perm=u'edit',
            path="file",
            confirm=u"Êtes-vous sûr de vouloir supprimer ce fichier ?",
            id=context.id,
            _query=dict(action='delete')
            )
        )


def file_delete_view(context, request):
    """
        View for file deletion
    """
    parent = context.parent
    DBSESSION().delete(context)
    return HTTPFound(request.route_path(parent.type_, id=parent.id))


def includeme(config):
    """
    Configure views
    """
    config.add_route("file", "/files/{id:\d+}", traverse="/files/{id}")
    config.add_route("filepng", "/files/{id:\d+}.png", traverse="/files/{id}")
    config.add_route("public", "/public/{name}", traverse="/configfiles/{name}")
    config.add_view(
        file_dl_view,
        route_name='file',
        permission='view',
        request_param='action=download',
    )
    config.add_view(
        file_dl_view,
        route_name='filepng',
        permission='view',
    )
    config.add_view(
        file_dl_view,
        route_name='public',
        permission='view',
    )
    config.add_view(
        file_view,
        route_name="file",
        permission='view',
        renderer="file.mako",
    )
    config.add_view(
        file_delete_view,
        route_name='file',
        permission='edit',
        request_param='action=delete',
    )
    config.add_view(
        FileEditView,
        route_name="file",
        permission='edit',
        renderer="base/formpage.mako",
        request_param='action=edit',
    )
