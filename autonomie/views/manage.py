# -*- coding: utf-8 -*-
# * File Name : manage.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 25-06-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Manage view :
        - last documents page
"""
import logging

from sqlalchemy import and_

from autonomie.models.task.task import Task
from autonomie.models.treasury import ExpenseSheet
from autonomie.models.task.invoice import Invoice
from autonomie.models.task.invoice import CancelInvoice
from autonomie.models.task.estimation import Estimation
from autonomie.models.project import Phase

log = logging.getLogger(__name__)


def manage(request):
    """
        The manage view
    """
    documents = Task.query()\
            .with_polymorphic([Invoice, CancelInvoice, Estimation])\
            .join(Task.phase)\
            .filter(and_(Task.CAEStatus == 'wait', Phase.name is not None))\
            .order_by(Task.statusDate).all()
    for document in documents:
        document.url = request.route_path(document.type_, id=document.id)

    expenses = ExpenseSheet.query()\
            .filter(ExpenseSheet.status == 'wait')\
            .order_by(ExpenseSheet.month).all()
    for expense in expenses:
        expense.url = request.route_path("expense", id=expense.id)
    return dict(title=u"Documents en attente de validation",
                tasks=documents,
                expenses = expenses)

def includeme(config):
    config.add_route("manage",
                    "/manage")
    config.add_view(manage,
                    route_name="manage",
                    renderer="manage.mako",
                    permission="manage")
