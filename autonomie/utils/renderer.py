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
import deform

from autonomie_base.utils.renderers import (
    configure_export,
    set_json_renderer,
)
from pkg_resources import resource_filename

from deform.template import ZPTRendererFactory

from pyramid.threadlocal import get_current_request


logger = logging.getLogger(__name__)


class CustomRenderer(ZPTRendererFactory):
    """
    Custom renderer needed to ensure our buttons (see utils/widgets.py) can be
    added in the form actions list
    It adds the current request object to the rendering context
    """
    def __call__(self, template_name, **kw):
        if "request" not in kw:
            kw['request'] = get_current_request()
        return ZPTRendererFactory.__call__(self, template_name, **kw)


def get_search_path():
    """
    Add autonomie's deform custom templates to the loader
    """
    path = resource_filename('autonomie', 'templates/deform')
    return (path, deform.template.default_dir,)


def set_custom_form_renderer(config):
    """
    Uses an extended renderer that ensures the request object is on our form
    rendering context
    Code largely inspired from pyramid_deform/__init__.py
    """
    # Add translation directories
    config.add_translation_dirs('colander:locale', 'deform:locale')
    config.add_static_view(
        "static-deform",
        'deform:static',
        cache_max_age=3600
    )
    # Initialize the Renderer
    from pyramid_deform import translator
    renderer = CustomRenderer(get_search_path(), translator=translator)

    deform.form.Form.default_renderer = renderer


def customize_renderers(config):
    """
    Customize the different renderers
    """
    logger.debug(u"Setting renderers related hacks")
    # Json
    set_json_renderer(config)
    # deform
    set_custom_form_renderer(config)
    # Exporters
    configure_export()


def set_close_popup_response(request, message, refresh=True):
    """
    Write directly js code inside the request reponse's body to call popup close
    """
    refresh = refresh and 'true' or 'false'
    request.response.text = u"""<!DOCTYPE html>
    <html><head><title></title></head><body>
    <script type="text/javascript">
    opener.dismissPopup(window, {message: "%s", refresh: %s});
    </script></body></html>""" % (message, refresh)
    return request
