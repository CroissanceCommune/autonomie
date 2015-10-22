# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2015 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
"""
Configuration de filedepot
"""
import cgi
import logging
from autonomie.export.utils import detect_file_headers


logger = logging.getLogger(__name__)


def configure_filedepot(settings):
    """
    Setup filedepot storage(s)
    """
    try:
        path = settings['autonomie.depot_path']
    except KeyError, err:
        logger.exception(
            u" !!!! You forgot to configure filedepot with an \
'autonomie.depot_path' setting"
        )
        raise err

    from depot.manager import DepotManager
    name = "local"
    if name not in DepotManager._depots:
        DepotManager.configure(name, {'depot.storage_path': path})


def _to_fieldstorage(fp, filename, size, **_kwds):
    """ Build a :class:`cgi.FieldStorage` instance.

    Deform's :class:`FileUploadWidget` returns a dict, but
    :class:`depot.fields.sqlalchemy.UploadedFileField` likes
    :class:`cgi.FieldStorage` objects
    """
    f = cgi.FieldStorage()
    f.file = fp
    f.filename = filename
    f.type = detect_file_headers(filename)
    f.length = size
    return f
