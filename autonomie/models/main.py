# -*- coding: utf-8 -*-
# * File Name : main.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 22-06-2012
# * Last Modified :
#
# * Project :
#
"""
    Main queries used in autonomie
    Allows to handle caching at function level (not at sqla level)
"""

from autonomie.models.model import Invoice
from autonomie.models.model import CancelInvoice
from autonomie.models.model import ManualInvoice

def get_next_officialNumber(dbsession):
    """
        Return the next available official number
    """
    a = Invoice.get_officialNumber(dbsession).first()[0]
    b = ManualInvoice.get_officialNumber(dbsession).first()[0]
    c = CancelInvoice.get_officialNumber(dbsession).first()[0]
    if not a:
        a = 0
    if not b:
        b = 0
    if not c:
        c = 0
    next_ = max(a,b,c) + 1
    return int(next_)
