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

from autonomie.models.payments import (
    PaymentMode,
    BankAccount,
)

from autonomie import forms


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
