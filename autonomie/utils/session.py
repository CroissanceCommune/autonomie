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
    Custom beaker session handling allowing to use a remember me cookie
    that allows long time connections
"""
import logging

from beaker.session import SessionObject
from pyramid_beaker import session_factory_from_settings


logger = logging.getLogger(__name__)


def get_session_factory(settings):
    """
        Wrap the beaker session factory to add longtimeout support
    """
    factory = session_factory_from_settings(settings)
    class AutonomieSessionObject(factory):
        """
            Our pyramid session object
        """
        _longtimeout = factory._options.pop("longtimeout")
        def __init__(self, request):
            options = self._options.copy()
            if "remember_me" in request.cookies.keys():
                options['timeout'] = self._longtimeout

            SessionObject.__init__(self, request.environ, **options)
            def session_callback(request, response):
                exception = getattr(request, 'exception', None)
                if (exception is None or self._cookie_on_exception
                    and self.accessed()):
                    self.persist()
                    headers = self.__dict__['_headers']
                    if headers['set_cookie'] and headers['cookie_out']:
                        response.headerlist.append(
                            ('Set-Cookie', headers['cookie_out']))
            request.add_response_callback(session_callback)
    return AutonomieSessionObject
