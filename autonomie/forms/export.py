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

from autonomie.models.expense.sheet import get_expense_years
from autonomie.models.task.invoice import get_invoice_years
from autonomie.models import user

from autonomie import forms


class ExportedField(colander.SchemaNode):
    schema_type = colander.Boolean
    title = u"Inclure les éléments déjà exportés ?"
    description = (
        u"Autonomie retient les éléments qui ont déjà été "
        u"exportés, vous pouvez décider ici de les inclure"
    )
    default = False
    missing = False


class PeriodSchema(colander.MappingSchema):
    """
        A form used to select a period
    """
    start_date = colander.SchemaNode(colander.Date(), title=u"Date de début")
    end_date = colander.SchemaNode(colander.Date(), title=u"Date de fin")
    exported = ExportedField()

    def validator(self, form, value):
        """
            Validate the period
        """
        if value['start_date'] > value['end_date']:
            exc = colander.Invalid(
                form,
                u"La date de début doit précéder la date de fin"
            )
            exc['start_date'] = u"Doit précéder la date de fin"
            raise exc


@colander.deferred
def deferred_invoice_number_clean(node, kw):
    request = kw['request']
    prefix = request.config.get('invoiceprefix', '')

    def cleaner(value):
        if prefix and value.startswith(prefix):
            return value[len(prefix):]
        else:
            return value

    return cleaner


class InvoiceNumberSchema(colander.MappingSchema):
    """
        Form schema for an invoice number selection (year + number)
    """
    financial_year = forms.year_select_node(
        title=u"Année comptable",
        query_func=get_invoice_years,
    )
    start = colander.SchemaNode(
        colander.String(),
        title=u'Depuis la facture numéro',
        description=u"Numéro de facture à partir duquel exporter",
        preparer=deferred_invoice_number_clean,
    )
    end = colander.SchemaNode(
        colander.String(),
        title=u"Jusqu'à la facture numéro",
        description=u"Numéro de facture jusqu'auquel exporter "
        u"(dernier document si vide)",
        preparer=deferred_invoice_number_clean,
        missing=0,
    )
    exported = ExportedField()

    def validator(self, form, value):
        """
        Validate the number range
        """
        if value['end'] > 0 and value['start'] > value['end']:
            exc = colander.Invalid(
                form,
                u"Le numéro de début doit être plus petit ou égal à celui "
                u"de fin"
            )
            exc['start'] = u"Doit être inférieur au numéro de fin"
            raise exc


class AllSchema(colander.MappingSchema):
    pass


class ExpenseSchema(colander.MappingSchema):
    """
    Schema for sage expense export
    """
    user_id = user.user_node(
        title=u"Nom de l'entrepreneur",
        widget_options={'default_option': (u'0', u'Tous les entrepreneurs',)}
    )
    year = forms.year_select_node(title=u"Année", query_func=get_expense_years)
    month = forms.month_select_node(title=u"Mois")
    exported = ExportedField()


class ExpenseIdSchema(colander.MappingSchema):
    sheet_id = colander.SchemaNode(
        colander.Integer(),
        title=u"Identifiant",
        description=u"Identifiant de la feuille de notes de dépense "
        u"(voir sur la page associée)")
    exported = ExportedField()
