# -*- coding: utf-8 -*-
# * File Name : session.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 19-12-2012
# * Last Modified :
#
# * Project :
#
"""
    Custom beaker session handling allowing to use a remember me cookie
    that allows long time connections
"""
import os

from beaker.session import SessionObject
from pyramid_beaker import session_factory_from_settings

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
