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
import colander

from autonomie.models.expense import get_expense_years
from autonomie.models.task.invoice import get_invoice_years
from autonomie.models import user

from autonomie import forms


def date_validator(form, value):
    """
        Validate the period
    """
    if value['start_date'] > value['end_date']:
        exc = colander.Invalid(form,
                    u"La date de début doit précéder la date de fin")
        exc['start_date'] = u"Doit précéder la date de fin"
        raise exc


EXPORTEDFIELD = colander.SchemaNode(colander.Boolean(),
            title=u"Inclure les documents déjà exportés ?",
            default=False,
            missing=False,
            description=u"Autonomie retient les documents qui ont déjà été \
exportés, vous pouvez décider ici de les inclure")


class PeriodSchema(colander.MappingSchema):
    """
        A form used to select a period
    """
    start_date = colander.SchemaNode(colander.Date(), title=u"Date de début")
    end_date = colander.SchemaNode(colander.Date(), title=u"Date de fin")
    exported = EXPORTEDFIELD


periodSchema = PeriodSchema(validator=date_validator)


class InvoiceNumberSchema(colander.MappingSchema):
    """
        Form schema for an invoice number selection (year + number)
    """
    financial_year = forms.year_select_node(
        title=u"Année comptable",
        query_func=get_invoice_years,
    )
    official_number = colander.SchemaNode(
            colander.String(),
            title=u'Numéro de facture')
    exported = EXPORTEDFIELD


class FromInvoiceNumberSchema(colander.MappingSchema):
    """
        Form schema for an invoice number selection (year + number)
    """
    financial_year = forms.year_select_node(
        title=u"Année comptable",
        query_func=get_invoice_years,
    )
    start_official_number = colander.SchemaNode(
            colander.String(),
            title=u'Numéro de facture',
            description=u"Numéro de facture à partir duquel vous voulez \
exporter (celle-ci sera inclue dans l'export)")
    exported = EXPORTEDFIELD


class AllSchema(colander.MappingSchema):
    pass


class ExpenseIdSchema(colander.MappingSchema):
    sheet_id = colander.SchemaNode(
            colander.Integer(),
            missing=0,
            title=u"Identifiant",
            description=u"Identifiant de la feuille de notes de dépense \
(voir sur la page associée)")
    exported = EXPORTEDFIELD


class ExpenseSchema(colander.MappingSchema):
    """
    Schema for sage expense export
    """
    user_id = user.user_node(title=u"Nom de l'entrepreneur",
        widget_options={'default_option':(u'0', u'Tous les entrepreneurs',)})
    year = forms.year_select_node(title=u"Année", query_func=get_expense_years)
    month = forms.month_select_node(title=u"Mois")
    exported = EXPORTEDFIELD
