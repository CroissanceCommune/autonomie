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
File related views, views related to the file model
"""

from autonomie.export.utils import write_file_to_request

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
    simple view for a given file
    """
    return dict(
            title=u"Fichier {0}".format(context.name),
            file=context,
            )


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
