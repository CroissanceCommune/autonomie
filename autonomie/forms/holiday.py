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
    form schemas for holiday declaration
"""
import colander
import logging

from deform import widget
from autonomie.forms.user import user_node

log = logging.getLogger(__name__)


def date_validator(form, value):
    if value['start_date'] >= value['end_date']:
        exc = colander.Invalid(form,
                    u"La date de début doit précéder la date de fin")
        exc['start_date'] = u"Doit précéder la date de fin"
        raise exc


class HolidaySchema(colander.MappingSchema):
    start_date = colander.SchemaNode(colander.Date(), title=u"Date de début")
    end_date = colander.SchemaNode(colander.Date(), title=u"Date de fin")


class HolidaysList(colander.SequenceSchema):
    holiday = HolidaySchema(title=u"Période", validator=date_validator)


class HolidaysSchema(colander.MappingSchema):
    holidays = HolidaysList(title=u"",
                widget=widget.SequenceWidget(min_len=1))


class SearchHolidaysSchema(colander.MappingSchema):
    start_date = colander.SchemaNode(colander.Date(), title=u"Date de début")
    end_date = colander.SchemaNode(colander.Date(), title=u"Date de fin")
    user_id = user_node(
        title=u"Entrepreneur",
        missing=colander.drop,
        widget_options={'default_option': ('', u"Tous")}
    )


searchSchema = SearchHolidaysSchema(
                        title=u"Rechercher les congés des entrepreneurs",
                        validator=date_validator)
