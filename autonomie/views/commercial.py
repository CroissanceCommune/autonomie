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
import colander
from deform import Form

from autonomie.models.task import Estimation
from autonomie.models.task import Invoice
from autonomie.models.client import Client
from autonomie.models.project import Project
from autonomie.views.forms.commercial import CommercialFormSchema

def get_year_range(year):
    """
        Return year range enclosing the current year
    """
    return datetime.date(year, 1, 1), datetime.date(year+1, 1, 1)


def get_month_range(month, year):
    """
        Return month range enclosing the current month
    """
    if month == 12:
        nxt_year = year + 1
        nxt_month = 1
    else:
        nxt_year = year
        nxt_month = month +1
    return datetime.date(year, month, 1), datetime.date(nxt_year, nxt_month, 1)




def display(request):
    company = request.context

    schema = CommercialFormSchema().bind(request=request)
    form = Form(schema=schema, buttons=(), method='GET', formid='year_form')
    try:
        appstruct = schema.deserialize(request.GET)
    except colander.Invalid:
        appstruct = schema.deserialize({})
    form.set_appstruct(appstruct)

    year = appstruct['year']
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
                if invoice.CAEStatus in Invoice.valid_states:
                    clients += 1
                    break

    realised_number = dict()
    for month in range(1, 13):
        before, after = get_month_range(month, year)
        invoices = Invoice.query().join(Project)\
                    .filter(Project.company_id==company.id)\
                    .filter(Invoice.taskDate.between(before, after))\
                    .filter(Invoice.CAEStatus.in_(Invoice.valid_states))
        val = sum([invoice.total_ht() for invoice in invoices])
        realised_number[month] = val


    return dict(title=u"Gestion commerciale",
                estimations=estimations.count(),
                validated_estimations=validated_estimations.count(),
                clients=clients,
                realised_number=realised_number,
                form=form)

def includeme(config):
    config.add_route("commercial_handling", "/company/{id:\d+}/commercial",
                        traverse='/companies/{id}')
    config.add_view(display,
                    route_name="commercial_handling",
                    renderer="treasury/commercial.mako",
                    permission="manage")
