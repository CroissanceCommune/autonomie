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
import deform

from decimal import Decimal
from pkg_resources import resource_filename

from deform.template import ZPTRendererFactory

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Integer,
    Float,
)

from pyramid.renderers import JSON
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


def set_json_renderer(config):
    """
        Customize json renderer to allow datetime rendering
    """
    json_renderer = JSON()

    def toisoformat(obj, request):
        return obj.isoformat()

    json_renderer.add_adapter(datetime.datetime, toisoformat)
    json_renderer.add_adapter(datetime.date, toisoformat)
    json_renderer.add_adapter(colander._null, lambda _, r: "null")

    def decimal_to_num(obj, request):
        return float(obj)

    json_renderer.add_adapter(Decimal, decimal_to_num)

    config.add_renderer('json', json_renderer)
    return config


def set_export_formatters():
    """
    Globally set export formatters in the sqla_inspect registry
    """
    from sqla_inspect.export import FORMATTERS_REGISTRY
    from autonomie.views import render_api
    from autonomie.export.utils import format_boolean

#    FORMATTERS_REGISTRY.add_formatter(Date, render_api.format_date)
#    FORMATTERS_REGISTRY.add_formatter(DateTime, render_api.format_datetime)
    FORMATTERS_REGISTRY.add_formatter(Boolean, format_boolean)
    FORMATTERS_REGISTRY.add_formatter(Float, render_api.format_quantity)
    FORMATTERS_REGISTRY.add_formatter(Integer, render_api.format_quantity)


def set_export_blacklist():
    """
    Globally set an export blacklist
    """
    print("Setting blacklisted keys")
    from sqla_inspect.export import BLACKLISTED_KEYS

    BLACKLISTED_KEYS.extend([
        '_acl',
        'password',
        'parent_id',
        'parent',
        'type_',
        'children',
    ])


def set_xls_formats():
    """
    Globally set the xls formats by datatype
    """
    from sqla_inspect.excel import FORMAT_REGISTRY

    FORMAT_REGISTRY.add_item(Date, "dd/mm/yyyy")
    FORMAT_REGISTRY.add_item(DateTime, "dd/mm/yyyy hh:mm")


def set_custom_deform_js():
    from js import deform
    from autonomie.resources import custom_deform_js
    logger.debug(u"Overriding the default deform_js resource")
    deform.deform_js = custom_deform_js
    deform.resource_mapping['deform'] = [custom_deform_js]


def customize_renderers(config):
    """
    Customize the different renderers
    """
    # Json
    set_json_renderer(config)
    # deform
    set_custom_form_renderer(config)
    # Exporters
    set_export_formatters()
    set_export_blacklist()
    set_xls_formats()
    set_custom_deform_js()
