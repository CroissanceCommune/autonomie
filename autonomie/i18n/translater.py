# -*- coding: utf-8 -*-
# * File Name : translater.py
#
# * Copyright (C) 2010 Gaston TJEBBES <tonthon21@gmail.com>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 18-02-2012
# * Last Modified : mar. 17 avril 2012 17:32:21 CEST
#
# * Project : Autonomie
#
"""
    Translation tools
"""
from pyramid.i18n import TranslationStringFactory
from pyramid.i18n import get_localizer
from pyramid.threadlocal import get_current_request

def translate(term):
    """
        String translator
        Allows string translation without having a request object available
        from deform rendering for example
    """
    tsf = TranslationStringFactory('deform')
    localizer = get_localizer(get_current_request())
    if not hasattr(term, 'interpolate'):
        term = tsf(term)
    return localizer.translate(term)
