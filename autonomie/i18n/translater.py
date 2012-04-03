# -*- coding: utf-8 -*-
# * File Name : translater.py
#
# * Copyright (C) 2010 Gaston TJEBBES <tonthon21@gmail.com>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 18-02-2012
# * Last Modified : jeu. 29 mars 2012 12:32:47 CEST
#
# * Project : Autonomie
#
import deform
from pkg_resources import resource_filename
from pyramid.i18n import TranslationStringFactory
from pyramid.i18n import get_localizer
from pyramid.threadlocal import get_current_request

translater = TranslationStringFactory('autonomie')
def _(request, string, mapping=None):
    ts = translater(string, mapping)
    localizer = get_localizer(request)
    return localizer.translate(ts)

def get_deform_renderer_opts():
    """
        return the deform renderer with i18n support
    """
    factory = TranslationStringFactory('deform')
    deform_template_dir = (
            resource_filename('deform_bootstrap', 'templates/'),
            resource_filename('deform', 'templates/'),)
    def translator(term):
        ts = factory(term)
        localizer = get_localizer(get_current_request())
        return localizer.translate(ts)
    return deform_template_dir, translator

def set_deform_renderer():
    """
        Returns a deform renderer allowing translation
    """
    deform_template_dir, translator = get_deform_renderer_opts()
    deform.Form.set_zpt_renderer(deform_template_dir, translator=translator)
