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
import logging

from sqlalchemy import desc

from autonomie.statistics import inspect

from autonomie.resources import statistics_js
from autonomie.models.user import UserDatas
from autonomie.models.statistics import StatisticSheet
from autonomie.views import (
    BaseView,
    DisableView,
)


logger = logging.getLogger(__name__)


class StatisticSheetList(BaseView):
    """
    Listview of statistic sheets
    """
    title = u"Feuilles de statistiques"

    def __call__(self):
        sheets = StatisticSheet.query()\
                .order_by(desc(StatisticSheet.active))\
                .all()
        return dict(sheets=sheets, title=self.title)


def statistic_add_view(request):
    """
    View for adding statistics
    """
    statistics_js.need()
    loadurl = request.route_path(
        'statistics',
        _query=dict(action='options'),
    )
    return dict(
        title=u"Ajout de feuille de statistiques",
        loadurl=loadurl,
    )


def statistic_form_options(request):
    """
    Returns datas used to build the statistic form page
    """
    inspector = inspect.StatisticInspector(UserDatas)
    return dict(columns=inspector.get_json_columns())


class StatisticDisableView(DisableView):
    enable_msg = u"La feuille de statistiques a été activée"
    disable_msg = u"La feuille de statistiques a été désactivée"
    redirect_route = "statistics"


def includeme(config):
    """
    Include views in the app's configuration
    """
    # Routes for statistic sheet view/add/edit/delete
    config.add_route(
        'statistics',
        '/statistics',
    )

    config.add_route(
        'statistic',
        '/statistics/{id:\d+}',
        traverse='/statistics/{id}',
    )

    config.add_route(
        'statistic_entry',
        '/statistics/entries/{id:\d+}',
        traverse='/statistic_entries/{id}',
    )

    config.add_view(
        StatisticSheetList,
        route_name='statistics',
        renderer="statistics/list.mako",
        permission='manage',
    )

    config.add_view(
        statistic_add_view,
        route_name="statistics",
        renderer="statistics/edit.mako",
        request_param="action=add",
        permission='manage',
    )

    config.add_view(
        statistic_form_options,
        route_name='statistics',
        renderer='json',
        request_param="action=options",
        permission='manage',
    )

    config.add_view(
        StatisticDisableView,
        route_name="statistic",
        request_param="action=disable",
        permission='manage',
    )
