# -*- coding: utf-8 -*-
# * File Name : widgets.py
#
# * Copyright (C) 2010 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 19-10-2011
# * Last Modified : mar. 28 août 2012 15:03:38 CEST
#
# * Project : autonomie
#
"""
    Widget library
"""
import cgi
import urllib
import logging

from pkg_resources import resource_filename

from mako.template import Template
from pyramid.security import has_permission

from autonomie.utils.pdf import render_html

log = logging.getLogger(__name__)

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

class Widget(object):
    """
        Base widget
    """
    template = None
    request = None

    def set_template(self, template):
        """
            Change the template of the menu
        """
        self.template = template

    def render(self, request):
        """
            return an html output of the widget
        """
        request = self.request or request
        return render_html( request, self.template, {'elem':self})

class PermWidget(object):
    """
        widget with permission
    """
    perm = None
    def set_special_perm_func(self, func):
        """
            Allows to insert a specific permission function
        """
        self.special_perm_func = func

    def permitted(self, context, request):
        """
            Return True if the user has the right to access the destination
        """
        right = True
        if self.perm:
            right = has_permission(self.perm, context, request)
        if right and hasattr(self, "special_perm_func"):
            right = self.special_perm_func(context, request)
        return right

class StaticWidget(PermWidget):
    """
        Static Html widget with permission management
        @html : an html string (maybe you can use Webhelpers to build it)
        @perm: the permission needed to display this element
    """
    def __init__(self, html, perm=None):
        self.html = html
        self.perm = perm

    def render(self, request):
        """
            Return the html output
        """
        if self.permitted(request.context, request):
            return self.html
        else:
            return ""

class Link(Widget, PermWidget):
    template = None

class JsLink(Link):
    """
        Simple Javascript Link
    """
    template = "base/jsbutton.mako"
    def __init__(self, label, perm=None, css="", js=None, title=None, icon=""):
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

    def __init__(self, label, perm=None, path=None, css="", js=None, title=None,
            icon="", request=None, **kw):
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
        self.request = request

    def url(self, request):
        """
            Returns the button's url
        """
        request = self.request or request
        if self.path:
            return request.route_path(self.path, **self.url_kw)
        else:
            return u"#{0}".format(self.perm)

    def onclick(self):
        """
            return the onclick attribute
        """
        return self.js

    def selected(self, request):
        """
            Return True if the button is active
        """
        request = self.request or request
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

class Submit(Widget):
    """
        Submit Link used to be included in a form
        It's componed by :
        @label : the label of the button
        @perm : permission needed to display this button
        @value: value of the button
        @name : name of the button (the couple name=value is submitted)
        @title: title used onmouseover
        @css: css class string
        @_type: type of the button
    """
    template = "base/submit.mako"
    name = "submit"
    css = "btn btn-primary"
    js = None
    type_='submit'
    icon = None

    def __init__(self, label, value, title=None,
                            request=None, confirm=None):
        self.label = label
        self.value = value
        self.title = title or self.label
        if confirm:
            self.js = u"return confirm('{0}')".format(
                                        confirm.replace("'", "\\'"))
        if request:
            self.request = request

class ToggleLink(Link):
    template = "base/togglelink.mako"
    def __init__(self, label, perm=None, target=None, title=None, css="", \
                                                                icon=""):
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

class Menu(Widget):
    template = None
    def __init__(self, template=None, css=None):
        self.items = []
        if template:
            self.set_template(template)
        if css:
            self.css = css

    def add(self, item):
        """
            Add an item to the menu
        """
        self.items.append(item)

    def insert(self, item, index=0):
        """
            Insert an item in the menu
        """
        self.items.insert(index, item)

class ActionMenu(Menu):
    """
        Represent the ActionMenu
    """
    template = "base/actionmenu.mako"

class MenuDropDown(Menu, PermWidget):
    template = "base/dropdown.mako"
    def __init__(self, label, perm=None, title=None, template=None):
        Menu.__init__(self, template)
        self.label = label
        self.perm = perm
        self.title = title or label

class MainMenuItem(ViewLink):
    template = "base/mainmenu_item.mako"

class ButtonLink(Widget):

    template = "base/button.mako"

    def __init__(self, label, path, js=None, title=None, icon="", **kw):
        self.label = label
        self.path = path
        self.js = js
        self.title = title or self.label
        self.icon = icon
        self.url_kw = kw

    def url(self, request):
        """
            Returns the button's url
        """
        return request.route_path(self.path, **self.url_kw)

    def onclick(self):
        """
            return the onclick attribute
        """
        return self.js

    def selected(self, request):
        """
            Return True if the button is active
        """
        request = self.request or request
        cur_path = request.current_route_path()
        if request.GET.has_key('action'):
            cur_path += "?action=%s" % request.GET['action']
        return urllib.unquote(cur_path) == self.url(request)

class ButtonJsLink(ButtonLink):

    template = "base/button.mako"

    def url(self, request):
        return "#{0}".format(self.path)

    def selected(self, request):
        """
            return True if it's selected
        """
        return False

class PopUp(object):
    """
        A popup
    """
    def __init__(self, name, title, html):
        self.name = name
        self.title = title
        self.html = html

    def open_btn(self, label=None, factory=ButtonJsLink, **kw):
        label = label or self.title
        return factory(label, js=self._get_js_link(), path=self.name, **kw)

    def _get_js_link(self):
        return u"$('#{0}').dialog('open');".format(self.name)
