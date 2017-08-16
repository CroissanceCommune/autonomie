# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Action objects
"""
from autonomie import interfaces
from autonomie.models.action_manager import (
    Action,
    ActionManager,
)


def invoice_valid_callback(request, task, **kw):
    """
    Set a official number on invoices (or cancelinvoices)

    :param obj request: The current pyramid request
    :param obj context: The current context
    """
    invoice_service = request.find_service(interfaces.IInvoiceService)
    invoice_service.valid_callback(task)
    return task


def get_status_actions(data_type):
    """
    Return a state machine handling the basic states

    :param str data_type: estimation/invoice/cancelinvoice

    :returns: A state machine that can be used to perform state changes
    :rtype: class:`autonomie.models.statemachine.StateMachine`
    """
    manager = ActionManager()
    for status, icon, label, title, css in (
        (
            'valid', "ok-sign",
            u"Valider",
            u"Valider ce document (il ne pourra plus être modifié)",
            "btn btn-primary primary-action",
        ),
        (
            'wait',
            'time',
            u"Demander la validation",
            u"Enregistrer ce document et en demander la validation",
            "btn btn-primary primary-action",
        ),
        (
            'invalid',
            'trash',
            u"Invalider",
            u"Invalider ce document afin que l'entrepreneur le corrige",
            "btn btn-default",
        ),
        (
            'draft',
            'save',
            u"Enregistrer",
            u'Enregistrer en brouillon afin de modifier ce document '
            u'ultérieurement',
            'btn btn-default',
        ),
    ):
        action = Action(
            status,
            '%s.%s' % (status, data_type),
            status_attr='status',
            userid_attr='status_person_id',
            icon=icon,
            label=label,
            title=title,
            css=css,
        )
        if status == 'valid' and data_type in ('invoice', 'cancelinvoice'):
            action.callback = invoice_valid_callback

        manager.add(action)
    return manager


DEFAULT_ACTION_MANAGER = {
    'estimation': get_status_actions('estimation'),
    'invoice': get_status_actions('invoice'),
    'cancelinvoice': get_status_actions('cancelinvoice'),
}


def get_signed_status_actions():
    """
    Return actions available for setting the signed_status attribute on
    Estimation objects
    """
    manager = ActionManager()
    for status, icon, label, title, css in (
        (
            'waiting',
            'time',
            u"En attente de réponse",
            u"En attente de réponse du client",
            "btn btn-default"
        ),
        (
            "sent",
            "send",
            u"Envoyé au client",
            u"A bien été envoyé au client",
            "btn btn-default",
        ),
        (
            'aborted',
            'trash',
            u"Sans suite",
            u"Marquer sans suite",
            "btn btn-default",
        ),
        (
            'signed',
            'ok',
            u"Signé par le client",
            u"Indiquer que le client a passé commande",
            "btn btn-default",
        ),
    ):
        action = Action(
            status,
            'set_signed_status.estimation',
            status_attr='signed_status',
            icon=icon,
            label=label,
            title=title,
            css=css,
        )
        manager.add(action)
    return manager


SIGNED_ACTION_MANAGER = get_signed_status_actions()
