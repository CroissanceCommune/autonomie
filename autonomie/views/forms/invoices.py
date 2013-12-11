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
    form schemas for invoices related views
"""
from datetime import date
import colander

from autonomie.views.forms.lists import BaseListsSchema
from autonomie.views.forms.widgets import (
        deferred_year_select_widget,
        )


STATUS_OPTIONS = ((u"Toutes les factures", "both"),
                  (u"Les factures payées", "paid"),
                  (u"Seulement les impayés", "notpaid"))

@colander.deferred
def default_year(node, kw):
    return date.today().year

class InvoicesListSchema(BaseListsSchema):
    # We override the search param, it needs to be an integer in our case
    # (officialNumber)
#    search = colander.SchemaNode(colander.Integer(), missing=None)
    status = colander.SchemaNode(colander.String(),
            validator=colander.OneOf([s[1] for s in STATUS_OPTIONS]),
            missing='both')
    year = colander.SchemaNode(colander.Integer(), missing=default_year)
    customer_id = colander.SchemaNode(colander.Integer(), missing=-1)
    company_id = colander.SchemaNode(colander.Integer(), missing=-1)


def range_validator(form, value):
    """
        Validate that end is higher or equal than start
    """
    if value['end'] > 0 and value['start'] > value['end']:
        exc = colander.Invalid(form,
             u"Le numéro de début doit être plus petit ou égal à celui de fin")
        exc['start'] = u"Doit être inférieur au numéro de fin"
        raise exc


class InvoicesPdfExport(colander.MappingSchema):
    """
        Schema for invoice bulk export
    """
    year = colander.SchemaNode(
            colander.Integer(),
            title=u"Année comptable",
            widget=deferred_year_select_widget,
            missing=default_year,
            default=default_year,
            )
    start = colander.SchemaNode(
            colander.Integer(),
            title=u"Numéro de début",
            description=u"Numéro à partir duquel exporter",
            )
    end = colander.SchemaNode(
            colander.Integer(),
            title=u"Numéro de fin",
            description=u"Numéro jusqu'auquel exporter \
(dernier document si vide)",
            missing=-1,
            )

pdfexportSchema = InvoicesPdfExport(
        title=u"Exporter un ensemble de factures dans un fichier pdf",
        validator=range_validator)
