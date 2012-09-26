# -*- coding: utf-8 -*-
# * File Name : renderer.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 09-07-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    MultiRenderer tools to allow multiple renderers to be used with deform
"""
import logging
import os

from pkg_resources import resource_filename

from pyramid.renderers import render

from deform.form import Form
from deform.template import ZPTRendererFactory

from autonomie.i18n import translate

log = logging.getLogger(__name__)


class MultiRendererFactory(object):
    """
        Multi renderer, allows rendering deform widgets
        in multiple formats
        chameleon by default and mako if not
    """
    def __init__(self,
                    search_path,
                    auto_reload=True,
                    translator=None):
        #FIXME : auto_reload should be retrived from inifile
        self.default_renderer = ZPTRendererFactory(
                                search_path=search_path,
                                auto_reload=auto_reload,
                                encoding="utf-8",
                                translator=translator)

    def __call__(self, template_name, **kw):
        """
            Launched by the client library
        """
        return self.load(template_name, **kw)

    def load(self, template_name, **kw):
        """
            Load the appropriate engine
            chameleon by default mako if not
        """
        if os.path.splitext(template_name)[1] == "":
            return self.default_renderer(template_name, **kw)
        else:
            return render(template_name, kw)


def set_deform_renderer():
    """
        Returns a deform renderer allowing translation and multi-rendering
    """
    deform_template_dirs = (
        resource_filename('deform_bootstrap', 'templates/'),
        resource_filename('deform', 'templates/'),
        )

    renderer = MultiRendererFactory(search_path=deform_template_dirs,
                                    translator=translate)
    Form.default_renderer = renderer
