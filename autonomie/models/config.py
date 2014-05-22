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
    app = Column("config_app",
            String(50),
            primary_key=True,
            default='autonomie')
    name = Column("config_name", String(255), primary_key=True)
    value = Column("config_value", Text())

    @classmethod
    def get(cls, keyname):
        query = super(Config, cls).query()
        query = query.filter(Config.app=='autonomie')
        query = query.filter(Config.name==keyname)
        return query.first()

    @classmethod
    def query(cls):
        query = super(Config, cls).query()
        return query.filter(Config.app=='autonomie')


def get_config():
    """
        Return a dictionnary with the config objects
    """
    return dict((entry.name, entry.value)
                for entry in Config.query().all())
