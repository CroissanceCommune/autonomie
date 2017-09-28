# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import functools


def includeme(config):
    config.include('.vente')
    config.include('.receipts')
    config.include('.accounting')
