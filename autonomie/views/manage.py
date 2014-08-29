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
    Manage view :
        - last documents page
"""
import logging

from sqlalchemy import and_

from autonomie.models.task.task import Task
from autonomie.models.treasury import ExpenseSheet
from autonomie.models.task.invoice import (
    Invoice,
    CancelInvoice,
)
from autonomie.models.task.estimation import Estimation
from autonomie.models.project import Phase
from autonomie.models.activity import Activity
from autonomie.models.user import User

log = logging.getLogger(__name__)


def manage(request):
    """
        The manage view
    """
    query = Estimation.query()
    query = query.join(Estimation.phase)
    query = query.filter(
        and_(
            Estimation.CAEStatus == 'wait',
            Phase.name is not None
        )
    )
    estimations = query.order_by(Task.statusDate).all()
    for item in estimations:
        item.url = request.route_path(item.type_, id=item.id)

    invoices = Task.query()\
            .filter(Task.type_.in_(('invoice', 'cancelinvoice',)))\
            .join(Task.phase)\
            .filter(and_(Task.CAEStatus == 'wait', Phase.name is not None))\
            .order_by(Task.type_).order_by(Task.statusDate).all()

    for item in invoices:
        item.url = request.route_path(item.type_, id=item.id)

    expenses = ExpenseSheet.query()\
            .filter(ExpenseSheet.status == 'wait')\
            .order_by(ExpenseSheet.month).all()
    for expense in expenses:
        expense.url = request.route_path("expense", id=expense.id)


    user_id = request.user.id
    query = Activity.query()
    query = query.join(Activity.conseillers)
    query = query.filter(
        Activity.conseillers.any(User.id==user_id)
    )
    query = query.filter(Activity.status=='planned')
    query = query.order_by(Activity.datetime).limit(10)
    activities = query.all()

    for activity in activities:
        activity.url = request.route_path("activity", id=activity.id)

    return dict(title=u"Documents en attente de validation",
                invoices=invoices,
                estimations=estimations,
                expenses = expenses,
                activities=activities)

def includeme(config):
    config.add_route("manage",
                    "/manage")
    config.add_view(manage,
                    route_name="manage",
                    renderer="manage.mako",
                    permission="manage")
