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
from autonomie.models.model import Config

def load_config(dbsession, name=None):
    """
        Load the config value for key
    """
    if name:
        entry = dbsession.query(Config).filter(Config.name==name).first()
        if not entry:
            return {}
        else:
            return {entry.name:entry.value}
    else:
        return dict((entry.name, entry.value)
                for entry in dbsession.query(Config).all())
