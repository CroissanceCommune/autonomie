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
import cStringIO as StringIO
from sqlalchemy.orm import load_only

from pyramid_deform import SessionFileUploadTempStore

from autonomie.models.task import Task
from autonomie.models.files import (
    File,
    FileType,
)
from autonomie.models.project.business import Business
from autonomie.models.project.file_types import BusinessTypeFileType

from autonomie.compute.math_utils import convert_to_int
from autonomie.utils.strings import human_readable_filesize
from autonomie import forms
from autonomie.forms.validators import validate_image_mime


class CustomFileUploadWidget(deform.widget.FileUploadWidget):
    """
    file upload widget that handles filters when deserializing

        filters

            An optionnal list (or simple filter) that will be fired on the datas
            (for example in order to reduce image sizes)
    """
    template = "fileupload.pt"

    def deserialize(self, field, pstruct):
        data = deform.widget.FileUploadWidget.deserialize(self, field, pstruct)
        # We're returning the datas in the appstruct dict, we format the file if
        # needed
        if hasattr(data, 'has_key') and 'fp' in data:

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


class FileNode(colander.SchemaNode):
    """
    A main file upload node class
    """
    schema_type = deform.FileData
    title = u"Choix du fichier"
    default_max_size = 1048576
    _max_allowed_file_size = None

    def validator(self, node, value):
        """
        Build a file size validator
        """
        request = self.bindings['request']
        max_filesize = self._get_max_allowed_file_size(request)
        file_obj = value.get('fp')
        if file_obj:
            file_obj.seek(0)
            size = len(file_obj.read())
            if size > max_filesize:
                message = u"Ce fichier est trop volumineux"
                raise colander.Invalid(node, message)

    def _get_max_allowed_file_size(self, request):
        """
        Return the max allowed filesize configured in autonomie
        """
        if self._max_allowed_file_size is None:
            settings = request.registry.settings
            size = settings.get("autonomie.maxfilesize", self.default_max_size)
            self._max_allowed_file_size = convert_to_int(
                size, self.default_max_size
            )
        return self._max_allowed_file_size

    @colander.deferred
    def widget(self, kw):
        request = kw['request']
        tmpstore = SessionDBFileUploadTempStore(request)
        return CustomFileUploadWidget(tmpstore)

    def after_bind(self, node, kw):
        size = self._get_max_allowed_file_size(kw['request'])
        if not getattr(self, 'description', ''):
            self.description = ""

        self.description += u" Taille maximale : {0}".format(
            human_readable_filesize(size)
        )


class ImageNode(FileNode):
    def validator(self, node, value):
        FileNode.validator(self, node, value)
        validate_image_mime(node, value)

    def after_bind(self, node, kw):
        if not getattr(self, 'description', ''):
            self.description = ""

        self.description += u"Charger un fichier de type image \
(*.png *.jpeg *.jpg)"


class FileTypeNode(colander.SchemaNode):
    title = u"Type de document"
    schema_type = colander.Int

    def __init__(self, *args, **kwargs):
        colander.SchemaNode.__init__(self, *args, **kwargs)
        self.types = []

    @colander.deferred
    def widget(self, kw):
        context = kw['request'].context
        available_types = self._collect_available_types(context)
        if available_types:
            choices = [(t.id, t.label) for t in available_types]
            choices.insert(0, ('', ''))
            widget = deform.widget.SelectWidget(values=choices)
        else:
            widget = deform.widget.HiddenWidget()
        return widget

    def _collect_available_types(self, context):
        """
        Collect file types that may be loaded for the given context

        :param obj context: The current object we're attaching a file to
        :returns: A list of FileType instances
        """
        result = []
        if isinstance(context, File):
            context = context.parent

        if isinstance(context, Task) or isinstance(context, Business):
            business_type_id = context.business_type_id

            result = BusinessTypeFileType.get_file_type_options(
                business_type_id, context.type_
            )
        else:
            result = FileType.query().options(load_only('id', 'label')).all()
        return result

    def after_bind(self, node, kw):
        get_params = kw['request'].GET
        if 'file_type_id' in get_params:
            self.default = int(get_params["file_type_id"])


class FileUploadSchema(colander.Schema):
    come_from = forms.come_from_node()
    popup = forms.popup_node()

    file_type_id = FileTypeNode(missing=colander.drop)
    upload = FileNode()

    description = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(
            min=5,
            max=100,
            min_err=u"La description ne doit pas être inférieure à 5 caractères",
            max_err=u"La description ne doit pas être supérieure à 100 caractères"),
    )


def get_template_upload_schema():
    """
    Return the form schema for template upload
    """
    def add_description(node, kw):
        node['upload'].description += u" Le fichier doit être au format ODT"
        del node['file_type_id']
    schema = FileUploadSchema(after_bind=add_description)
    return schema
