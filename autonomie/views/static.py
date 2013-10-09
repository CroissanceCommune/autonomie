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
    Custom views for dynamic static datas
"""
import os

from pkg_resources import resource_filename

from pyramid.response import Response
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config

def make_root_static_view(filename, ctype):
    """
        Return a static view rendering given file with headers set to the ctyp
        Content-Type
    """
    fpath = resource_filename("autonomie", os.path.join("static", filename))
    file_datas = open(fpath).read()
    def static_view(context, request):
        file_response =  Response(content_type=ctype, body=file_datas)
        return file_response
    return static_view


def includeme(config):
    config.add_route('favicon.ico', '/favicon.ico')
    config.add_route('robots.txt', '/robots.txt')
    config.add_view(make_root_static_view("robots.txt", 'text/plain'),
                        route_name="robots.txt",
                        permission=NO_PERMISSION_REQUIRED)
    config.add_view(make_root_static_view("favicon.ico", "image/x-icon"),
                        route_name="favicon.ico",
                        permission=NO_PERMISSION_REQUIRED)
