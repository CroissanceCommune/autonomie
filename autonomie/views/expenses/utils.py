# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import deform
from autonomie.forms.expense import ExpensePaymentSchema


def get_payment_form(request, counter=None):
    """
    Return a payment form object
    """
    valid_btn = deform.Button(
        name='submit',
        value="paid",
        type='submit',
        title=u"Valider",
    )
    schema = ExpensePaymentSchema().bind(request=request)
    if request.context.__name__ == 'expense':
        action = request.route_path(
            "/expenses/{id}/addpayment",
            id=request.context.id,
        )
    else:
        action = request.route_path(
            "/expenses/{id}/addpayment",
            id=-1,
        )
    form = deform.Form(
        schema=schema,
        buttons=(valid_btn,),
        formid="paymentform",
        action=action,
        counter=counter,
    )
    return form
