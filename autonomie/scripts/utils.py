# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
#

"""
    script utility, allows the use of the app's context (database, models ...)
    from within command line calls
"""
import logging
from docopt import docopt
from pyramid.paster import bootstrap
from transaction import commit
from pyramid.paster import setup_logging
from transaction import commit


def command(func, doc):
    """
        Usefull function to wrap command line scripts
    """
    logging.basicConfig()
    args = docopt(doc)
    pyramid_env = bootstrap(args['<config_uri>'])
    setup_logging(args['<config_uri>'])
    try:
        func(args)
    finally:
        pyramid_env['closer']()
    commit()
    return 0


def get_value(arguments, key, default):
    """
        Return the value for key in arguments or default
    """
    val = arguments.get('--%s' % key)
    if not val:
        val = default
    return val
