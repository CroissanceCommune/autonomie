# -*- coding: utf-8 -*-
# * File Name : formutils.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 31-01-2012
# * Last Modified : mer. 06 févr. 2013 18:10:03 CET
#
# * Project : autonomie
#
"""
    Deform utility wrappers
"""
import logging
import colander

from deform.form import Form


log = logging.getLogger(__name__)


def merge_session_with_post(session, app_struct):
    """
        Merge Deform validated datas with SQLAlchemy's objects
        Allow to spare some lines of assigning datas to the object
        before writing to database
    """
    for key, value in app_struct.items():
        setattr(session, key, value)
    return session
