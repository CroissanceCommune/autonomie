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

from autonomie.models import company
from autonomie.models.task import invoice
from autonomie.models.task import (
    PaymentConditions,
    PaymentMode,
    BankAccount,

)
from autonomie.models.tva import (
    Product,
    Tva,
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
    if request.user.is_admin() or request.user.is_manager():
        return deform.widget.TextInputWidget(mask='9999')
    else:
        return deform.widget.HiddenWidget()


FINANCIAL_YEAR = colander.SchemaNode(
    colander.Integer(),
    name="financial_year",
    title=u"Année comptable de référence",
    widget=deferred_financial_year_widget,

    default=forms.default_year,
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

    title = u"Date de la facture"
    schema['common']['taskDate'].title = title

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

    title = u"Date de l'avoir"
    schema['common']['taskDate'].title = title

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


# Payment form
def get_amount_topay(kw):
    """
    Retrieve the amount to be paid regarding the context
    """
    context = kw['request'].context
    if context.__name__ == 'invoice':
        task = context
        topay = task.topay()
    else:
        task = context.task
        topay = task.topay()
        topay += context.amount
    return topay


@colander.deferred
def deferred_amount_default(node, kw):
    """
        default value for the payment amount
    """
    return get_amount_topay(kw)


@colander.deferred
def deferred_total_validator(node, kw):
    """
        validate the amount to keep the sum under the total
    """
    topay = get_amount_topay(kw)
    max_msg = u"Le montant ne doit pas dépasser %s (total ttc - somme \
des paiements + montant d'un éventuel avoir)" % (topay / 100.0)
    min_msg = u"Le montant doit être positif"
    return colander.Range(
        min=0, max=topay, min_err=min_msg, max_err=max_msg,
    )


@colander.deferred
def deferred_payment_mode_widget(node, kw):
    """
        dynamically retrieves the payment modes
    """
    modes = [(mode.label, mode.label) for mode in PaymentMode.query()]
    return deform.widget.SelectWidget(values=modes)


@colander.deferred
def deferred_payment_mode_validator(node, kw):
    return colander.OneOf([mode.label for mode in PaymentMode.query()])


@colander.deferred
def deferred_bank_widget(node, kw):
    """
    Renvoie le widget pour la sélection d'une banque
    """
    options = [(bank.id, bank.label) for bank in BankAccount.query()]
    if len(options) > 1:
        widget = forms.get_select(options)
    else:
        widget = deform.widget.HiddenWidget()
    return widget


class PaymentSchema(colander.MappingSchema):
    """
        colander schema for payment recording
    """
    come_from = forms.come_from_node()
    amount = colander.SchemaNode(
        AmountType(),
        title=u"Montant",
        validator=deferred_total_validator,
        default=deferred_amount_default,
    )
    date = forms.today_node()
    mode = colander.SchemaNode(
        colander.String(),
        title=u"Mode de paiement",
        widget=deferred_payment_mode_widget,
        validator=deferred_payment_mode_validator,
    )
    bank_id = colander.SchemaNode(
        colander.Integer(),
        title=u"Banque",
        missing=colander.drop,
        widget=deferred_bank_widget,
        default=forms.get_deferred_default(BankAccount),
    )
    resulted = colander.SchemaNode(
        colander.Boolean(),
        title=u"Soldé",
        description="""Indique que le document est soldé (
ne recevra plus de paiement), si le montant indiqué correspond au
montant de la facture celle-ci est soldée automatiquement""",
        default=False,
    )


class TvaPayment(colander.MappingSchema):
    amount = colander.SchemaNode(
        AmountType(),
        title=u"Montant de l'encaissement",
    )
    tva_id = colander.SchemaNode(
        colander.Integer(),
        title=u"Tva liée à cet encaissement",
        widget=forms.get_deferred_select(
            Tva, mandatory=True, keys=('id', 'name')
        ),
    )


@colander.deferred
def deferred_amount_by_tva_validation(node, kw):
    invoice = kw['request'].context
    tva_parts = invoice.tva_ttc_parts()

    def validate_amount_by_tva(values):
        tva_id = values.get('tva_id')
        tva = Tva.get(tva_id)
        if tva is None:
            return u"Tva inconnue"
        amount = values.get('amount')
        if amount > tva_parts[tva.value]:
            return u"Le montant de l'encaissement doit être inférieur à la \
part de cette Tva dans la facture"

    return colander.Function(validate_amount_by_tva)


@colander.deferred
def deferred_remittance_amount_validation(node, kw):
    """
    Validate that the remittance amount is equal to the sum of the tva parts
    """
    invoice = kw['request'].context

    def validate_sum_of_tvapayments(values):
        """
        Validate the sum of the tva payments is equal to the remittance_amount
        """
        tva_sum = sum([tvap['amount'] for tvap in values['tvas']])
        remittance_amount = values['remittance_amount']
        if tva_sum != remittance_amount:
            return u"Le montant de la remise doit correspondre à la somme \
des encaissements correspondant"

    return colander.Function(validate_sum_of_tvapayments)


class TvaPaymentSequence(colander.SequenceSchema):
    tvas = TvaPayment(title=u'', validator=deferred_amount_by_tva_validation)


class MultiplePaymentSchema(colander.MappingSchema):
    """
        colander schema for payment recording
    """
    come_from = forms.come_from_node()
    remittance_amount = colander.SchemaNode(
        AmountType(),
        title=u"Montant de la remise",
        validator=deferred_total_validator,
        default=deferred_amount_default,
    )
    date = forms.today_node()
    mode = colander.SchemaNode(
        colander.String(),
        title=u"Mode de paiement",
        widget=deferred_payment_mode_widget,
        validator=deferred_payment_mode_validator,
    )
    bank_id = colander.SchemaNode(
        colander.Integer(),
        title=u"Banque",
        missing=colander.drop,
        widget=deferred_bank_widget,
        default=forms.get_deferred_default(BankAccount),
    )
    tvas = TvaPaymentSequence(title=u'Encaissements par taux de Tva')
    resulted = colander.SchemaNode(
        colander.Boolean(),
        title=u"Soldé",
        description="""Indique que le document est soldé (
ne recevra plus de paiement), si le montant indiqué correspond au
montant de la facture celle-ci est soldée automatiquement""",
        default=False,
    )


def get_payment_schema(request):
    """
    Returns the schema for payment registration
    """
    invoice = request.context
    tva_module = request.config.get('receipts_active_tva_module')

    num_tvas = len(invoice.get_tvas().keys())

    # Only one tva
    if num_tvas == 1 or not tva_module:
        return PaymentSchema()
    else:
        schema = MultiplePaymentSchema(
            validator=deferred_remittance_amount_validation
        )
        schema['tvas'].widget = deform.widget.SequenceWidget(
            min_len=1,
            max_len=num_tvas,
            orderable=False,
        )
        return schema


class FinancialYearSchema(colander.MappingSchema):
    """
        colander Schema for financial year setting
    """
    financial_year = FINANCIAL_YEAR


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
            ))

    schema.insert(0, company.customer_node(is_admin))

    if is_admin:
        schema.insert(
            0,
            colander.SchemaNode(
                custom_types.AmountType(),
                name='ttc',
                missing=colander.drop,
                description=u"Montant TTC",
            )
        )

        schema.insert(
            0,
            company.company_node(
                name='company_id',
                missing=colander.drop,
                widget_options={'default': ('', u'Toutes les entreprises')}
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
