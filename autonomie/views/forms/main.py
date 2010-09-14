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
from datetime import date
from deform import widget
from deform_bootstrap.widget import ChosenSingleWidget

from autonomie.models import user
from autonomie.views import render_api

from autonomie.views.forms import widgets as custom_widgets


def get_users_options(roles=None):
    """
    Return the list of active users from the database formatted as choices:
        [(user_id, user_label)...]

    :param role: roles of the users we want
        default:  all
        values : ('contractor', 'manager', 'admin'))
    """
    if roles and not hasattr(roles, "__iter__"):
        roles = [roles]
    if roles:
        query = user.get_user_by_roles(roles)
    else:
        query = user.User.query()
    return [(unicode(u.id), render_api.format_account(u)) for u in query]


def get_deferred_user_choice(roles=None):
    """
        Return a colander deferred for users selection options
    """
    @colander.deferred
    def user_select(node, kw):
        """
            Return a user select widget
        """
        choices = get_users_options(roles)
        return ChosenSingleWidget(values=choices)
    return user_select


@colander.deferred
def deferred_autocomplete_widget(node, kw):
    """
        Dynamically assign a autocomplete single select widget
    """
    choices = kw.get('choices')
    if choices:
        wid = widget.ChosenSingleWidget(values=choices)
    else:
        wid = widget.TextInputWidget()
    return wid


@colander.deferred
def deferred_today(node, kw):
    """
        return a deferred value for "today"
    """
    return date.today()


def get_date_input(**kw):
    """
    Return a date input displaying a french user friendly format
    #FIXME : check the current deform we use to see if it's fun to use the
    browser's date widget
    """
    date_input = custom_widgets.CustomDateInputWidget(**kw)
    date_input.options['dateFormat'] = 'dd/mm/yy'
    return date_input

def user_node(roles=None, **kw):
    """
    Return a schema node for user selection
    roles: allow to restrict the selection to the given roles
        (to select between admin, contractor and manager)
    """
    return colander.SchemaNode(
            colander.Integer(),
            widget=get_deferred_user_choice(roles),
            **kw
            )


def today_node(**kw):
    """
    Return a schema node for date selection, defaulted to today
    """
    if not "default" in kw:
        kw['default'] = deferred_today
    return colander.SchemaNode(
            colander.Date(),
            widget=get_date_input(),
            **kw)

def come_from_node(**kw):
    """
    Return a form node for storing the come_from page url
    """
    if not "missing" in kw:
        kw["missing"] = ""
    return colander.SchemaNode(
            colander.String(),
            widget=widget.HiddenWidget(),
            **kw
            )


def textarea_node(**kw):
    """
    Return a node for storing Text objects
    """
    css_class = kw.pop('css_class', None) or 'span10'
    return colander.SchemaNode(
            colander.String(),
            widget=widget.TextAreaWidget(css_class=css_class),
            **kw
            )
