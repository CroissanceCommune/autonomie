# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 03-09-2012
# * Last Modified :
#
# * Project :
#
"""
    Tasks states
"""
import logging
import datetime

from autonomie.models.statemachine import TaskState
from autonomie.exception import Forbidden
from autonomie.exception import SignatureError

log = logging.getLogger(__name__)

MANAGER_PERMS = "manage"


def valid_callback(task, **kw):
    """
        callback for the task validation
    """
    task = set_date(task)
    task.valid_callback()
    return task


def record_payment(task, **kw):
    """
        record a payment for the given task
        expecting a paymendMode to be passed throught kw
    """
    log.debug("recording a payment")
    log.debug(task)
    if "mode" in kw and "amount" in kw:
        return task.record_payment(kw['mode'], kw['amount'], kw.get('resulted'))
    else:
        raise Forbidden()


def duplicate_task(task, **kw):
    """
        Duplicates a task
    """
    if kw.get("project") is not None and kw.get("phase") is not None:
        return task.duplicate(kw['user'], kw['project'], kw['phase'])
    else:
        raise Forbidden()


def gen_cancelinvoice(task, **kw):
    """
        gen the cancelinvoice for the given task
    """
    if 'user_id' in kw:
        return task.gen_cancelinvoice(kw['user_id'])
    else:
        raise SignatureError()


def gen_invoices(task, **kw):
    """
        gen_invoices for the given task
    """
    if "user_id" in kw:
        return task.gen_invoices(kw['user_id'])
    else:
        raise SignatureError()


def set_date(task, **kw):
    """
        set the date of the current task
    """
    task.taskDate = datetime.date.today()
    return task


def get_base_state():
    """
        return the task states
    """
    result = {}
    result['draft'] = ('draft', 'wait', )
    result['invalid'] = ('draft', 'wait',)
    return result


def get_est_state():
    """
        return the estimation state workflow
        draft
        wait
        valid
        invalid
        aboest
    """
    duplicate = ('duplicate', 'view', duplicate_task, False,)
    valid = ('valid', MANAGER_PERMS, set_date,)
    invalid = ('invalid', MANAGER_PERMS,)
    geninv = ('geninv', None, gen_invoices,)
    delete = ('delete', None, None, False,)
    result = {}
    result['draft'] = ('draft', 'wait', 'delete',)
    result['invalid'] = ('draft', 'wait', 'delete',)
    result['wait'] = (valid, invalid, duplicate, 'delete')
    result['valid'] = ('aboest', geninv, duplicate, 'delete')
    result['aboest'] = (delete,)
    result['geninv'] = (duplicate,)
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
        aboinv
    """
    duplicate = ('duplicate', 'view', duplicate_task, False,)
    valid = ('valid', MANAGER_PERMS, valid_callback,)
    invalid = ('invalid', MANAGER_PERMS,)
    aboinv = ('aboinv', MANAGER_PERMS,)
    paid = ('paid', MANAGER_PERMS, record_payment,)
    gencinv = ('gencinv', None, gen_cancelinvoice, False,)
    delete = ('delete', None, None, False,)
    mdelete = ('delete', MANAGER_PERMS, None, False,)
    resulted = ('resulted', MANAGER_PERMS,)
    result = {}
    result['draft'] = ('draft', 'wait', delete,)
    result['invalid'] = ('draft', 'wait', delete, )
    result['wait'] = (valid, invalid, duplicate, delete, )
    result['valid'] = (paid, resulted, aboinv, gencinv, duplicate, mdelete, )
    result['paid'] = (paid, resulted, gencinv, duplicate,)
    result['resulted'] = (gencinv, duplicate,)
    result['aboinv'] = (delete,)
    return result


def get_cinv_state():
    """
        return the cancel invoice state workflow
        draft
        wait
        valid
        invalid
    """
    valid = ('valid', MANAGER_PERMS, valid_callback,)
    invalid = ('invalid', MANAGER_PERMS,)
    result = {}
    result['draft'] = ('wait', 'delete', )
    result['wait'] = (valid, invalid, 'delete', )
    result['invalid'] = ('draft', 'wait',)
    return result

DEFAULT_STATE_MACHINES = {
        "base": TaskState('draft', get_base_state()),
        "estimation": TaskState('draft', get_est_state()),
        "invoice": TaskState('draft', get_inv_state()),
        "cancelinvoice": TaskState('draft', get_cinv_state())}
