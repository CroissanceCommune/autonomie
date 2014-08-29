# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2014 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
"""
Main deferreds functions used in autonomie
"""
import colander
import calendar
import datetime
import deform

from autonomie.utils.fileupload import FileTempStore

from autonomie.views.forms import widgets as custom_widgets


TEMPLATES_PATH = "autonomie:deform_templates/"


MAIL_ERROR_MESSAGE = u"Veuillez entrer une adresse e-mail valide"


@colander.deferred
def deferred_today(node, kw):
    """
        return a deferred value for "today"
    """
    return datetime.date.today()


@colander.deferred
def deferred_now(node, kw):
    """
    Return a deferred datetime value for now
    """
    return datetime.datetime.now()


@colander.deferred
def deferred_current_user_id(node, kw):
    """
        Return a deferred for the current user
    """
    return kw['request'].user.id


def get_date_input(**kw):
    """
    Return a date input displaying a french user friendly format
    """
    date_input = custom_widgets.CustomDateInputWidget(**kw)
    return date_input


def get_datetime_input(**kw):
    """
    Return a datetime input displaying a french user friendly format
    """
    datetime_input = custom_widgets.CustomDateTimeInputWidget(**kw)
    return datetime_input


def today_node(**kw):
    """
    Return a schema node for date selection, defaulted to today
    """
    if not "default" in kw:
        kw['default'] = deferred_today
    widget_options = kw.pop('widget_options', {})
    return colander.SchemaNode(
            colander.Date(),
            widget=get_date_input(**widget_options),
            **kw)


def now_node(**kw):
    """
    Return a schema node for time selection, defaulted to "now"
    """
    if not "default" in kw:
        kw['default'] = deferred_now
    return colander.SchemaNode(
        colander.DateTime(default_tzinfo=None),
        widget=get_datetime_input(),
        **kw)


def come_from_node(**kw):
    """
    Return a form node for storing the come_from page url
    """
    if not "missing" in kw:
        kw["missing"] = ""
    return colander.SchemaNode(
            colander.String(),
            widget=deform.widget.HiddenWidget(),
            **kw
            )


def textarea_node(**kw):
    """
    Return a node for storing Text objects
    """
    css_class = kw.pop('css_class', None) or 'span10'
    if kw.pop('richwidget', None):
        wid = deform.widget.RichTextWidget(css_class=css_class, theme="advanced")
    else:
        wid = deform.widget.TextAreaWidget(css_class=css_class)
    return colander.SchemaNode(
            colander.String(),
            widget=wid,
            **kw
            )


@colander.deferred
def default_year(node, kw):
    return datetime.date.today().year


def get_year_select_deferred(query_func, default_val=None):
    """
    return a deferred widget for year selection
    :param query_func: the query function returning a list of years
    """
    @colander.deferred
    def deferred_widget(node, kw):
        years = query_func()
        values = zip(years, years)
        if default_val is not None:
            values.insert(0, default_val)
        return deform.widget.SelectWidget(values=values,
                    css_class='input-small')
    return deferred_widget


def year_select_node(query_func, **kw):
    """
    Return a year select node with defaults and missing values

    :param query_func: a function to call that return the years we want to
        display
    """
    title = kw.pop('title', u"")
    query_func = kw['query_func']
    missing = kw.pop('missing', default_year)
    widget_options = kw.pop('widget_options', {})
    default_val = widget_options.get('default_val')
    return colander.SchemaNode(
        colander.Integer(),
        widget=get_year_select_deferred(query_func, default_val),
        default=default_year,
        missing=missing,
        title=title,
        **kw
        )


@colander.deferred
def default_month(node, kw):
    return datetime.date.today().month


def get_month_options():
    return [(index, calendar.month_name[index].decode('utf8')) \
            for index in range(1, 13)]


def get_month_select_widget(widget_options):
    """
    Return a select widget for month selection
    """
    options = get_month_options()
    default_val = widget_options.get('default_val')
    if default_val is not None:
        options.insert(0, default_val)
    return deform.widget.SelectWidget(values=options,
                    css_class='input-small')


def month_select_node(**kw):
    """
    Return a select widget for month selection
    """
    title = kw.pop('title', u"")
    default = kw.pop('default', default_month)
    missing = kw.pop('missing', default_month)
    widget_options = kw.pop('widget_options', {})
    return colander.SchemaNode(
            colander.Integer(),
            widget=get_month_select_widget(widget_options),
            default=default,
            missing=missing,
            title=title,
            **kw
            )


def mail_node(**kw):
    """
        Return a generic customized mail input field
    """
    title = kw.pop('title', None) or u"Adresse e-mail"
    return colander.SchemaNode(
        colander.String(),
        title=title,
        validator=colander.Email(MAIL_ERROR_MESSAGE),
        **kw)


def id_node():
    """
    Return a node for id recording (usefull in edition forms for retrieving
    original objects)
    """
    return colander.SchemaNode(
        colander.Integer(),
        widget=deform.widget.HiddenWidget(),
        missing=0,
        )


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
    return deform.widget.FileUploadWidget(tmpstore,
                template=TEMPLATES_PATH + "fileupload.mako")
