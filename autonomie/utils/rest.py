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
    Rest related utilities
"""
from pyramid.httpexceptions import HTTPError
from pyramid.httpexceptions import HTTPTemporaryRedirect
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


class Apiv1Resp(dict):
    def __init__(self, body, status='success'):
        dict.__init__(self, status=status, result=body)


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


def add_rest_views(config, route_name, factory,
        edit_rights='edit', add_rights='view', view_rights='view'):
    """
        Add a rest iface associating the factory's methods to the different
        request methods of the routes based on route_name :
            route_name : route name of a single item (items/{id})
            route_name + "s" : route name of the items model (items)
        del - > route_name, DELETE
        put - > route_name, PUT
        get - > route_name, GET
        post - > route_name+"s", POST
    """
    # FIXME : l'api rest est placée à la racine, on a pas de traversal qui nous
    # permet de donner des droits autres que 'view' à nos users, donc tout est
    # autorisé pour les gens qui ont les droits 'view'
    config.add_view(factory,
            attr='get',
            route_name=route_name,
            renderer="json",
            request_method='GET',
            permission=view_rights,
            xhr=True)
    config.add_view(factory,
            attr='post',
            # C pas beau je sais
            route_name=route_name + "s",
            renderer="json",
            request_method='POST',
            permission=add_rights,
            xhr=True)
    config.add_view(factory,
            attr='put',
            route_name=route_name,
            renderer="json",
            request_method='PUT',
            permission=edit_rights,
            xhr=True)
    config.add_view(factory,
            attr='delete',
            route_name=route_name,
            renderer="json",
            request_method='DELETE',
            permission=edit_rights,
            xhr=True)


def make_redirect_view(route_name, with_id=True):
    """
        Returns a redirect function that redirects to route_name
        :@param with_id: the route expects and id
    """
    def view(request):
        if with_id:
            id_ = request.context.id
            url = request.route_path(route_name, id=id_)
        else:
            url = request.route_path(route_name)
        return HTTPTemporaryRedirect(url)
    return view
