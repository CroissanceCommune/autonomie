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
    Export utilities
"""
import os
from autonomie.utils.ascii import (
        force_ascii,
        )


MIMETYPES = {'.csv': 'application/csv',
        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.ms-excel',
        '.pdf': 'application/pdf',
        '.txt': 'text/plain'}


def detect_file_headers(filename):
    """
        Return the headers adapted to the given filename
    """
    ext = os.path.splitext(filename)[1]
    return MIMETYPES.get(ext, "text/plain")


def write_headers(request, filename, header):
    """
        Write the given headers to the current request
    """
    request.response.content_type = header
    request.response.headerlist.append(
            ('Content-Disposition',
             'attachment; filename={0}'.format(force_ascii(filename))))
    return request


def write_file_to_request(request, filename, buf, headers=None):
    """
        Write a buffer as request content
        :param request: Pyramid's request object
        :param filename: The destination filename
        :param buf: The file buffer mostly StringIO object, should provide a
            getvalue method
        :param headers: Headers to pass to the request
            (automatic detection is provided for many types)
    """
    if headers is None:
        headers = detect_file_headers(filename)
    request = write_headers(request, filename, headers)
    request.response.write(buf.getvalue())
    return request

