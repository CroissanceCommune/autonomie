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
from pyramid.security import NO_PERMISSION_REQUIRED

from autonomie.export.utils import write_file_to_request
from autonomie.utils.widgets import (
    ViewLink,
    Link,
)
from autonomie.models.files import File
from autonomie import forms
from autonomie.forms.files import (
    FileUploadSchema,
)
from autonomie.resources import fileupload_js
from autonomie.views import (
    BaseFormView,
    BaseView,
    DeleteView,
)


UPLOAD_MISSING_DATAS_MSG = u"Des informations sont manquantes pour \
l'adjonction de fichiers"


UPLOAD_OK_MSG = u"Le fichier a bien été enregistré"
EDIT_OK_MSG = u"Le fichier a bien été enregistré"


logger = log = logging.getLogger(__name__)


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


class FileViewRedirectMixin(object):
    """
    Mixin providing tools to handle redirection from within a File related view
    """
    NODE_TYPE_ROUTES = {
        'activity': u"activity",
        'business': '/businesses/{id}/files',
        'cancelinvoice': "/cancelinvoices/{id}.html",
        'estimation': "/estimations/{id}.html",
        'expensesheet': "/expenses/{id}",
        'invoice': "/invoices/{id}.html",
        'project': "project",
        'userdata': "/users/{id}/userdatas/filelist",
        "workshop": u"workshop",
    }

    NODE_TYPE_LABEL = {
        'activity': u'au rendez-vous',
        'business': u"à l'affaire",
        'cancelinvoice': u"à l'avoir",
        'estimation': u'au devis',
        "expensesheet": u"à la note de dépense",
        'invoice': u'à la facture',
        'project': u'au projet',
        'userdata': u"à la fiche de gestion sociale",
        "workshop": u"à l'atelier",
    }

    def get_redirect_item(self):
        item = parent = self.context.parent

        if parent.type_ == 'userdata':
            item = parent.user
        return item

    def back_url(self):
        parent = self.context.parent
        route_name = self.NODE_TYPE_ROUTES.get(parent.type_)
        if route_name is None:
            raise Exception(u"You should set the route on the FileView \
attribute")
        return self.request.route_path(
            route_name, id=self.get_redirect_item().id
        )

    def get_label(self):
        parent = self.context.parent
        type_label = self.NODE_TYPE_LABEL.get(parent.type_, u'au précédent')
        label = u"Revenir {0}".format(type_label)
        return label


class FileView(BaseView, FileViewRedirectMixin):
    """
    A base file view allowing to tune the way datas is shown
    """
    def populate_actionmenu(self):
        return Link(self.back_url(), self.get_label())

    def edit_url(self):
        return self.request.route_path(
            "file", id=self.context.id, _query={'action': 'edit'}
        )

    def delete_url(self):
        return self.request.route_path(
            "file", id=self.context.id, _query={'action': 'delete'}
        )

    def __call__(self):
        return dict(
            title=u"Fichier {0}".format(self.context.name),
            file=self.context,
            edit_url=self.edit_url(),
            delete_url=self.delete_url(),
            navigation=self.populate_actionmenu(),
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
        forms.merge_session_with_post(file_object, appstruct)
        self.request.dbsession.add(file_object)
        self.request.dbsession.flush()
        self.request.session.flash(self.valid_msg)

    def redirect(self, come_from=None):
        """
        Build the redirection url

        Can be overriden to specify a redirection
        """
        return HTTPFound(come_from)

    def submit_success(self, appstruct):
        """
            Insert data in the database
        """
        log.debug(u"A file has been uploaded (add or edit)")

        come_from = appstruct.pop('come_from', None)
        appstruct.pop("filetype", '')

        appstruct = forms.flatten_appstruct(appstruct)

        self.persist_to_database(appstruct)

        # Clear all informations stored in session by the tempstore used for the
        # file upload widget
        self.request.session.pop('substanced.tempstore')
        self.request.session.changed()
        return self.redirect(come_from)


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

        appstruct = {'come_from': come_from}
        appstruct.update(self.format_dbdatas())
        form.set_appstruct(appstruct)

    def persist_to_database(self, appstruct):
        forms.merge_session_with_post(self.request.context, appstruct)
        self.request.dbsession.merge(self.request.context)
        self.request.session.flash(self.valid_msg)


def get_add_file_link(
    request, label=u"Attacher un fichier", perm="add.file", route=None
):
    """
        Add a button for file attachment
    """
    context = request.context
    route = route or context.type_
    return ViewLink(
        label,
        perm,
        path=route,
        id=context.id,
        _query=dict(action="attach_file")
    )


class FileDeleteView(DeleteView, FileViewRedirectMixin):
    delete_msg = u"Le fichier a été supprimé"

    def redirect(self):
        return HTTPFound(self.back_url())


def add_routes(config):
    """
    Add module's related routes
    """
    config.add_route(
        "file",
        "/files/{id:\d+}",
        traverse="/files/{id}"
    )
    config.add_route(
        "filepng",
        "/files/{id:\d+}.png",
        traverse="/files/{id}"
    )
    config.add_route(
        "public",
        "/public/{name}",
        traverse="/configfiles/{name}"
    )


def includeme(config):
    """
    Configure views
    """
    add_routes(config)
    config.add_view(
        FileView,
        route_name="file",
        permission='view.file',
        renderer="file.mako",
    )
    config.add_view(
        file_dl_view,
        route_name='filepng',
        permission='view.file',
    )
    config.add_view(
        file_dl_view,
        route_name='file',
        permission='view.file',
        request_param='action=download',
    )
    config.add_view(
        file_dl_view,
        route_name='public',
        permission=NO_PERMISSION_REQUIRED,
    )
    config.add_view(
        FileEditView,
        route_name="file",
        permission='edit.file',
        renderer="base/formpage.mako",
        request_param='action=edit',
    )
    config.add_view(
        FileDeleteView,
        route_name='file',
        permission='delete.file',
        request_param='action=delete',
    )
