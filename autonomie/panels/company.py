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
    Panels related to a company
"""
import logging

from webhelpers import paginate
from sqlalchemy import desc, or_
from sqlalchemy.orm import aliased
from autonomie.models.task import CancelInvoice, Estimation, Invoice, Task
from autonomie.models.project import Project

from autonomie import resources


_p1 = aliased(Project)
_p2 = aliased(Project)
_p3 = aliased(Project)


log = logging.getLogger(__name__)


def _get_tasklist_url(page):
    """
        Return a js url for tasklist pagination
        :param page: page number
    """
    return "#tasklist/{0}".format(page)


def _get_post_int(request, key, default):
    """
        Retrieve an int from the post datas
        :param key: the key the data should be retrieved from
        :param default: a default value
    """
    val = default
    if key in request.POST:
        try:
            val = int(request.POST[key])
        except ValueError:
            val = default
    return val


def _get_tasks_per_page(request):
    """
    Infers the nb of tasks per page from a request.
    If value supplied in POST, we redefine it in a cookie.

    tasks_per_page is a string representation of a base 10 int
        expected to be 5, 15 or 50.

    """
    post_value = _get_post_int(request, 'tasks_per_page', None)
    if post_value is not None:
        request.response.set_cookie('tasks_per_page', '%d' % post_value)
        return post_value

    if 'tasks_per_page' in request.cookies:
        raw_nb_per_page = request.cookies['tasks_per_page']
        return int(raw_nb_per_page)

    # fall back to base value
    return 5


def _company_tasks_query(company_id):
    """
    Build sqlalchemy query to all tasks of a company, in reverse statusDate
    order.
    """
    query = Task.query()
    query = query.with_polymorphic([Invoice, Estimation, CancelInvoice])
    query = query.order_by(desc(Task.statusDate))

    query = query.outerjoin(_p1, Invoice.project)
    query = query.outerjoin(_p2, Estimation.project)
    query = query.outerjoin(_p3, CancelInvoice.project)

    return query.filter(or_(
                _p1.company_id==company_id,
                _p2.company_id==company_id,
                _p3.company_id==company_id
                ))


def _get_taskpage_number(request):
    """
        Return the page number the user is asking
    """
    return _get_post_int(request, 'tasks_page_nb', 0)


def recent_tasks_panel(context, request):
    """
    Panel returning the company's tasklist
    Parameters to be supplied as a cookie or in request.POST

    pseudo params: tasks_per_page, see _get_tasks_per_page()
    tasks_page_nb: -only in POST- the page we display
    """
    if not request.is_xhr:
        # javascript engine for the panel
        resources.task_list_js.need()

    query = _company_tasks_query(context.id)
    page_nb = _get_taskpage_number(request)
    items_per_page = _get_tasks_per_page(request)

    paginated_tasks = paginate.Page(
            query,
            page_nb,
            items_per_page=items_per_page,
            url=_get_tasklist_url,
            )

    result_data = {'tasks': paginated_tasks}

    return result_data


def includeme(config):
    """
        Add all panels to our main config object
    """
    config.add_panel(recent_tasks_panel,
                    'company_tasks',
                    renderer='panels/tasklist.mako')
