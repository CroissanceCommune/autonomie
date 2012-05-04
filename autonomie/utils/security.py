# -*- coding: utf-8 -*-
# * File Name : security.py
#
# * Copyright (C) 2010 Gaston TJEBBES <tonthon21@gmail.com>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-02-2012
# * Last Modified : ven. 04 mai 2012 16:47:26 CEST
#
# * Project : autonomie
#
"""
    Root factory <=> Acl handling
"""
from pyramid.security import Allow
from pyramid.security import Authenticated

class RootFactory(object):
    """
       Ressource factory, returns the appropriate resource regarding
       the request object
    """
    __acl__ = [(Allow, Authenticated, 'view'),
                ]
    def __init__(self, request):
        self.request = request

class Forbidden(Exception):
    """
        Forbidden exception, used to raise a forbidden action error
    """
    pass
