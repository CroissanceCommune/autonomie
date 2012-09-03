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

BASE_STATUS_DICT = {
        'draft':('draft', 'wait', 'duplicate', ),
        'invalid':('draft', 'wait', 'duplicate',),}
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

def get_est_state(base_dict):
    """
        return the estimation state workflow
    """
    valid = ('valid', MANAGER_PERMS, set_date,)
    invalid = ('invalid', MANAGER_PERMS,)
    geninv = ('geninv', None, gen_invoices,)
    delete = ('delete', None, None, False,)
    result = base_dict.copy()
    result['wait'] = (valid, invalid, 'duplicate',)
    result['valid'] = ('sent', 'aboest', geninv, 'duplicate',)
    result['sent'] = ('aboest', geninv, 'duplicate',)
    result['aboest'] = (delete,)
    result['geninv'] = ('duplicate',)
    return result

def get_inv_state(base_dict):
    """
        return the invoice state workflow
    """
    valid = ('valid', MANAGER_PERMS, valid_callback,)
    invalid = ('invalid', MANAGER_PERMS,)
    aboinv = ('aboinv', MANAGER_PERMS,)
    paid = ('paid', MANAGER_PERMS, record_payment,)
    gencinv = ('gencinv', None, gen_cancelinvoice,)
    delete = ('delete', None, None, False,)
    result = base_dict.copy()
    result['wait'] = (valid, invalid, 'duplicate',)
    result['valid'] = ('sent', aboinv, paid, 'resulted', 'duplicate',
                                                       'recinv', gencinv,)
    result['sent'] = (aboinv, paid, 'resulted', 'duplicate', 'recinv',
                                                                 gencinv,)
    result['aboinv'] = (delete,)
    result['paid'] = ('duplicate', paid, gencinv, 'resulted')
    result['recinv'] = (aboinv, paid, gencinv, 'resulted', 'duplicate',
                                                                 gencinv,)
    result['gencinv'] = (paid, 'resulted', 'duplicate',)
    return result

def get_cinv_state(base_dict):
    """
        return the cancel invoice state workflow
    """
    valid = ('valid', MANAGER_PERMS, valid_callback,)
    invalid = ('invalid', MANAGER_PERMS,)
    result = base_dict.copy()
    result['wait'] = (valid, invalid, 'duplicate',)
    result['valid'] = ('sent',)
    return result

DEFAULT_STATE_MACHINES = {
        "base":TaskState('draft', BASE_STATUS_DICT),
        "estimation":TaskState('draft', get_est_state(BASE_STATUS_DICT)),
        "invoice":TaskState('draft', get_inv_state(BASE_STATUS_DICT)),
        "cancelinvoice":TaskState('draft', get_cinv_state(BASE_STATUS_DICT))}

