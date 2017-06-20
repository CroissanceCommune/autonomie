# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def format_civilite(civilite_str):
    """
    Shorten the civilite string

    :param str civilite_str: Monsieur/Madame
    :returns: Mr/Mme
    :rtype: str
    """
    res = civilite_str
    if civilite_str.lower() == u'monsieur':
        res = u"Mr"
    elif civilite_str.lower() == u'madame':
        res = u"Mme"
    return res
