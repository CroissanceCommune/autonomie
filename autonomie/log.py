# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 03-10-2012
# * Last Modified :
#
# * Project :
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
