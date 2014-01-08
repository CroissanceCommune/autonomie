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
from autonomie.views.forms import (
        BaseFormView,
        merge_session_with_post,
        )
from autonomie.views.forms.files import FileUploadSchema
from autonomie.resources import fileupload_js


UPLOAD_MISSING_DATAS_MSG = u"Des informations sont manquantes pour \
l'adjonction de fichiers"


UPLOAD_OK_MSG = u"Le fichier a bien été adjoint au document"
EDIT_OK_MSG = u"Le fichier a bien été adjoint au document"


log = logging.getLogger(__name__)


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
    schema = FileUploadSchema()
    title = u"Téléverser un fichier"

    def _parent_id(self):
        """
            Returns the file parent's id
        """
        return self.request.context.id

    def before(self, form):
        fileupload_js.need()

        come_from = self.request.referrer
        log.debug(u"Coming from : %s" % come_from)

        parent_id = self._parent_id()

        appstruct = {
                'parent_id': parent_id,
                'come_from': come_from
                }
        form.set_appstruct(appstruct)

    def format_appstruct(self, appstruct):
        """
            Format the appstruct returned by the form to match the
            datas structure expected for File add/edit
        """
        file_infos = appstruct.pop('upload')
        # Ensure the provided file object isn't consumed yet
        if file_infos.has_key('fp'):
            file_infos['fp'].seek(0)

            # Retrieving file datas from the datas provided by the FileUploadWidget
            appstruct['data'] = file_infos['fp'].read()
            appstruct['size'] = len(appstruct['data'])
            appstruct['mimetype'] = file_infos['mimetype']
            appstruct['name'] = file_infos['filename']
        return appstruct

    def persist_to_database(self, appstruct):
        """
            Execute actions on the database
        """
        # Inserting in the database
        file_object = File(**appstruct)
        self.request.dbsession.add(file_object)
        self.request.session.flash(UPLOAD_OK_MSG)

    def submit_success(self, appstruct):
        """
            Insert data in the database
        """
        log.debug(u"A file has been uploaded (add or edit)")
        log.debug(appstruct)

        come_from = appstruct.pop('come_from')
        appstruct.pop("filetype")

        appstruct = self.format_appstruct(appstruct)

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
                }
        filedict.pop('data')
        filedict.pop('mimetype')
        filedict.pop('size')
        return filedict

    def before(self, form):
        fileupload_js.need()

        come_from = self.request.referrer
        log.debug(u"Coming from : %s" % come_from)


        appstruct = {
                'come_from': come_from
                }
        appstruct.update(self.format_dbdatas())
        form.set_appstruct(appstruct)

    def persist_to_database(self, appstruct):
        merge_session_with_post(self.request.context, appstruct)
        self.request.dbsession.merge(self.request.context)
        self.request.session.flash(EDIT_OK_MSG)


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
    if context.parent.type_ == 'project':
        label = u"Revenir au projet"
    else:
        label = u"Revenir au document"
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
    config.add_view(
            file_dl_view,
            route_name='file',
            permission='view',
            request_param='action=download',
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
