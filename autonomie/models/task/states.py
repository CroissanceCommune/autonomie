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
    Tasks states
"""
import logging
import datetime

from autonomie.models.statemachine import (
    StateMachine,
    State,
)
from autonomie.exception import Forbidden
from autonomie.exception import SignatureError
from autonomie import interfaces

log = logging.getLogger(__name__)

MANAGER_PERMS = "manage"


class TaskStates(StateMachine):
    """
        Task statemachine
    """
    status_attr = "status"
    userid_attr = "statusPerson"


def valid_callback(request, task, **kw):
    """
        callback for the task validation
    """
    task = set_date(request, task)
    invoice_service = request.find_service(interfaces.IInvoiceService)
    invoice_service.valid_callback(task)
    return task


def record_payment(request, invoice, **kw):
    """
    record a payment for the given task
    """
    log.info(u"Recording a payment for {0}".format(invoice))
    if "amount" in kw:
        invoice.record_payment(**kw)
    elif "tvas" in kw:
        for payment in kw['tvas']:
            invoice.record_payment(**payment)
    else:
        raise Forbidden(u"Missing mandatory arguments")
    return invoice


def duplicate_task(request, task, **kw):
    """
        Duplicates a task
    """
    project = kw.get("project")
    phase = kw.get("phase")
    customer = kw.get('customer')
    if project is not None and phase is not None and customer is not None:
        return task.duplicate(kw['user'], project, phase, customer)
    else:
        raise Forbidden(u"Missing mandatory arguments")


def mark_estimation_signed(request, estimation, **kw):
    """
    mark an estimation as signed
    :param obj request: The current request
    :param obj estimation: The task to edit
    :param dict kw: The keywords
    """
    estimation.signed_status = 'signed'
    return estimation


def mark_estimation_aborted(request, estimation, **kw):
    """
    mark an estimation as aborted
    :param obj request: The current request
    :param obj estimation: The task to edit
    :param dict kw: The keywords
    """
    estimation.signed_status = 'aborted'
    return estimation


def edit_metadata_task(request, task, **kw):
    """
        Change a task's phase
    """
    for key, value in kw.items():
        if value not in (None, ''):
            setattr(task, key, value)
    return task


def edit_task_date(request, task, **kw):
    """
    Change a task's date
    :param obj request: The current request
    :param obj task: The task to edit
    :param dict kw: The keywords
    """
    new_date = kw.get('date')
    if new_date is not None:
        task.date = new_date
    return task


def gen_cancelinvoice(request, task, **kw):
    """
        gen the cancelinvoice for the given task
    """
    if 'user' in kw:
        return task.gen_cancelinvoice(kw['user'])
    else:
        raise SignatureError()


def gen_invoices(request, task, **kw):
    """
        gen_invoices for the given task
    """
    if "user" in kw:
        return task.gen_invoices(kw['user'])
    else:
        raise SignatureError()


def set_date(request, task, **kw):
    """
        set the date of the current task
    """
    task.date = datetime.date.today()
    return task


def set_financial_year(request, task, **kw):
    """
        Set the financial year of the current task
    """
    if 'financial_year' in kw:
        task.financial_year = kw['financial_year']
    if 'prefix' in kw:
        task.prefix = kw['prefix']
    return task


def set_products(request, task, **kw):
    """
        Set the products to the lines of the current task
    """
    for line in kw.get('lines', []):
        line_id = line.pop('id')
        product_id = line.get('product_id')
        if line_id is not None and product_id is not None:
            for line_ in task.all_lines:
                if line_.id == line_id:
                    line_.product_id = product_id
                else:
                    log.warning(
                        u"Unknow line number in form validation : {0}"
                        .format(line_id)
                    )
        else:
            log.warning(u"No line id was passed at form validation")
    return task


def get_est_state():
    """
        return the estimation state workflow
        draft
        wait
        valid
        invalid
        aboest
    """
    draft = ('draft', ('edit.estimation', 'add_estimation'))
    wait = ('wait', 'wait.estimation')
    manager_wait = ('wait', 'admin_estimation',)
    duplicate = ('duplicate', 'edit.estimation', duplicate_task, False,)
    edit_metadata = (
        "edit_metadata",
        "edit.estimation",
        edit_metadata_task,
        False,
    )
    valid = ('valid', 'valid.estimation', set_date,)
    invalid = ('invalid', 'admin_estimation',)
    geninv = ('geninv', "edit.estimation", gen_invoices,)
    delete = ('delete', "edit.estimation", None, False,)
    aboest = ('aboest', 'edit.estimation', )
    result = {}

    result['draft'] = (draft, wait, delete, valid, duplicate,)
    result['invalid'] = result['draft']

    result['wait'] = (
        draft,
        manager_wait,
        valid,
        invalid,
        duplicate,
        delete,
        edit_metadata,
    )
    result['valid'] = (
        aboest,
        geninv,
        duplicate,
        edit_metadata,
    )
    result['aboest'] = (edit_metadata, )
    result['geninv'] = (duplicate, edit_metadata, geninv)
    return result


def get_inv_state():
    """
        return the invoice state workflow
        draft
        wait
        valid
        invalid
        paid
        resulted
    """
    draft = ('draft', ('edit.invoice', 'add_invoice'))
    wait = ('wait', 'wait.invoice')
    manager_wait = ('wait', 'admin_invoice',)
    duplicate = (
        'duplicate',
        ('edit.invoice', 'add_invoice'),
        duplicate_task,
        False,
    )
    edit_metadata = (
        "edit_metadata",
        ('edit.invoice', 'add_invoice'),
        edit_metadata_task,
        False,
    )
    valid = ('valid', "valid.invoice", valid_callback,)
    invalid = ('invalid', "admin_invoice",)
    paid = ('paid', "add_payment", record_payment,)
    gencinv = (
        'gencinv',
        'edit.invoice',
        gen_cancelinvoice,
        False,
    )
    delete = ('delete', 'edit.invoice', None, False,)
    resulted = ('resulted', "add_payment",)
    financial_year = (
        'set_financial_year', "admin_invoice", set_financial_year, False,
    )
    products = (
        "set_products", "admin_invoice", set_products, False,
    )

    result = {}

    result['draft'] = (draft, wait, delete, valid, duplicate)
    result['invalid'] = result['draft']

    result['wait'] = (
        draft,
        manager_wait,
        valid,
        invalid,
        duplicate,
        delete,
        financial_year,
        edit_metadata,)

    result['valid'] = (
        paid,
        resulted,
        gencinv,
        duplicate,
        edit_metadata,
        financial_year,
        products,
    )

    result['paid'] = (
        paid, resulted, gencinv, duplicate, financial_year,
        edit_metadata, products,
    )

    result['resulted'] = (
        gencinv, duplicate, financial_year, edit_metadata,
        products,
    )

    return result


def get_cinv_state():
    """
        return the cancel invoice state workflow
        draft
        wait
        valid
        invalid
    """
    draft = ('draft', ('edit.cancelinvoice', 'add.cancelinvoice'))
    wait = ('wait', 'wait.cancelinvoice',)
    delete = ('delete', 'edit.cancelinvoice', None, False,)
    edit_metadata = (
        "edit_metadata",
        "edit.invoice",
        edit_metadata_task,
        False,
    )
    valid = ('valid', "valid.cancelinvoice", valid_callback,)
    invalid = ('invalid', "admin_invoice",)
    financial_year = (
        'set_financial_year', "admin_invoice", set_financial_year, False,
    )
    products = (
        "set_products", "admin_invoice", set_products, False,
    )
    result = {}
    result['draft'] = (draft, wait, delete, valid, )
    result['invalid'] = result['draft']

    result['wait'] = (
        draft,
        valid,
        invalid,
        delete,
        financial_year,
        edit_metadata,
        products,
    )

    result['valid'] = (financial_year, edit_metadata, products, )
    return result


def get_maninv_state():
    """
        Return the states for manual invoices
    """
    return {}


def get_state_machine(data_type):
    """
    Return a state machine handling the basic states

    :param str data_type: estimation/invoice/cancelinvoice

    :returns: A state machine that can be used to perform state changes
    :rtype: class:`autonomie.models.statemachine.StateMachine`
    """
    draft = State(
        'draft',
        'edit_%s' % data_type,
        status_attr='status',
        userid_attr='statusPerson',
    )
    wait = State(
        'wait',
        'wait.%s' % data_type,
        status_attr='status',
        userid_attr='statusPerson',
    )
    invalid = State(
        'invalid',
        'invalid.%s' % data_type,
        status_attr='status',
        userid_attr='statusPerson',
    )
    valid = State(
        'valid',
        'valid.%s' % data_type,
        status_attr='status',
        userid_attr='statusPerson',
    )
    machine = TaskStates()
    machine.add_transition('draft', draft)
    machine.add_transition('draft', wait)
    machine.add_transition('draft', valid)

    machine.add_transition('invalid', draft)
    machine.add_transition('invalid', valid)
    machine.add_transition('invalid', wait)

    machine.add_transition('wait', valid)
    machine.add_transition('wait', invalid)
    return machine


DEFAULT_STATE_MACHINES = {
    "base": get_state_machine('task'),
    "estimation": get_state_machine('estimation'),
    "invoice": get_state_machine('invoice'),
    "cancelinvoice": get_state_machine('cancelinvoice'),
}
