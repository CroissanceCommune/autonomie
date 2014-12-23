# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2014 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
"""
Job related pages
"""

from autonomie.models.job import (
    Job,
)
from autonomie.resources import job_js
from autonomie.forms.job import get_list_schema

from autonomie.utils.widgets import ViewLink
from autonomie.views import BaseListView


def job_view(context, request):
    """
    :param obj context: The job we want to watch
    :param obj request: The pyramid request object
    """
    job_js.need()
    populate_actionmenu(request)

    if context.type_ == "csv_import":
        title = u"Import de données"
    else:
        title = u"Action inconnue"
    return dict(
        title=title,
        url=request.route_path('job', id=context.id),
    )


def populate_actionmenu(request):
    request.actionmenu.add(ViewLink(u"Liste des tâches", path="jobs"))


class JobList(BaseListView):
    title = u"Historique des tâches"
    schema = get_list_schema()
    sort_columns = dict(
        created_at=Job.created_at
    )
    default_sort = "created_at"
    default_direction = "desc"

    def query(self):
        query = Job.query()
        return query

    def filter_type(self, query, appstruct):
        type_ = appstruct.get('type_')
        if type_ is not None:
            query = query.filter(Job.type_==type_)
        return query

    def filter_status(self, query, appstruct):
        status = appstruct.get('status')
        if status is not None:
            query = query.filter(Job.status=='status')
        return query


def stream_csv(context, request):
    """
    Stream resulting csv datas resulting from an import

    :param context: The csv import job instance
    """
    pass


def includeme(config):
    config.add_route('job', '/jobs/{id:\d+}', traverse="/jobs/{id}")
    config.add_route("jobs", "/jobs")
    config.add_view(
        job_view,
        route_name='job',
        renderer="/job.mako",
        permission='admin',
    )
    config.add_view(
        JobList,
        route_name="jobs",
        renderer="/jobs.mako",
        permission="admin",
    )
