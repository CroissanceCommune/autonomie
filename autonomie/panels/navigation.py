# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging

logger = logging.getLogger(__name__)


def navigation_panel(context, request):
    """
    Show the navigation panel

    Breadcrumb
    Alternative links
    Back link
    """
    logger.debug(u" -> Navigation panel")
    return dict(
        links=request.navigation.links,
        back_link=request.navigation.back_link,
        breadcrumb=request.navigation.breadcrumb,
    )


def includeme(config):
    config.add_panel(
        navigation_panel,
        name='navigation',
        renderer='autonomie:templates/panels/navigation.pt'
    )
