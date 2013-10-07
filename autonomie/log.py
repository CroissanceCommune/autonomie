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
    Logging utility to allow logging ips into custom logs
"""
import logging
from pyramid.threadlocal import get_current_request


def get_user(request):
    """
        Return the current user or anonymous
    """
    if request and hasattr(request, "_user"):
        if hasattr(request._user, "login"):
            return request._user.login
    return "Anonymous"

def get_ip(request):
    """
        Return the client's ip or None
    """
    if request:
        return request.remote_addr
    else:
        return "None"

class CustomFileHandler(logging.FileHandler, object):
    """
        CustomeFile Handler allowing to add ip and username in logs
    """
    def emit(self, record):
        request = get_current_request()
        record.ip = get_ip(request)
        record.user = get_user(request)
        super(CustomFileHandler, self).emit(record)

class CustomStreamHandler(logging.StreamHandler, object):
    """
        CustomeStream Handler allowing to add ip and username in logs
    """
    def emit(self, record):
        request = get_current_request()
        record.ip = get_ip(request)
        record.user = get_user(request)
        super(CustomStreamHandler, self).emit(record)
