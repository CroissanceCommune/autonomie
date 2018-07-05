# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
"""
import logging

from webhelpers import paginate
from sqlalchemy import desc
from sqlalchemy.orm import aliased
from autonomie.models.task import (
    Task,
)
from autonomie.models.project import Project

from autonomie import resources
from autonomie.panels.company_index import utils

_p1 = aliased(Project)
_p2 = aliased(Project)
_p3 = aliased(Project)

log = logging.getLogger(__name__)


def _company_tasks_query(company):
    """
    Build sqlalchemy query to all tasks of a company, in reverse status_date
    order.
    """
    return company.get_tasks().order_by(desc(Task.status_date))


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

    query = _company_tasks_query(context)
    page_nb = utils.get_page_number(request, "tasks_page_nb")
    items_per_page = utils.get_items_per_page(request, 'tasks_per_page')

    paginated_tasks = paginate.Page(
        query,
        page_nb,
        items_per_page=items_per_page,
        url=utils.make_get_list_url('tasklist'),
    )

    result_data = {'tasks': paginated_tasks}

    return result_data


def includeme(config):
    """
        Add all panels to our main config object
    """
    config.add_panel(
        recent_tasks_panel,
        'company_recent_tasks',
        renderer='panels/company_index/recent_tasks.mako',
    )
