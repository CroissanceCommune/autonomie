# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pkg_resources
from autonomie.resources import admin_resources


class AdminLayout(object):
    autonomie_version = pkg_resources.get_distribution('autonomie').version

    def __init__(self, context, request):
        admin_resources.need()


def includeme(config):
    config.add_layout(
        AdminLayout,
        template='autonomie:templates/admin/layout.mako',
        name='admin',
    )
