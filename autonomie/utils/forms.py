# -*- coding: utf-8 -*-
# * File Name : formutils.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 31-01-2012
# * Last Modified : lun. 09 juil. 2012 22:55:35 CEST
#
# * Project : autonomie
#
"""
    Deform utility wrappers
"""
import logging
import colander

from deform.form import Form


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

