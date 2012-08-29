# -*- coding: utf-8 -*-
# * File Name : initialize.py
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
    Initialization function
"""
from autonomie.models import DBSESSION
from autonomie.models import DBMETADATA
from autonomie.models import DBBASE
from autonomie.scripts.migrate import fetch_head

def initialize_sql(engine):
    """
        Initialize the database engine
    """
    DBSESSION.configure(bind=engine)
    DBMETADATA.bind = engine
    if not engine.table_names():
        fetch_head()
        DBBASE.metadata.create_all(engine)
    return DBSESSION
