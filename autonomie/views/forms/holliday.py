# -*- coding: utf-8 -*-
# * File Name : holliday.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 22-06-2012
# * Last Modified :
#
# * Project :
#
"""
    form schemas for holliday declaration
"""
import colander
import logging

from deform import widget
from autonomie.utils.forms import deferred_autocomplete_widget
from autonomie.utils.forms import  get_date_input

log = logging.getLogger(__file__)

def date_validator(form, value):
    if value['start_date'] >= value['end_date']:
        exc = colander.Invalid(form,
                    u"La date de début doit précéder la date de fin")
        exc['start_date'] = u"Doit précéder la date de fin"
        raise exc

class HollidaySchema(colander.MappingSchema):
    start_date = colander.SchemaNode(colander.Date(), title=u"Date de début",
            widget=get_date_input())
    end_date = colander.SchemaNode(colander.Date(), title=u"Date de fin",
            widget=get_date_input())

class HollidaysList(colander.SequenceSchema):
    holliday = HollidaySchema(title=u"Période", validator=date_validator)

class HollidaysSchema(colander.MappingSchema):
    hollidays = HollidaysList(title=u"",
                widget=widget.SequenceWidget(min_len=1))

class SearchHollidaysSchema(colander.MappingSchema):
    start_date = colander.SchemaNode(colander.Date(), title=u"Date de début",
            widget=get_date_input())
    end_date = colander.SchemaNode(colander.Date(), title=u"Date de fin",
            widget=get_date_input())
    user_id = colander.SchemaNode(colander.Integer(), title=u"Entrepreneur",
                       widget=deferred_autocomplete_widget,
                       missing=None)

searchSchema = SearchHollidaysSchema(
                        title=u"Rechercher les congés des entrepreneurs",
                        validator=date_validator)

