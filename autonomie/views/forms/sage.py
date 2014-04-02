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
    Form schemas for invoice exports
"""
from datetime import date
import colander
from autonomie.views.forms.widgets import (
        deferred_year_select_widget,
        )
from autonomie.views.forms import main


@colander.deferred
def default_year(node, kw):
    """
        Return the current year
    """
    return date.today().year


def date_validator(form, value):
    """
        Validate the period
    """
    if value['start_date'] > value['end_date']:
        exc = colander.Invalid(form,
                    u"La date de début doit précéder la date de fin")
        exc['start_date'] = u"Doit précéder la date de fin"
        raise exc


ExportedField = colander.SchemaNode(colander.Boolean(),
            title=u"Inclure les documents déjà exportés ?",
            default=False,
            missing=False,
            description=u"Autonomie retient les documents qui ont déjà été \
exportés, vous pouvez décider ici de les inclure")


class PeriodSchema(colander.MappingSchema):
    """
        A form used to select a period
    """
    start_date = colander.SchemaNode(colander.Date(), title=u"Date de début",
            widget=main.get_date_input())
    end_date = colander.SchemaNode(colander.Date(), title=u"Date de fin",
            widget=main.get_date_input())
    exported = ExportedField


periodSchema = PeriodSchema(
        title=u"Exporter les factures sur une période donnée",
        validator=date_validator)


class InvoiceNumberSchema(colander.MappingSchema):
    """
        Form schema for an invoice number selection (year + number)
    """
    financial_year = main.year_select_node(title=u"Année comptable")
    officialNumber = colander.SchemaNode(
            colander.String(),
            title=u'Numéro de facture')
    exported = ExportedField


class FromInvoiceNumberSchema(colander.MappingSchema):
    """
        Form schema for an invoice number selection (year + number)
    """
    financial_year = main.year_select_node(title=u"Année comptable")
    start_officialNumber = colander.SchemaNode(
            colander.String(),
            title=u'Numéro de facture',
            description=u"Numéro de facture à partir duquel vous voulez \
exporter (celle-ci sera inclue dans l'export)")
    exported = ExportedField

class AllSchema(colander.MappingSchema):
    pass
