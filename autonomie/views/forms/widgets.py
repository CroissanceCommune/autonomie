# -*- coding: utf-8 -*-
# * File Name :
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
# * Project :
#
"""
    Specific tools for handling widgets
"""
import os
import cgi
import logging
import colander

from deform import widget
from deform_bootstrap.widget import ChosenSingleWidget
from pyramid.renderers import render

from autonomie.utils.fileupload import FileTempStore

log = logging.getLogger(__name__)
MAIL_ERROR_MESSAGE = u"Veuillez entrer une adresse e-mail valide"

class DisabledInput(widget.Widget):
    """
        A non editable input
    """
    template = "autonomie:deform_templates/disabledinput.mako"
    def serialize(self, field, cstruct=None, readonly=True):
        if cstruct is colander.null:
            cstruct = u''
        quoted = cgi.escape(cstruct, quote='"')
        params = {'name': field.name, 'value':quoted}
        return render(self.template, params)

    def deserialize(self, field, pstruct):
        return pstruct

def get_mail_input(missing=None):
    """
        Return a generic customized mail input field
    """
    return colander.SchemaNode(colander.String(),
                            title="Adresse e-mail",
                            validator=colander.Email(MAIL_ERROR_MESSAGE),
                            missing=missing
                            )
def get_date_input(**kw):
    """
        Return a date input displaying a french user friendly format
    """
    date_input = widget.DateInputWidget(**kw)
    date_input.options['dateFormat'] = 'dd/mm/yy'
    return date_input

def deferred_upload_widget(path):
    """
        return a deferred fileupload widget
    """
    @colander.deferred
    def configured_widget(node, kw):
        """
            returns a already pre-configured upload widget
        """
        session = kw['session']
        root_path = kw['rootpath']
        root_url = kw['rooturl']
        # path becomes : /assets/company_id/header (or logo)
        store_url = os.path.join(root_url, path)
        store_directory = os.path.join(root_path, path)
        tmpstore = FileTempStore(session, store_directory, store_url)
        return widget.FileUploadWidget(tmpstore,
                    template="autonomie:deform_templates/fileupload.mako")
    return configured_widget

@colander.deferred
def deferred_edit_widget(node, kw):
    """
        Dynamic assigned widget
        returns a text widget disabled if edit is True in schema binding
    """
    if kw.get('edit'):
        wid = DisabledInput()
    else:
        wid = widget.TextInputWidget()
    return wid

@colander.deferred
def deferred_autocomplete_widget(node, kw):
    """
        Dynamically assign a autocomplete single select widget
    """
    choices = kw.get('choices')
    if choices:
        wid = ChosenSingleWidget(values=choices)
    else:
        wid = widget.TextInputWidget()
    return wid

