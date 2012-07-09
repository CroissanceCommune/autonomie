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

class CustomDateInputWidget(widget.Widget):
    """

    Renders a JQuery UI date picker widget
    (http://jqueryui.com/demos/datepicker/).  Most useful when the
    schema node is a ``colander.Date`` object.
    alt Tag is used to allow full customization of the displayed input

    **Attributes/Arguments**

    size
        The size, in columns, of the text input field.  Defaults to
        ``None``, meaning that the ``size`` is not included in the
        widget output (uses browser default size).

    template
        The template name used to render the widget.  Default:
        ``dateinput``.

    options
        Options for configuring the widget (eg: date format)

    readonly_template
        The template name used to render the widget in read-only mode.
        Default: ``readonly/textinput``.
    """
    template = 'autonomie:deform_templates/dateinput.pt'
    readonly_template = 'readonly/textinput'
    size = None
    requirements = ( ('jqueryui', None), )
    default_options = (('dateFormat', 'yy-mm-dd'),)

    def __init__(self, *args, **kwargs):
        self.options = dict(self.default_options)
        widget.Widget.__init__(self, *args, **kwargs)

    def serialize(self, field, cstruct, readonly=False):
        if cstruct in (colander.null, None):
            cstruct = ''
        template = readonly and self.readonly_template or self.template
        options = self.options
        # Force iso format for colander compatibility
        options['altFormat'] = 'yy-mm-dd'
        return field.renderer(template,
                              field=field,
                              cstruct=cstruct,
                              options=self.options)

    def deserialize(self, field, pstruct):
        date = pstruct.get('date', colander.null)
        if date in ('', colander.null):
            return colander.null
        return date

def get_mail_input(missing=None):
    """
        Return a generic customized mail input field
    """
    return colander.SchemaNode(colander.String(),
                            title="Adresse e-mail",
                            validator=colander.Email(MAIL_ERROR_MESSAGE),
                            missing=missing)

def get_date_input(**kw):
    """
        Return a date input displaying a french user friendly format
    """
    date_input = CustomDateInputWidget(**kw)
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

def get_deferred_edit_widget(**options):
    """
        Return a deferred edit widget
    """
    @colander.deferred
    def deferred_edit_widget(node, kw):
        if kw.get('edit'):
            wid = DisabledInput()
        else:
            wid = widget.TextInputWidget(**options)
        return wid
    return deferred_edit_widget

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

