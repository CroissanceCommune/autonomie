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
from autonomie.models.activity import Activity
from autonomie.models.user import User

from autonomie import resources

_p1 = aliased(Project)
_p2 = aliased(Project)
_p3 = aliased(Project)

PARTICIPANTS = aliased(User)

log = logging.getLogger(__name__)


def _get_page_number(request, post_arg):
    """
        Return the page number the user is asking
    """
    return _get_post_int(request, post_arg, 0)


def _make_get_list_url(listname):
    """
    Return a url builder for the pagination
        :param listname: the name of the list
    """
    tmpl = "#{listname}/{option}".format(listname=listname, option="{0}")
    def _get_list_url(page):
        """
            Return a js url for a list pagination
            :param page: page number
        """
        return tmpl.format(page)
    return _get_list_url


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


def _get_items_per_page(request, cookie_name):
    """
    Infers the nb of items per page from a request.
    If value supplied in POST, we redefine it in a cookie.

    cookie_name is a string representation of a base 10 int
        expected to be 5, 15 or 50.

    """
    default = 5

    post_value = _get_post_int(request, cookie_name, None)
    if post_value is not None:
        request.response.set_cookie(cookie_name, '%d' % post_value)
        return post_value

    if cookie_name in request.cookies:
        raw_nb_per_page = request.cookies[cookie_name]
        try:
            return int(raw_nb_per_page)
        except ValueError:
            # Not an int, setting it again and going on
            request.response.set_cookie(cookie_name, '%d' % default)

    # fall back to base value
    return default


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
    page_nb = _get_page_number(request, "tasks_page_nb")
    items_per_page = _get_items_per_page(request, 'tasks_per_page')

    paginated_tasks = paginate.Page(
            query,
            page_nb,
            items_per_page=items_per_page,
            url=_make_get_list_url('tasklist'),
            )

    result_data = {'tasks': paginated_tasks}

    return result_data


def _user_activities_query(user_id):
    """
    Return a sqla query for the user's activities
    """
    query = Activity.query()
    query = query.outerjoin(PARTICIPANTS, Activity.participants)
    query = query.filter(Activity.participants.any(PARTICIPANTS.id==user_id))
    query = query.order_by(desc(Activity.date))
    return query


def next_activities_panel(context, request):
    """
        Return the list of the upcoming activities
    """
    if not request.is_xhr:
        resources.activity_list_js.need()

    query = _user_activities_query(request.user.id)
    page_nb = _get_page_number(request, 'activities_page_nb')
    items_per_page = _get_items_per_page(request, 'activities_per_page')

    paginated_activities = paginate.Page(
            query,
            page_nb,
            items_per_page=items_per_page,
            url=_make_get_list_url('activities'),
            )

    result_data = {'activities': paginated_activities}
    return result_data


def includeme(config):
    """
        Add all panels to our main config object
    """
    config.add_panel(recent_tasks_panel,
                    'company_tasks',
                    renderer='panels/tasklist.mako')
    config.add_panel(next_activities_panel,
                    'company_activities',
                    renderer='panels/activitylist.mako')
