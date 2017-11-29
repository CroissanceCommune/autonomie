# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging

import pkg_resources
from autonomie.resources import (
    main_group,
    opa_group,
)

logger = logging.getLogger(__name__)


class DefaultLayout(object):
    autonomie_version = pkg_resources.get_distribution('autonomie').version

    def __init__(self, context, request):
        logger.debug("In the default layout")
        main_group.need()


class OpaLayout(object):
    autonomie_version = pkg_resources.get_distribution('autonomie').version

    def __init__(self, context, request):
        logger.debug("In the opa layout")
        opa_group.need()


def includeme(config):
    config.add_layout(
        DefaultLayout,
        template='autonomie:templates/layouts/default.mako'
    )
    config.add_layout(
        DefaultLayout,
        template='autonomie:templates/layouts/default.mako',
        name='default',
    )
    config.add_layout(
        OpaLayout,
        template='autonomie:templates/layouts/opa.mako',
        name='opa'
    )
    config.add_layout(
        DefaultLayout,
        template='autonomie:templates/layouts/login.mako',
        name='login',
    )
