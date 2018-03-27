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
    Form schemas for commercial handling
"""
import datetime
import colander
from deform import widget

from autonomie.models.task import invoice
from autonomie import forms
from .custom_types import AmountType


def get_years(kw):
    years = invoice.get_invoice_years(kw)
    next_year = datetime.date.today().year + 1
    if next_year not in years:
        years.append(next_year)
    return years


class CommercialFormSchema(colander.MappingSchema):
    year = forms.year_select_node(query_func=get_years)


class CommercialSetFormSchema(colander.MappingSchema):
    month = colander.SchemaNode(
        colander.Integer(),
        widget=widget.HiddenWidget(),
        title=u'',
        validator=colander.Range(1,12),
    )
    value = colander.SchemaNode(
        AmountType(5),
        title=u"CA prévisionnel"
    )
    comment = forms.textarea_node(
        title=u"Commentaire",
        missing=u""
    )
