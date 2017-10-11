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


from autonomie.models.task.task import Task
from autonomie.models.expense.sheet import ExpenseSheet
from autonomie.models.activity import Activity
from autonomie.models.user import User

log = logging.getLogger(__name__)


def manage(request):
    """
    The manage view
    """
    estimations = Task.get_waiting_estimations().all()

    invoices = Task.get_waiting_invoices().all()

    for item in estimations:
        item.url = request.route_path('/estimations/{id}', id=item.id)

    for item in invoices:
        item.url = request.route_path('/%ss/{id}' % item.type_, id=item.id)

    expenses = ExpenseSheet.query()\
        .filter(ExpenseSheet.status == 'wait')\
        .order_by(ExpenseSheet.month)\
        .order_by(ExpenseSheet.status_date).all()
    for expense in expenses:
        expense.url = request.route_path("/expenses/{id}", id=expense.id)

    user_id = request.user.id
    query = Activity.query()
    query = query.join(Activity.conseillers)
    query = query.filter(
        Activity.conseillers.any(User.id == user_id)
    )
    query = query.filter(Activity.status == 'planned')
    query = query.order_by(Activity.datetime).limit(10)
    activities = query.all()

    for activity in activities:
        activity.url = request.route_path("activity", id=activity.id)

    return dict(
        title=u"Mon tableau de bord",
        invoices=invoices,
        estimations=estimations,
        expenses=expenses,
        activities=activities,
    )


def includeme(config):
    config.add_route(
        "manage",
        "/manage",
    )
    config.add_view(
        manage,
        route_name="manage",
        renderer="manage.mako",
        permission="manage",
    )
