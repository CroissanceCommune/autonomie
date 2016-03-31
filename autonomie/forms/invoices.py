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
import colander
import deform
import deform_extensions
from pyramid.security import has_permission

from autonomie.models import company
from autonomie.models.task import invoice
from autonomie.models.task import (
    PaymentConditions,

)
from autonomie.models.tva import (
    Product,
)

from autonomie import forms
from autonomie.forms.task import (
    TASKSCHEMA,
    deferred_default_payment_condition,
    TEMPLATES_URL,
)
from autonomie.forms import custom_types
from .custom_types import (
    AmountType,
)


STATUS_OPTIONS = (("both", u"Toutes les factures", ),
                  ("paid", u"Les factures payées", ),
                  ("notpaid", u"Seulement les impayés", ))


def get_product_choices():
    """
        Return data structure for product code select widget options
    """
    return [(p.id, u"{0} ({1})".format(p.name, p.compte_cg),)
            for p in Product.query()]


@colander.deferred
def deferred_product_validator(node, kw):
    options = [option[0] for option in get_product_choices()]
    return colander.OneOf(options)


@colander.deferred
def deferred_product_widget(node, kw):
    """
        return a widget for product selection
    """
    products = get_product_choices()
    wid = deform.widget.SelectWidget(values=products)
    return wid


@colander.deferred
def deferred_financial_year_widget(node, kw):
    request = kw['request']
    if has_permission('manage', request.context, request):
        return deform.widget.TextInputWidget(mask='9999')
    else:
        return deform.widget.HiddenWidget()


@colander.deferred
def deferred_prefix_widget(node, kw):
    request = kw['request']
    if has_permission('manage', request.context, request):
        return deform.widget.TextInputWidget()
    else:
        return deform.widget.HiddenWidget()


@colander.deferred
def deferred_default_prefix(node, kw):
    request = kw['request']
    return request.config.get('invoiceprefix', '')


FINANCIAL_YEAR = colander.SchemaNode(
    colander.Integer(),
    name="financial_year",
    title=u"Année comptable de référence",
    widget=deferred_financial_year_widget,
    default=forms.default_year,
)


PREFIX = colander.SchemaNode(
    colander.String(),
    name="prefix",
    title=u"Préfixe du numéro de facture",
    widget=deferred_prefix_widget,
    default=deferred_default_prefix,
    missing="",
)


class InvoicePayments(colander.MappingSchema):
    """
    Invoice payment conditions schema
    """
    payment_conditions_select = colander.SchemaNode(
        colander.String(),
        widget=forms.get_deferred_select(PaymentConditions),
        title=u"",
        missing=colander.drop,
    )

    payment_conditions = forms.textarea_node(
        title="",
        default=deferred_default_payment_condition,
    )


def get_invoice_schema():
    """
        Return the schema for invoice add/edit
    """
    schema = TASKSCHEMA.clone()
    schema['lines']['lines'].doctype = "invoice"

    title = u"Phase où insérer la facture"
    schema['common']['phase_id'].title = title
    # Ref #689
    schema['common'].add_before('description', FINANCIAL_YEAR)
    schema['common'].add_before('description', PREFIX)

    title = u"Date de la facture"
    schema['common']['date'].title = title

    title = u"Objet de la facture"
    schema['common']['description'].title = title

    title = u"Conditions de paiement"
    schema.add_before(
        "communication",
        InvoicePayments(title=title, name='payments')
    )

    product_id = colander.SchemaNode(

        colander.Integer(),
        title=u"Code produit",
        widget=deferred_product_widget,
        validator=deferred_product_validator,
        missing="",
        css_class="col-md-2",
        name='product_id',
    )
    schema['lines']['lines']['taskline'].add(product_id.clone())
    schema['lines']['groups']['groups']['lines']['taskline'].add(
        product_id.clone()
    )
    return schema


def get_cancel_invoice_schema():
    """
        return the cancel invoice form schema
    """
    schema = TASKSCHEMA.clone()
    schema['lines']['lines'].doctype = "taskschema"

    title = u"Phase où insérer l'avoir"
    schema['common']['phase_id'].title = title
    # Ref #689
    schema['common'].add_before('description', FINANCIAL_YEAR)
    schema['common'].add_before('description', PREFIX)

    title = u"Date de l'avoir"
    schema['common']['date'].title = title

    title = u"Objet de l'avoir"
    schema['common']['description'].title = title
    del schema['common']['course']

    title = u"Conditions de remboursement"
    del schema['lines']['discounts']

    payments = InvoicePayments(title=title, name='payments').clone()
    payments['payment_conditions'].title = title
    payments['payment_conditions'].description = u""
    payments['payment_conditions'].missing = u""

    schema['lines']['expenses_ht'].validator = forms.negative_validator

    schema.add_before("communication", payments)
    product_id = colander.SchemaNode(
        colander.Integer(),
        title=u"Code produit",
        widget=deferred_product_widget,
        validator=deferred_product_validator,
        missing="",
        css_class="col-md-2",
        name='product_id',
    )
    schema['lines']['lines']['taskline'].add(product_id.clone())
    schema['lines']['groups']['groups']['lines']['taskline'].add(
        product_id.clone()
    )
    return schema


class FinancialYearSchema(colander.MappingSchema):
    """
        colander Schema for financial year setting
    """
    financial_year = FINANCIAL_YEAR
    prefix = PREFIX


class ProductTaskLine(colander.MappingSchema):
    """
        A single estimation line
    """
    id = colander.SchemaNode(
        colander.Integer(),
        widget=deform.widget.HiddenWidget(),
        missing=u"",
        css_class="span0"
    )
    description = colander.SchemaNode(
        colander.String(),
        widget=deform_extensions.DisabledInput(),
        missing=u'',
        css_class='col-md-3',
    )
    tva = colander.SchemaNode(
        AmountType(),
        widget=deform_extensions.DisabledInput(),
        css_class='col-md-1',
        title=u'TVA',
    )
    product_id = colander.SchemaNode(
        colander.Integer(),
        widget=deferred_product_widget,
        validator=deferred_product_validator,
        missing="",
        css_class="col-md-2",
        title=u"Code produit",
    )


class ProductTaskLines(colander.SequenceSchema):
    taskline = ProductTaskLine(missing="", title=u"")


class SetProductsSchema(colander.MappingSchema):
    """
        Form schema used to configure Products
    """
    lines = ProductTaskLines(
        widget=deform.widget.SequenceWidget(
            template=TEMPLATES_URL + 'product_tasklines.pt',
            item_template=TEMPLATES_URL + 'product_tasklines_item.pt',
            min_len=1),
        missing="",
        title=u''
    )


class AmountRangeSchema(colander.MappingSchema):
    """
    Used to filter on a range of amount
    """
    start = colander.SchemaNode(
        custom_types.AmountType(),
        title="",
        missing=colander.drop,
        description=u"TTC entre",
    )
    end = colander.SchemaNode(
        custom_types.AmountType(),
        title="",
        missing=colander.drop,
        description=u"et",
    )


class PeriodSchema(colander.MappingSchema):
    """
        A form used to select a period
    """
    start = colander.SchemaNode(
        colander.Date(),
        title="",
        description=u"Émises entre le",
        missing=colander.drop,
    )
    end = colander.SchemaNode(
        colander.Date(),
        title="",
        description=u"et le",
        missing=colander.drop,
    )


# INVOICE LIST RELATED SCHEMAS
def get_list_schema(is_admin=False):
    """
    Return a schema for invoice listing

    is_admin

        If True, we don't provide the company selection node and we reduce the
        customers to the current company's
    """
    schema = forms.lists.BaseListsSchema().clone()

    schema.insert(
        0,
        colander.SchemaNode(
            colander.String(),
            name='status',
            widget=deform.widget.SelectWidget(values=STATUS_OPTIONS),
            validator=colander.OneOf([s[0] for s in STATUS_OPTIONS]),
            missing='both',
        )
    )

    schema.insert(0, company.customer_node(is_admin))

    if is_admin:
        schema.insert(
            0,
            company.company_node(
                name='company_id',
                missing=colander.drop,
                widget_options={'default': ('', u'Toutes les entreprises')}
            )
        )

    schema.insert(
        0,
        PeriodSchema(
            name='period',
            title="",
            validator=colander.Function(
                forms.range_validator,
                msg=u"La date de début doit précéder la date de début"
            ),
            widget=deform.widget.MappingWidget(
                template=TEMPLATES_URL + 'clean_mapping.pt',
            ),
            missing=colander.drop,
        )
    )
    schema.insert(
        0,
        AmountRangeSchema(
            name='ttc',
            title="",
            validator=colander.Function(
                forms.range_validator,
                msg=u"Le montant de départ doit être inférieur ou égale \
à celui de la fin"
            ),
            widget=deform.widget.MappingWidget(
                template=TEMPLATES_URL + 'clean_mapping.pt',
            ),
            missing=colander.drop,
        )
    )

    node = forms.year_select_node(
        name='year',
        query_func=invoice.get_invoice_years,
    )

    schema.insert(0, node)

    schema['search'].description = u"Identifiant du document"

    return schema


def range_validator(form, value):
    """
        Validate that end is higher or equal than start
    """
    if value['end'] > 0 and value['start'] > value['end']:
        exc = colander.Invalid(
            form,
            u"Le numéro de début doit être plus petit ou égal à celui de fin"
        )
        exc['start'] = u"Doit être inférieur au numéro de fin"
        raise exc


class InvoicesPdfExport(colander.MappingSchema):
    """
        Schema for invoice bulk export
    """
    year = forms.year_select_node(
        title=u"Année comptable",
        query_func=invoice.get_invoice_years
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
    validator=range_validator,
)
