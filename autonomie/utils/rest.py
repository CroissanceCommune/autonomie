# -*- coding: utf-8 -*-
# * File Name : rest.py
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
    Rest related utilities
"""
from pyramid.httpexceptions import HTTPError
from pyramid.response import Response

from pyramid.renderers import render

def allowed_methods(*allowed):
    """
        Custom predict checking if the HTTP method in the allowed set.
        It also changes the request.method according to "_method" form parameter
        and "X-HTTP-Method-Override" header
    """
    def predicate(info, request):
        if request.method == 'POST':
            request.method = (
                request.POST.get('_method', '').upper() or
                request.headers.get('X-HTTP-Method-Override', '').upper() or
                request.method)

        return request.method in allowed
    return predicate


class RestError(HTTPError):
    """
        Rest error, allows to raise errors from rest apis like we would do with
        common http exceptions
    """
    def __init__(self, errors, code=400):
        body = {'status':"error", "errors":errors}
        Response.__init__(self, status=code, body=render("json", body))
        self.content_type = 'application/json'


class RestJsonRepr(object):
    """
        BaseJson model wrapper
        Allows to enhance the __json__ method of an sqlalchemy model by
        formatting its output with a colander schema for UI representation
        purpose.
        Takes the json dict and update it with the output of the serialize
        method of the given schema

        :attr schema: colander schema used to preformat datas for ui rendering
        :param model: the model instance we have to format

        :param bind_params: parameters used to bind the schema.
        By default the json renderer passes the request when calling the
        __json__ method of our object, so we use request as default bind_param
    """
    schema = None
    def __init__(self, model, bind_params=None):
        self.model = model
        self.bind_params = bind_params

    def get_schema(self, request):
        """
            Return the binded schema
        """
        if self.bind_params is None:
            bind_params = dict(request=request)
        else:
            bind_params = self.bind_params
        return self.schema.bind(**bind_params)

    def preformat(self, appstruct, request):
        """
            Pass the values through the form schema to preformat some datas for
            ui representation
            (e.g: amounts are represented as floats while they are integers in
            the db)
        """
        if self.schema is not None:
            schema = self.get_schema(request)
            appstruct = schema.serialize(appstruct)
        return appstruct

    def appstruct(self, request):
        """
            Return the appstruct associated to the current schema
            Should be overriden if the model has some relationships
        """
        if hasattr(self.model, '__json__'):
            return self.model.__json__(request)
        else:
            return self.model.appstruct()

    def postformat(self, appstruct):
        """
            allows to postformat the data we want to provide as json
        """
        return appstruct

    def __json__(self, request):
        appstruct = self.appstruct(request)
        result = self.preformat(appstruct, request)
        # We update the appstruct with the value we had expected from the json
        # repr
        for key, value in appstruct.items():
            if not result.has_key(key):
                result[key] = value
        result = self.postformat(result)
        return result
