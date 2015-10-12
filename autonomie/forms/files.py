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
Form schema for file handling
"""
import colander
import deform
import simplejson as json
import cStringIO as StringIO

from pyramid.threadlocal import get_current_registry
from pyramid_deform import SessionFileUploadTempStore

from autonomie.compute.math_utils import convert_to_int
from autonomie.views.render_api import human_readable_filesize
from autonomie import forms


class CustomFileUploadWidget(deform.widget.FileUploadWidget):
    """
    file upload widget that handles filters when deserializing

        filters

            An optionnal list (or simple filter) that will be fired on the datas
            (for example in order to reduce image sizes)
    """
    def deserialize(self, field, pstruct):
        data = deform.widget.FileUploadWidget.deserialize(self, field, pstruct)
        # We're returning the datas in the appstruct dict, we format the file if
        # needed
        if hasattr(data, 'has_key') and data.has_key('fp'):

            data['fp'].seek(0)
            if hasattr(self.tmpstore, 'filter_data'):
                data['fp'] = self.tmpstore.filter_data(data['fp'])

            data['data'] = data['fp']

            data['size'] = len(data['fp'].read())
            data['fp'].seek(0)
            data['name'] = data['filename']
        return data


class SessionDBFileUploadTempStore(SessionFileUploadTempStore):
    """
    A session based File upload temp store

    Is necessary for deform's upload widget to be able to keep the datas when
    there are errors on form validation

        request

            The current request object
    """
    def __init__(self, request, filters=None):
        SessionFileUploadTempStore.__init__(self, request)

        if filters and not hasattr(filters, '__iter__'):
            filters = [filters]
        self.filters = filters or []

    def filter_data(self, fbuf):
        """
        Pass file datas through filters
        """
        if self.filters:
            # Use an intermediary buffer
            fdata = StringIO.StringIO(fbuf.read())
            for filter_ in self.filters:
                fdata = filter_(fdata)
                fdata.seek(0)
            return fdata
        else:
            return fbuf

    def preview_url(self, uid):
        doctype = getattr(self.request.context, 'type_', '')
        if doctype:
            return self.request.route_path(doctype, id=self.request.context.id)
        else:
            return None


@colander.deferred
def deferred_upload_widget(node, kw):
    request = kw['request']
    tmpstore = SessionDBFileUploadTempStore(request)
    return CustomFileUploadWidget(
        tmpstore,
        template=forms.TEMPLATES_PATH + "fileupload.pt"
    )


@colander.deferred
def deferred_filetype_select(node, kw):
    request = kw['request']
    filetypes = json.loads(request.config.get('attached_filetypes', '[]'))
    filetypes.insert(0, "")
    values = zip(filetypes, filetypes)
    return deform.widget.SelectWidget(values=values)


def get_max_allowedfilesize():
    """
    Return the max allowed filesize configured in autonomie
    """
    default = 1048576 # 1MB
    settings = get_current_registry().settings
    size = settings.get("autonomie.maxfilesize", default)
    return convert_to_int(size, default)


@colander.deferred
def file_description(node, kw):
    """
        Return the file upload field description
    """
    size = get_max_allowedfilesize()
    return u"Taille maximale : {0}".format(human_readable_filesize(size))


@colander.deferred
def filesize_validator(node, value):
    """
    Validates the file's size
    """
    file_obj = value.get('fp')
    if file_obj:
        file_obj.seek(0)
        max_filesize = get_max_allowedfilesize()
        size = len(file_obj.read())
        if size > max_filesize:
            message = u"Ce fichier est trop volumineux"
            raise colander.Invalid(node, message)


class FileUploadSchema(colander.Schema):
    parent_id = colander.SchemaNode(
        colander.Integer(),
        widget=deform.widget.HiddenWidget(),
        missing=colander.drop,
    )

    come_from = forms.come_from_node()

    filetype = colander.SchemaNode(
        colander.String(),
        widget=deferred_filetype_select,
        missing="",
        title=u"Type de fichier",
    )

    description = colander.SchemaNode(colander.String())

    upload = colander.SchemaNode(
        deform.FileData(),
        widget=deferred_upload_widget,
        title=u"Choix du fichier",
        description=file_description,
        validator=filesize_validator,
    )


def get_template_upload_schema():
    """
    Return the form schema for template upload
    """
    def add_description(node, kw):
        node['upload'].description += u" Le fichier doit être au format ODT"
        del node['filetype']
    schema = FileUploadSchema(after_bind=add_description)
    return schema
