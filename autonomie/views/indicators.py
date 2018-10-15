# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
from pyramid.httpexceptions import HTTPFound
from autonomie.events.indicators import IndicatorChanged

INDICATOR_ROUTE = "/indicators/{id}"


logger = logging.getLogger(__name__)


def force_indicator_view(context, request):
    """
    Force an indicator (sets forced to True
    """
    if context.forced:
        context.unforce()
        logger.debug(
            u"+ Setting force=False for the indicator {}".format(
                context.id,
            )
        )
    else:
        logger.debug(
            u"+ Setting force=True for the indicator {}".format(
                context.id,
            )
        )
        context.force()
    request.dbsession.merge(context)
    request.registry.notify(IndicatorChanged(request, context))
    return HTTPFound(request.referrer)


def validate_file_view(context, request):
    """
    """
    validation_status = request.GET.get('validation_status')
    if validation_status in context.VALIDATION_STATUS:
        logger.debug(u"+ Setting the status of the indicator {} to {}".format(
            context.id, validation_status
        ))
        context.set_validation_status(validation_status)
        request.registry.notify(IndicatorChanged(request, context))
    else:
        request.session.flash(u"Statut invalide : %s" % validation_status)
    return HTTPFound(request.referrer)


def includeme(config):
    config.add_route(INDICATOR_ROUTE, INDICATOR_ROUTE, traverse=INDICATOR_ROUTE)
    config.add_view(
        force_indicator_view,
        route_name=INDICATOR_ROUTE,
        permission="force.indicator",
        request_param="action=force",
    )
    config.add_view(
        validate_file_view,
        route_name=INDICATOR_ROUTE,
        permission="valid.indicator",
        request_param="action=validation_status",
    )
