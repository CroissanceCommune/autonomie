# -*- coding: utf-8 -*-
# * File Name : http_method_middleware.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 08-03-2013
# * Last Modified :
#
# * Project :
#
"""
    WSGI middleware that overrides the HTTP request method
    to allow DELETE and PUT methods
    Since :
    * some browsers doesn't support those http methods
    * some firewalls block those

    We need to restrict the client-server communication to POST and GET
    We pass a _method parameter that stores the http method we want to use
    The middleware parse the request before it arrives at the pyramid level and
    set the appropriate method so that we can go on
"""

class HttpMethodOverrideMiddleware(object):
    """
        WSGI middleware for overriding HTTP Request Method for RESTful support
        app = HttpMethodOverrideMiddleware(app)
    """
    def __init__(self, application):
        self.application = application


    def __call__(self, environ, start_response):
        if 'POST' == environ['REQUEST_METHOD']:
            override_method = ''
            # First check the "_method" form parameter
            if 'form-urlencoded' in environ['CONTENT_TYPE']:
                from webob import Request
                request = Request(environ)
                override_method = request.str_POST.get('_method', '').upper()

            # If not found, then look for "X-HTTP-Method-Override" header
            if not override_method:
                override_method = environ\
                        .get('HTTP_X_HTTP_METHOD_OVERRIDE', '').upper()

            if override_method in ('PUT', 'DELETE', 'OPTIONS', 'PATCH'):
                # Save the original HTTP method
                environ['http_method_override.original_method'] = \
                                                environ['REQUEST_METHOD']
                # Override HTTP method
                environ['REQUEST_METHOD'] = override_method
        return self.application(environ, start_response)
