# -*- coding: utf-8 -*-
# * File Name : formutils.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 31-01-2012
# * Last Modified : mar. 17 avril 2012 17:32:24 CEST
#
# * Project : autonomie
#
"""
    Deform utility wrappers
"""
import os
import logging
import colander

from pkg_resources import resource_filename

from pyramid.renderers import render
from deform.form import Form
from deform.template import ZPTRendererFactory

from autonomie.i18n import translate

log = logging.getLogger(__name__)

def merge_session_with_post(session, app_struct):
    """
        Merge Deform validated datas with SQLAlchemy's objects
        Allow to spare some lines of assigning datas to the object
        before writing to database
    """
    for key, value in app_struct.items():
        setattr(session, key, value)
    return session

class XHttpForm(Form):
    """
        Extends deform form object to add deform.load javascript calls
        Note : it allows sendind deform forms with use_ajax=True
    """

    def __init__(self, *args, **kw):
        Form.__init__(self, *args, **kw)
        self.messages = []

    def add_message(self, message):
        """
            Add a message to the form
        """
        self.messages.append(message)

    def render_messages(self):
        """
            render messages
        """
        html = ''
        for i in self.messages:
            html += u"<script>alert('{0}');</script>".format(i)
        self.reset_messages()
        return html

    def reset_messages(self):
        """
            remove trailing messages
        """
        self.messages = []

    def render(self, appstruct=colander.null, readonly=False):
        """
            Hack the render method to add the missing js tag
        """
        log.debug(self.messages)
        html = self.render_messages()
        html += Form.render(self, appstruct, readonly)
        html += "<script>deform.load()</script>"
        return html

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
        Returns a deform renderer allowing translation
    """
    deform_template_dirs = (
        resource_filename('deform_bootstrap', 'templates/'),
        resource_filename('deform', 'templates/'),
        )

    renderer = MultiRendererFactory(search_path=deform_template_dirs,
                                    translator=translate
                                    )
    Form.default_renderer = renderer

