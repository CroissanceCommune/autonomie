# -*- coding: utf-8 -*-
# * File Name : translater.py
#
# * Copyright (C) 2010 Gaston TJEBBES <tonthon21@gmail.com>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 18-02-2012
# * Last Modified : ven. 13 avril 2012 23:11:45 CEST
#
# * Project : Autonomie
#
"""
    Translation tools
"""
import os

from deform.template import ZPTTemplateLoader
from deform import Form
from pkg_resources import resource_filename
from pyramid.i18n import TranslationStringFactory
from pyramid.i18n import get_localizer
from pyramid.threadlocal import get_current_request
from pyramid.renderers import render

translater = TranslationStringFactory('autonomie')
def _(request, string, mapping=None):
    ts = translater(string, mapping)
    localizer = get_localizer(request)
    return localizer.translate(ts)

deform_template_dirs = (
        resource_filename('deform_bootstrap', 'templates/'),
        resource_filename('deform', 'templates/'),
        )

def translator(term):
    """
        String translator
    """
    factory = TranslationStringFactory('deform')
    localizer = get_localizer(get_current_request())
    return localizer.translate(factory(term))

class MultiRendererFactory(object):
    """
        Multi renderer, allows rendering deform widgets
        in multiple formats
    """
    def __init__(self, search_path, auto_reload=True, debug=False,
                encoding='utf-8', translator=None):
        self.default_loader = ZPTTemplateLoader(
                            search_path=search_path,
                            auto_reload=auto_reload,
                            debug=debug,
                            encoding=encoding,
                            translate=translator)

    def __call__(self, template_name, **kw):
        """
            Launched by the client library
        """
        return self.load(template_name, **kw)

    def load(self, template_name, **kw):
        """
            Load the appropriate engine
        """
        if os.path.splitext(template_name)[1] == '':
            template_name += ".pt"

        if os.path.splitext(template_name)[1] == ".pt":
            return self.default_loader.load(template_name)(**kw)
        else:
            return render(template_name, kw)

def set_deform_renderer():
    """
        Returns a deform renderer allowing translation
    """
    renderer = MultiRendererFactory(deform_template_dirs)
    Form.set_default_renderer(renderer)

