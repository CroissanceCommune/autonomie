#-*-coding:utf-8*-*
# * File Name : model.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : mer. 11 janv. 2012
# * Last Modified : lun. 04 févr. 2013 11:37:49 CET
#
# * Project : autonomie
#
"""
    Regouping all models imports is necessary
    to allow the metadata.create_all function to work well
"""
from base import DBBASE
from base import DBSESSION

import client
import company
import config
import holiday
import project
import treasury
import tva
import user
import task
