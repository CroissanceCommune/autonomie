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
    Widget library
"""
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


class Widget(object):
    """
        Base widget
    """
    name = None
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
        return render_html(request, self.template, {'elem': self})


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

class ViewLink(Widget, PermWidget):

    template = "base/button.mako"

    def __init__(self, label, perm=None, path=None, css="", js=None,
                 title=None, icon="", request=None, confirm=None, **kw):
        self.label = label
        self.perm = perm
        self.path = path
        if confirm:
            self.js = u"return confirm('{0}')".format(
                                        confirm.replace("'", "\\'"))
        else:
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
        if 'action' in request.GET:
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
        return render_html(request, self.template, {'elem': self,
                                                    'item': item})



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
    css = "btn btn-primary"
    js = None
    type_ = 'submit'
    icon = None
    disabled = False

    def __init__(self, label, value, title=None,
                            request=None, confirm=None, name="submit"):
        self.label = label
        self.value = value
        self.name = name or "submit"
        self.title = title or self.label
        if confirm:
            self.js = u"return confirm('{0}')".format(
                                        confirm.replace("'", "\\'"))
        if request:
            self.request = request


class ToggleLink(Widget, PermWidget):
    template = "base/togglelink.mako"

    def __init__(self, label, perm=None, target=None, title=None, css="",
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
        self.defaults = {}

    def set_defaults(self, defaults):
        """
            stores default values for the form
        """
        self.defaults = defaults

    def insert(self, widget):
        """
            Insert elements in the form before the main ones
        """
        self.widgets.append(widget)


class ButtonLink(Widget):

    template = "base/button.mako"

    def __init__(self, label, path, js=None, title=None,
                 icon="", css='', **kw):
        self.label = label
        self.path = path
        self.js = js
        self.title = title or self.label
        self.icon = icon
        self.css = css
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
        if 'action' in request.GET:
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
        return factory(
                label,
                js=self._get_js_link(),
                path="popup-%s" % self.name,
                **kw)

    def _get_js_link(self):
        return u"$('#{0}').dialog('open');".format(self.name)


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

    def void(self):
        """
            Return True if the menu is void
        """
        return not bool(len(self.items))


class ActionMenu(Menu):
    """
        Represent the ActionMenu
    """
    template = "base/actionmenu.mako"
