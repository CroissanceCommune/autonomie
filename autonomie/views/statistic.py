# -*- coding: utf-8 -*-
# * File Name : statistic.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 03-07-2012
# * Last Modified :
#
# * Project :
#
"""
    View for statistics computing
"""
import logging
import datetime

from pyramid.view import view_config

from autonomie.models.model import Company

from .base import BaseView

log = logging.getLogger(__name__)

class StatisticView(BaseView):
    """
        View displaying statistics
    """
    @view_config(route_name="statistics", permission="manage",
                                          renderer="statistics.mako")
    @view_config(route_name="statistic", permission="manage",
                                          renderer="statistics.mako")
    def statistics(self):
        """
            the stats view
        """
        log.debug("# Asking for the statistics page #")
        ret_dict = dict(title=u"Statistiques")
        companies = Company.query(self.request.dbsession(), [Company.id,
                                                          Company.name]).all()
        ret_dict['companies'] = companies
        current_year = 2000
        years = range(2000, datetime.date.today().year+1)
        ret_dict['years'] = years
        if self.request.context.__name__ == 'company':
            if 'year' in self.request.params:
                try:
                    year = int(self.request.params['year'])
                    if year not in years:
                        raise Exception
                    current_year = year
                except:
                    pass
            company = self.request.context
            projects = company.projects
            clients = company.clients
            invoices = []
            estimations = []
            for proj in projects:
                invoices.extend([inv for inv in proj.invoices
                                        if inv.taskDate.year >= current_year])
                estimations.extend([est for est in proj.estimations \
                        if est.taskDate.year >= current_year])
            prospects = [cli for cli in clients if True not in [
                            len(proj.invoices)>0 for proj in cli.projects]]
            #Return the stats
            ret_dict['current_company'] = company
            ret_dict['projects'] = projects
            ret_dict['clients'] = clients
            ret_dict['prospects'] = prospects
            ret_dict['invoices'] = invoices
            ret_dict['estimations'] = estimations
        ret_dict['current_year'] = current_year
        return ret_dict

def sum_it(datas, key=None):
    if key:
        return sum([getattr(d, key)for d in datas])
    else:
        return sum(datas)

def lenof_if(datas):
    return len(datas)

class StatElement(object):
    def __init__(self, label, value, formatter=lambda a:a):
        self.label = label
        self.value = value
        self.formatter = formatter

    def set_formatter(self, formatter):
        """
            set a formatter
        """
        self.formatter = formatter

    def render(self):
        return u"{0} : {1}".format(label, self.formatter(value))
