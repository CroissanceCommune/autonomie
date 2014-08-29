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
    MultiRenderer tools to allow multiple renderers to be used with deform
"""
import logging
import datetime
import colander
import os

from pkg_resources import resource_filename

from pyramid.renderers import render
from pyramid.renderers import JSON
from pyramid.threadlocal import get_current_request

from deform.schema import default_widget_makers as defaults
from deform.form import Form
from deform.template import ZPTRendererFactory

from autonomie.i18n import translate
from autonomie import deform_extend


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
            if "request" not in kw:
                kw['request'] = get_current_request()
            return self.default_renderer(template_name, **kw)
        else:
            return render(template_name, kw)


def set_deform_renderer():
    """
        Returns a deform renderer allowing translation and multi-rendering
    """
    deform_template_dirs = (
        resource_filename('autonomie', 'templates/deform'),
        resource_filename('deform_bootstrap', 'templates/'),
        resource_filename('deform', 'templates/'),
        )

    renderer = MultiRendererFactory(search_path=deform_template_dirs,
                                    translator=translate)
    Form.default_renderer = renderer


def set_default_widgets():
    """
    Set custom date and datetime input widgets for a better user-experience
    """
    defaults[colander.DateTime] = deform_extend.CustomDateTimeInputWidget
    defaults[colander.Date] = deform_extend.CustomDateInputWidget


def set_json_renderer(config):
    """
        Customize json renderer to allow datetime rendering
    """
    json_renderer = JSON()
    def toisoformat(obj, request):
        return obj.isoformat()
    json_renderer.add_adapter(datetime.datetime, toisoformat)
    json_renderer.add_adapter(datetime.date, toisoformat)
    json_renderer.add_adapter(colander._null, lambda _,r:"null")
    config.add_renderer('json', json_renderer)
    return config
