# -*- coding: utf-8 -*-
# * File Name : commercial.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 01-02-2013
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Commercial Management module
"""
import datetime
from fanstatic import Resource

from autonomie.models.task import Estimation
from autonomie.models.client import Client
from autonomie.models.project import Project

def get_year_range(year):
    """
        Return year range enclosing the current year
    """
    return datetime.date(year-1, 1,1), datetime.date(year, 1,1)

def display(request):
    default_year = datetime.date.today().year
    company = request.context

    year = request.params.get('year', "")
    if year.isdigit() and len(year) == 4:
        year = int(year)
    else:
        year = default_year
    before, after = get_year_range(year)
    estimations = Estimation.query().join(Project)\
                    .filter(Project.company_id==company.id)\
                    .filter(Estimation.taskDate.between(before, after))
    validated_estimations = estimations.filter(Estimation.CAEStatus=='geninv')
    all_clients = Client.query().filter(Client.company_id==company.id)
    clients = 0
    for client in all_clients:
        for invoice in client.invoices:
            if invoice.financial_year == year:
                clients += 1
                break

    return dict(title=u"Gestion commerciale",
                estimations=estimations.count(),
                validated_estimations=validated_estimations.count(),
                clients=clients)

def includeme(config):
    config.add_route("commercial_handling", "/company/{id:\d+}/commercial",
                        traverse='/companies/{id}')
    config.add_view(display,
                    route_name="commercial_handling",
                    renderer="treasury/commercial.mako",
                    permission="manage")
