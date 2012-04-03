# -*- coding: utf-8 -*-
# * File Name : widgets.py
#
# * Copyright (C) 2010 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 19-10-2011
# * Last Modified : lun. 26 mars 2012 17:55:45 CEST
#
# * Project : autonomie
#
"""
    Widget library
"""
import cgi

from mako.template import Template

from pyramid.renderers import render

from colander import null

from deform.widget import Widget

from pkg_resources import resource_filename

def mako_renderer(tmpl, **kw):
    """
        A mako renderer to be used inside deform special widgets
    """
    template = Template(resource_filename(__name__, tmpl))
    return template.render(**kw)

class Link:
    """
        Simple object to build a link
    """
    def __init__(self, href="#", label=None, title=None, icon=None):
        self.href = href
        self.label = label
        self.title = title
        self.icon = icon

class DisabledInput(Widget):
    """
        A non editable input
    """
    template = "autonomie:deform_templates/disabledinput.mako"
    def serialize(self, field, cstruct=None, readonly=True):
        if cstruct is null:
            cstruct = u''
        quoted = cgi.escape(cstruct, quote='"')
        name = field.name
        params = {'name': field.name, 'value':quoted}
        return render(self.template, params)

    def deserialize(self, field, pstruct):
        return pstruct
