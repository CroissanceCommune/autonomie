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
    Regouping all models imports is necessary
    to allow the metadata.create_all function to work well
"""
from autonomie_base.models.base import DBBASE
from autonomie_base.models.base import DBSESSION


import activity
import career_stage
import career_path
import commercial
import company
import competence
import config
import customer
import files
import holiday
import node
import options
import payments
import sale_product
import statistics
import treasury
import tva
import task
import workshop
from .accounting import operations
from .accounting import treasury_measures
from .accounting import income_statement_measures
from .expense import sheet
from .expense import types
from .expense import payment
from .project import phase
from .project import project
from .project import types
from .training import trainer
from .user import user
from .user import login
from .user import group
from .user import userdatas
from autonomie_celery import models


def adjust_for_engine(engine):
    """
    Ajust the models definitions to fit the current database engine
    :param obj engine: The current engine to be used
    """
    if engine.dialect.name == 'mysql':
        # Mysql does case unsensitive comparison by default
        login.Login.__table__.c.login.type.collation = 'utf8_bin'


__author__ = "Arezki Feth, Miotte Julien, Pettier Gabriel and Tjebbes Gaston"
__copyright__ = "Copyright 2012-2013, Croissance Commune"
__license__ = "GPL"
__version__ = "3.0"
