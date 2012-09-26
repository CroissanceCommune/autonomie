# -*- coding: utf-8 -*-
# * File Name : config.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 26-04-2012
# * Last Modified : 26-04-2012
#
# * Project :
#
"""
    Simple utilities to access main configuration
"""


def get_config(request, dbsession=None):
    """
        Return a dictionnary with the config objects
    """
    from autonomie.models.model import Config
    if not dbsession:
        dbsession = request.dbsession
    return dict((entry.name, entry.value)
                for entry in dbsession.query(Config).all())
