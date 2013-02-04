# -*- coding: utf-8 -*-
# * File Name : config.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 20-10-2012
# * Last Modified :
#
# * Project :
#
"""
    Config model stores :
    Autonomie's welcome message
    Documents footers, headers ...
"""

from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import String
from autonomie.models.base import DBBASE
from autonomie.models.base import default_table_args


class Config(DBBASE):
    """
        Table containing the main configuration
          `config_app` varchar(50) NOT NULL,
          `config_name` varchar(255) NOT NULL,
          `config_value` text,
          PRIMARY KEY  (`config_app`,`config_name`)
    """
    __tablename__ = 'config'
    __table_args__ = default_table_args
    app = Column("config_app", String(50), primary_key=True)
    name = Column("config_name", String(255), primary_key=True)
    value = Column("config_value", Text())


def get_config():
    """
        Return a dictionnary with the config objects
    """
    return dict((entry.name, entry.value)
                for entry in Config.query().all())
