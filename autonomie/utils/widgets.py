# -*- coding: utf-8 -*-
# * File Name : widgets.py
#
# * Copyright (C) 2010 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 19-10-2011
# * Last Modified : ven. 15 juin 2012 14:04:23 CEST
#
# * Project : autonomie
#
"""
    Widget library
"""
import cgi
import urllib
import logging

from mako.template import Template

from pyramid.renderers import render
from pyramid.security import has_permission

from colander import null

from deform.widget import Widget as DeformWidget

from pkg_resources import resource_filename

from autonomie.utils.pdf import render_html

log = logging.getLogger(__file__)

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

class DisabledInput(DeformWidget):
    """
        A non editable input
    """
    template = "autonomie:deform_templates/disabledinput.mako"
    def serialize(self, field, cstruct=None, readonly=True):
        if cstruct is null:
            cstruct = u''
        quoted = cgi.escape(cstruct, quote='"')
        params = {'name': field.name, 'value':quoted}
        return render(self.template, params)

    def deserialize(self, field, pstruct):
        return pstruct

class Widget(object):
    """
        Base widget
    """
    template = None
    def render(self, request):
        """
            return an html output of the widget
        """
        return render_html( request, self.template, {'elem':self})

class PermWidget(object):
    """
        widget with permission
    """
    def set_special_perm_func(self, func):
        """
            Allows to insert a specific permission function
        """
        self.special_perm_func = func

    def permitted(self, context, request):
        """
            Return True if the user has the right to access the destination
        """
        right = has_permission(self.perm, context, request)

        if right and hasattr(self, "special_perm_func"):
            return self.special_perm_func(context, request)
        else:
            return right

class StaticWidget(PermWidget):
    """
        Static Html widget with permission management
    """
    def __init__(self, html):
        self.html = html

    def render(self, request):
        return self.html

class Link(Widget, PermWidget):
    template = None

class JsLink(Link):
    """
        Simple Javascript Link
    """
    template = "base/jsbutton.mako"
    def __init__(self, label, perm, css="", js=None, title=None, icon=""):
        self.label = label
        self.perm = perm
        self.js = js
        if title:
            self.title = title
        else:
            self.title = self.label
        self.css = css
        self.icon = icon

    def onclick(self):
        """
            Return the onclick behaviour
        """
        return self.js

class ViewLink(Link):

    template = "base/button.mako"

    def __init__(self, label, perm, path=None, css="", js=None, title=None,
            icon="", **kw):
        self.label = label
        self.perm = perm
        self.path = path
        self.js = js
        if title:
            self.title = title
        else:
            self.title = self.label
        self.url_kw = kw
        self.css = css
        self.icon = icon

    def url(self, request):
        """
            Returns the button's url
        """
        if self.path:
            return request.route_path(self.path, **self.url_kw)
        else:
            return "#{0}".format(self.perm)

    def onclick(self):
        """
            return the onclick attribute
        """
        return self.js

    def selected(self, request):
        """
            Return True if the button is active
        """
        log.debug(request.current_route_path())
        log.debug(request.current_route_url())
        log.debug(request.path_qs)
        cur_path = request.current_route_path()
        if request.GET.has_key('action'):
            cur_path += "?action=%s" % request.GET['action']
        return urllib.unquote(cur_path) == self.url(request)

class ItemActionLink(ViewLink):
    """
        Action button used in item list
    """
    template = "base/itemactionlink.mako"
    def url(self, context, request):
        """
            Returns the url associated with current btn
        """
        return request.route_path(self.path,
                                  id=context.id,
                                  **self.url_kw)

    def render(self, request, item):
        return render_html( request, self.template, {'elem':self, 'item':item})


class ToggleLink(Link):
    template = "base/togglelink.mako"
    def __init__(self, label, perm, target, title=None, css="", icon=""):
        self.label = label
        self.perm = perm
        self.target = target
        self.title = title or label
        self.css = css
        self.icon = icon

class SearchForm(Widget):
    template = "base/searchform.mako"

    def __init__(self, helptext=u"", submit=u"Rechercher", id_="search_form"):
        self.helptext = helptext
        self.submit_text = submit
        self.id_ = id_
        self.widgets = []

    def insert(self, widget):
        """
            Insert elements in the form before the main ones
        """
        self.widgets.append(widget)

class ActionMenu(Widget):
    """
        Represent the ActionMenu
    """
    template = "base/actionmenu.mako"

    def __init__(self):
        self.items = []

    def add(self, item):
        """
            Add an item to the menu
        """
        self.items.append(item)
