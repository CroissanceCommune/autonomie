# -*- coding: utf-8 -*-
# * File Name : utils.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 29-08-2012
# * Last Modified :
#
# * Project :
#
"""
    script utility, allows the use of the app's context (database, models ...)
    from within command line calls
"""
import logging
from docopt import docopt
from pyramid.paster import bootstrap
from transaction import commit


def command(func, doc):
    """
        Usefull function to wrap command line scripts
    """
    logging.basicConfig()
    args = docopt(doc)
    pyramid_env = bootstrap(args['<config_uri>'])
    try:
        func(args)
    finally:
        pyramid_env['closer']()
    commit()
    return 0
