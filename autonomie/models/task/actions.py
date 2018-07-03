# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Action objects
"""
from autonomie.models.config import Config
from autonomie.models.action_manager import (
    Action,
    ActionManager,
)
from autonomie.models.services.invoice_sequence_number import (
    InvoiceNumberService,
)


def _set_invoice_number(request, task, **kw):
    """
    Set a official number on invoices (or cancelinvoices)

    :param obj request: The current pyramid request
    :param obj task: The current context
    """
    template = Config.get_value('invoice_number_template', None)
    assert template is not None, \
        'invoice_number_template setting should be set'

    if task.official_number is None:
        InvoiceNumberService.assign_number(
            task,
            template,
        )
    return task


def _force_file_requirement_indicators(request, task, **kw):
    """
    Force File requirement to be successfull

    :param obj request: The current pyramid request
    :param obj task: The current context
    """
    task.file_requirement_service.force_all(task)
    return task


def estimation_valid_callback(request, task, **kw):
    """
    Estimation validation callback

    :param obj request: The current pyramid request
    :param obj task: The current context
    """
    _force_file_requirement_indicators(request, task, **kw)
    return task


def invoice_valid_callback(request, task, **kw):
    """
    Invoice validation callback

    :param obj request: The current pyramid request
    :param obj task: The current context
    """
    _set_invoice_number(request, task, **kw)
    _force_file_requirement_indicators(request, task, **kw)
    return task


def get_status_actions(data_type):
    """
    Return a state machine handling the basic states

    :param str data_type: estimation/invoice/cancelinvoice

    :returns: An action manager machine that can be used to perform state changes
    :rtype: class:`autonomie.models.action_manager.ActionManager`
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
        if status == 'valid':
            if data_type in ('invoice', 'cancelinvoice'):
                action.callback = invoice_valid_callback
            else:
                action.callback = estimation_valid_callback

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
