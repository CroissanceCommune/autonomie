# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def get_excluded_colanderalchemy(title):
    """
    Return colanderalchemy for excluded field but with title set (for other sqla
    inspection based modules like py3o inspection or ods generation)
    """
    return {'exclude': True, title: title}
