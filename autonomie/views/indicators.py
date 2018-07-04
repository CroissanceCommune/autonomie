# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from pyramid.httpexceptions import HTTPFound


def force_indicator_view(context, request):
    """
    Force an indicator (sets forced to True
    """
    if context.forced:
        context.unforce()
    else:
        context.force()
    request.dbsession.merge(context)
    return HTTPFound(request.referrer)


def validate_file_view(context, request):
    """
    """
    validation_status = request.GET.get('validation_status')
    if validation_status in context.VALIDATION_STATUS:
        context.set_validation_status(validation_status)
    else:
        request.session.flash(u"Statut invalide : %s" % validation_status)
    return HTTPFound(request.referrer)


def includeme(config):
    config.add_route(
        "/sale_file_requirements/{id}",
        "/sale_file_requirements/{id}",
        traverse="sale_file_requirements/{id}"
    )
    config.add_view(
        force_indicator_view,
        route_name="/sale_file_requirements/{id}",
        permission="force.indicator",
        request_param="action=force",
    )
    config.add_view(
        validate_file_view,
        route_name="/sale_file_requirements/{id}",
        permission="valid.indicator",
        request_param="action=validation_status",
    )
