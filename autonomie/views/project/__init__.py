# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def includeme(config):
    config.include('.routes')
    config.include('.layout')
    config.include('.project')
    config.include('.phases')
