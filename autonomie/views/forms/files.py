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

from pyramid_deform import SessionFileUploadTempStore


class SessionDBFileUploadTempStore(SessionFileUploadTempStore):
    def preview_url(self, uid):
        if self.request.context.type_ == 'file':
            return self.request.route_path('file', id=self.request.context.id)
        else:
            return None

def get_file_datas(request, file_obj):
    from cStringIO import StringIO
    buf = StringIO()
    buf.write(file_obj.data)
    datas = {
            'uid': str(file_obj.id),
            'fp': buf,
            'mimetype': file_obj.mimetype,
            'filename': file_obj.name,
            'size': file_obj.size,
            'preview_url': request.route_path('file', id=file_obj.id)
            }
    return datas

@colander.deferred
def deferred_upload_widget(node, kw):
    request = kw['request']
    tmpstore = SessionDBFileUploadTempStore(request)
    if request.context.type_ == 'file':
        tmpstore[str(request.context.id)] = get_file_datas(request, request.context)
    return deform.widget.FileUploadWidget(tmpstore)


@colander.deferred
def deferred_filetype_select(node, kw):
    request = kw['request']
    filetypes = json.loads(request.config.get('attached_filetypes', '[]'))
    filetypes.insert(0, "")
    values = zip(filetypes, filetypes)
    return deform.widget.SelectWidget(values=values)


class FileUploadSchema(colander.Schema):
    parent_id = colander.SchemaNode(
            colander.Integer(),
            widget=deform.widget.HiddenWidget(),
            )

    come_from = colander.SchemaNode(
            colander.String(),
            widget=deform.widget.HiddenWidget(),
            missing="",
            )

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
            )
