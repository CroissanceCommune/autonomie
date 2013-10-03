# -*- coding: utf-8 -*-
# * File Name : utils.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 03-10-2013
# * Last Modified :
#
# * Project : Autonomie
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

