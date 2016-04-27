# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2015 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
import colander
import deform

from autonomie.models.task import (
    PaymentMode,
    BankAccount,
)
from autonomie.models.tva import (
    Tva,
)

from autonomie import forms
from .custom_types import (
    AmountType,
)


def get_amount_topay(kw):
    """
    Retrieve the amount to be paid regarding the context
    """
    topay = 0
    context = kw['request'].context
    if context.__name__ in ('invoice', 'expense'):
        topay = context.topay()
    else:
        if hasattr(context, 'parent'):
            document = context.parent
            if hasattr(document, 'topay'):
                topay = document.topay()
                if hasattr(context, 'get_amount'):
                    topay += context.get_amount()
    return topay


@colander.deferred
def deferred_amount_default(node, kw):
    """
        default value for the payment amount
    """
    return get_amount_topay(kw)


@colander.deferred
def deferred_remittance_amount_default(node, kw):
    """
        default value for the payment amount
    """
    from autonomie.views.render_api import format_amount
    return format_amount(get_amount_topay(kw), precision=5, grouping=False)


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
    widget = forms.get_select(options)
    return widget


class PaymentSchema(colander.MappingSchema):
    """
        colander schema for payment recording
    """
    come_from = forms.come_from_node()
    remittance_amount = colander.SchemaNode(
        colander.String(),
        title=u"Identifiant de la remise en banque",
        description=u"Ce champ est un indicateur permettant de \
retrouver la remise en banque à laquelle cet encaissement est associé",
        default=deferred_remittance_amount_default,
    )
    amount = colander.SchemaNode(
        AmountType(5),
        title=u"Montant de l'encaissement",
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
        AmountType(5),
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
        return True

    return colander.Function(validate_amount_by_tva)


@colander.deferred
def deferred_payment_amount_validation(node, kw):
    """
    Validate that the remittance amount is equal to the sum of the tva parts
    """
    def validate_sum_of_tvapayments(values):
        """
        Validate the sum of the tva payments is equal to the remittance_amount
        """
        tva_sum = sum([tvap['amount'] for tvap in values['tvas']])
        remittance_amount = values['payment_amount']
        if tva_sum != remittance_amount:
            return u"Le montant du paiement doit correspondre à la somme \
des encaissements correspondant"
        return True

    return colander.Function(validate_sum_of_tvapayments)


class TvaPaymentSequence(colander.SequenceSchema):
    tvas = TvaPayment(title=u'', validator=deferred_amount_by_tva_validation)


class MultiplePaymentSchema(colander.MappingSchema):
    """
        colander schema for payment recording
    """
    come_from = forms.come_from_node()
    remittance_amount = colander.SchemaNode(
        colander.String(),
        title=u"Identifiant de la remise en banque",
        default=deferred_remittance_amount_default,
    )
    payment_amount = colander.SchemaNode(
        AmountType(5),
        title=u"Montant du paiement",
        description=u"Ce champ permet de contrôler que la somme des \
encaissements saisis dans ce formulaire correspondent bien au montant du \
paiement.",
        validator=deferred_total_validator,
        default=deferred_amount_default,
    )
    date = forms.today_node(title=u"Date de la remise")
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
            validator=deferred_payment_amount_validation
        )
        schema['tvas'].widget = deform.widget.SequenceWidget(
            min_len=1,
            max_len=num_tvas,
            orderable=False,
        )
        return schema


@colander.deferred
def deferred_expense_total_validator(node, kw):
    """
        validate the amount to keep the sum under the total
    """
    topay = get_amount_topay(kw)
    max_msg = u"Le montant ne doit pas dépasser %s (total ttc - somme \
des paiements)" % (topay / 100.0)
    min_msg = u"Le montant doit être positif"
    return colander.Range(
        min=0, max=topay, min_err=min_msg, max_err=max_msg,
    )


class ExpensePaymentSchema(colander.MappingSchema):
    """
    Schéma de saisi des paiements des notes de dépense
    """
    come_from = forms.come_from_node()
    amount = colander.SchemaNode(
        AmountType(),
        title=u"Montant du paiement",
        validator=deferred_expense_total_validator,
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
    waiver = colander.SchemaNode(
        colander.Boolean(),
        title=u"Abandon de créance",
        description="""Indique que ce paiement correspond à un abandon de
créance à la hauteur du montant indiqué (le Mode de paiement et la Banque sont
alors ignorés)""",
        default=False,
    )
    resulted = colander.SchemaNode(
        colander.Boolean(),
        title=u"Soldé",
        description="""Indique que le document est soldé (
ne recevra plus de paiement), si le montant indiqué correspond au
montant de feuille de notes de dépense celle-ci est soldée automatiquement""",
        default=False,
    )
