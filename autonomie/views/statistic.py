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
    View for statistics computing
"""
import logging
import datetime

from pyramid.view import view_config

from autonomie.models.company import Company

log = logging.getLogger(__name__)


class StatisticView(object):
    """
        View displaying statistics
    """
    def __init__(self, request):
        self.request = request

    def __call__(self):
        """
            the stats view
        """
        ret_dict = dict(title=u"Statistiques")
        companies = Company.query([Company.id, Company.name]).all()
        ret_dict['companies'] = companies
        current_year = 2000
        years = range(2000, datetime.date.today().year + 1)
        ret_dict['years'] = years
        if self.request.context.__name__ == 'company':
            if 'year' in self.request.params:
                try:
                    year = int(self.request.params['year'])
                    if year not in years:
                        raise ValueError
                except:
                    year = 2000
                current_year = year
            company = self.request.context
            projects = company.projects
            clients = company.clients
            invoices = []
            estimations = []
            for proj in projects:
                invoices.extend(
                    [inv
                     for inv in proj.invoices
                     if inv.taskDate.year >= current_year]
                )
                estimations.extend(
                    [est
                     for est in proj.estimations
                     if est.taskDate.year >= current_year]
                )
            prospects = [cli
                         for cli in clients
                         if True not in [len(proj.invoices) > 0
                                         for proj in cli.projects]]
            #Return the stats
            ret_dict['current_company'] = company
            ret_dict['projects'] = projects
            ret_dict['clients'] = clients
            ret_dict['prospects'] = prospects
            ret_dict['invoices'] = invoices
            ret_dict['estimations'] = estimations
        ret_dict['current_year'] = current_year
        return ret_dict


def includeme(config):
    """
        Route/views declaration for statistic prototype view
    """
    config.add_route('statistic',
                     '/statistics/{id:\d+}',
                     traverse='/companies/{id}')
    config.add_route('statistics',
                    '/statistics')
    config.add_view(StatisticView,
                    route_name="statistics",
                    permission="manage",
                    renderer="statistics.mako")
    config.add_view(StatisticView,
                    route_name="statistic",
                    permission="manage",
                    renderer="statistics.mako")
