# -*- coding: utf-8 -*-
# * File Name : sage.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 24-09-2013
# * Last Modified :
#
# * Project :
#
"""
    Form schemas for invoice exports
"""
from datetime import date
import colander
from autonomie.views.forms.widgets import (
        get_date_input,
        deferred_year_select_widget,
        )


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
    if value['start_date'] >= value['end_date']:
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
            widget=get_date_input())
    end_date = colander.SchemaNode(colander.Date(), title=u"Date de fin",
            widget=get_date_input())
    exported = ExportedField


periodSchema = PeriodSchema(
        title=u"Exporter les factures sur une période donnée",
        validator=date_validator)


class InvoiceNumberSchema(colander.MappingSchema):
    """
        Form schema for an invoice number selection (year + number)
    """
    financial_year = colander.SchemaNode(colander.Integer(),
            widget=deferred_year_select_widget,
            default=default_year,
            missing=default_year,
            title=u"Année comptable")
    officialNumber = colander.SchemaNode(
            colander.String(),
            title=u'Numéro de facture')
    exported = ExportedField


class FromInvoiceNumberSchema(colander.MappingSchema):
    """
        Form schema for an invoice number selection (year + number)
    """
    financial_year = colander.SchemaNode(colander.Integer(),
            widget=deferred_year_select_widget,
            default=default_year,
            missing=default_year,
            title=u"Année comptable")
    start_officialNumber = colander.SchemaNode(
            colander.String(),
            title=u'Numéro de facture',
            description=u"Numéro de facture à partir duquel vous voulez \
exporter (celle-ci sera inclue dans l'export)")
    exported = ExportedField

class AllSchema(colander.MappingSchema):
    pass

