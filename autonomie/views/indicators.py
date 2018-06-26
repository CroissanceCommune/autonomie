# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from pyramid.httpexceptions import HTTPFound


def force_indicator(context, request):
    """
    Force an indicator (sets forced to True
    """
    context.force()
    request.dbsession.merge(context)
    return HTTPFound(request.referrer)


def includeme(config):
    config.add_route(
        "/sale_file_requirements/{id}",
        "/sale_file_requirements/{id}",
        traverse="sale_file_requirements/{id}"
    )
    config.add_view(
        force_indicator,
        route_name="/sale_file_requirements/{id}",
        permission="force.indicator",
        request_param="action=force",
    )
