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
    Specific tools for handling widgets
"""
import cgi
import logging
import json
import colander
from datetime import date

from beaker.cache import cache_region
from sqlalchemy import distinct
from deform.compat import url_quote
from deform.compat import string_types
from deform.i18n import _
from deform import widget
from translationstring import TranslationString

from deform_bootstrap.widget import ChosenSingleWidget
from pyramid.renderers import render

from autonomie.utils.fileupload import FileTempStore
from autonomie.models.task import Invoice


log = logging.getLogger(__name__)


class DisabledInput(widget.Widget):
    """
        A non editable input
    """
    template = "autonomie:deform_templates/disabledinput.mako"

    def serialize(self, field, cstruct=None, readonly=True):
        if cstruct is colander.null:
            cstruct = u''
        quoted = cgi.escape(cstruct, quote='"')
        params = {'name': field.name, 'value': quoted}
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
    requirements = (('jqueryui', None), )
    default_options = (('dateFormat', 'dd/mm/yy'),)

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


class CustomDateTimeInputWidget(CustomDateInputWidget):
    """
    Renders a datetime picker widget.

    The default rendering is as a native HTML5 datetime  input widget,
    falling back to jQuery UI date picker with a JQuery Timepicker add-on
    (http://trentrichardson.com/examples/timepicker/).

    Used for ``colander.DateTime`` schema nodes.

    **Attributes/Arguments**

    options
        A dictionary of options that's passed to the datetimepicker.

    size
        The size, in columns, of the text input field.  Defaults to
        ``None``, meaning that the ``size`` is not included in the
        widget output (uses browser default size).

    style
        A string that will be placed literally in a ``style`` attribute on
        the text input tag.  For example, 'width:150px;'.  Default: ``None``,
        meaning no style attribute will be added to the input tag.

    template
        The template name used to render the widget.  Default:
        ``dateinput``.

    readonly_template
        The template name used to render the widget in read-only mode.
        Default: ``readonly/textinput``.
    """
    template = 'autonomie:deform_templates/datetimeinput.pt'
    readonly_template = 'readonly/textinput'
    type_name = 'datetime'
    size = None
    style = None
    requirements = ( ('modernizr', None), ('jqueryui', None),
                     ('datetimepicker', None), )
    default_options = (('dateFormat', 'dd/mm/yy'),
                       ('timeFormat', 'hh:mm:ss'),
                       ('separator', ' '))

    def serialize(self, field, cstruct, readonly=False):
        if cstruct in (colander.null, None):
            cstruct = ''
        if cstruct:
            parsed = colander.iso8601.ISO8601_REGEX.match(cstruct)
            if parsed: # strip timezone if it's there
                timezone = parsed.groupdict()['timezone']
                if timezone and cstruct.endswith(timezone):
                    cstruct = cstruct[:-len(timezone)]
        options = self.options
        options['altFormat'] = 'yy-mm-dd'
        separator = options.get('separator', ' ')
        options = json.dumps(options)
        cstruct = separator.join(cstruct.split('T'))
        template = readonly and self.readonly_template or self.template
        return field.renderer(
            template,
            field=field,
            cstruct=cstruct,
            options=options)

    def deserialize(self, field, pstruct):
        datetime_data = pstruct.get('datetime', colander.null)
        if datetime_data in ('', colander.null):
            return colander.null
        return datetime_data.replace(self.options['separator'], 'T')


class CustomSequenceWidget(widget.SequenceWidget):
    """
        See : https://github.com/Pylons/deform/pull/79
    """
    def prototype(self, field):
        """
            Build the prototype of a serialized sequence item
        """
        # we clone the item field to bump the oid (for easier
        # automated testing; finding last node)
        item_field = field.children[0].clone()
        proto = field.renderer(self.item_template, field=item_field,
                            cstruct=item_field.schema.serialize(colander.null),
                                                             parent=field)
        if isinstance(proto, string_types):
            proto = proto.encode('utf-8')
        proto = url_quote(proto)
        return proto

    def serialize(self, field, cstruct, readonly=False):
        """
            Overrided serialize method
        """
        if (self.render_initial_item and self.min_len is None):
            # This is for compat only: ``render_initial_item=True`` should
            # now be spelled as ``min_len = 1``
            self.min_len = 1

        if cstruct in (colander.null, None):
            if self.min_len is not None:
                cstruct = [colander.null] * self.min_len
            else:
                cstruct = []

        cstructlen = len(cstruct)

        if self.min_len is not None and (cstructlen < self.min_len):
            cstruct = list(cstruct) + \
                    ([colander.null] * (self.min_len - cstructlen))

        item_field = field.children[0]

        if getattr(field, 'sequence_fields', None):
            # this serialization is being performed as a result of a
            # validation failure (``deserialize`` was previously run)
            assert(len(cstruct) == len(field.sequence_fields))
            subfields = list(zip(cstruct, field.sequence_fields))
        else:
            # this serialization is being performed as a result of a
            # first-time rendering
            subfields = []
            for val in cstruct:
                if val is colander.null:
                    val = item_field.schema.serialize(val)
                subfields.append((val, item_field.clone()))

        template = readonly and self.readonly_template or self.template
        translate = field.translate
        add_template_mapping = dict(
            subitem_title=translate(item_field.title),
            subitem_description=translate(item_field.description),
            subitem_name=item_field.name)
        if isinstance(self.add_subitem_text_template, TranslationString):
            add_subitem_text = self.add_subitem_text_template % \
                add_template_mapping
        else:
            add_subitem_text = _(self.add_subitem_text_template,
                                 mapping=add_template_mapping)
        return field.renderer(template,
                              field=field,
                              cstruct=cstruct,
                              subfields=subfields,
                              item_field=item_field,
                              add_subitem_text=add_subitem_text)


class CustomChosenOptGroupWidget(widget.SelectWidget):
    """
    Customize the chosenselectwidget to be able to provide a default value for
    unselection
    """
    template = 'autonomie:deform_templates/chosen_optgroup.pt'


def get_fileupload_widget(store_url, store_path, session, \
        default_filename=None, filters=None):
    """
        return a file upload widget
    """
    tmpstore = FileTempStore(
            session,
            store_path,
            store_url,
            default_filename=default_filename,
            filters=filters,
            )
    return widget.FileUploadWidget(tmpstore,
                template="autonomie:deform_templates/fileupload.mako")

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


def get_years(dbsession):
    """
        Return a cached query for the available years
    """
    @cache_region("long_term", "taskdates")
    def taskyears():
        """
            return the distinct financial years available in the database
        """
        years = dbsession.query(distinct(Invoice.financial_year))\
                .order_by(Invoice.financial_year).all()
        years = [year[0] for year in years]
        now = date.today().year
        if now not in years:
            years.append(now)
        return years
    return taskyears()


@colander.deferred
def deferred_year_select_widget(node, kw):
    """
        Return a deferred year select widget
    """
    years = get_years(kw['request'].dbsession)
    return widget.SelectWidget(values=zip(years, years),
                css_class='input-small')


@colander.deferred
def deferred_today(node, kw):
    """
        return a deferred value for "today"
    """
    return date.today()
