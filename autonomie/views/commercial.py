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
from decimal import Decimal

from sqlalchemy import extract
from deform import Form
from deform.exception import ValidationFailure
from fanstatic import Resource
from pyramid.httpexceptions import HTTPFound

from autonomie.utils.views import submit_btn
from autonomie.views.forms import merge_session_with_post
from autonomie.compute.math_utils import dec_round
from autonomie.models.task import (
        Estimation,
        Invoice,
        CancelInvoice,
        )
from autonomie.models.client import Client
from autonomie.models.project import Project
from autonomie.models.treasury import TurnoverProjection
from autonomie.views.base import BaseView
from autonomie.views.forms.commercial import (
        CommercialFormSchema,
        CommercialSetFormSchema,
        )
from autonomie.resources import lib_autonomie, backbone

commercial_js = Resource(lib_autonomie, "js/commercial.js", depends=[backbone])

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


def get_current_url(request):
    """
        return the current url with arguments
    """
    return request.path_url + "?" + request.query_string


def get_form(counter):
    """
        Return the form for turnover projection configuration
    """
    schema = CommercialSetFormSchema()
    return Form(schema=schema, buttons=(submit_btn,), formid='setform',
                counter=counter)

class DisplayCommercialHandling(BaseView):
    """
        Commercial handling view
        Allows to get commercial informations by year through GET
        Allows to set turnover projections through POST
    """
    title = u"Gestion commerciale"
    year_form_schema = CommercialFormSchema()
    form_schema = CommercialSetFormSchema()

    def __init__(self, request):
        super(DisplayCommercialHandling, self).__init__(request)
        commercial_js.need()
        self.year = self.submit_year()['year']

    def submit_year(self):
        """
            Validate the year form datas
        """
        schema = self.year_form_schema.bind(request=self.request)
        try:
            appstruct = schema.deserialize(self.request.GET)
        except colander.Invalid:
            appstruct = schema.deserialize({})
        return appstruct

    def get_year_form(self):
        """
            Return the year selection form
        """
        schema = self.year_form_schema.bind(request=self.request)
        form = Form(schema=schema, buttons=(), method='GET', formid='year_form')
        form.set_appstruct(self.submit_year())
        return form

    def estimations(self):
        """
            Query for estimations
        """
        return Estimation.query().join(Project)\
                    .filter(Project.company_id==self.request.context.id)\
                    .filter(extract('year', Estimation.taskDate)==self.year)

    def validated_estimations(self):
        """
            Query for estimations where an invoice has been generated
        """
        return self.estimations()\
                .filter(Estimation.CAEStatus=='geninv')

    def clients(self):
        """
            Return the number of real clients (with invoices)
            for the current year
        """
        company_id = self.request.context.id
        result = 0
        for client in Client.query().filter(Client.company_id==company_id):
            for invoice in client.invoices:
                if invoice.financial_year == self.year:
                    if invoice.CAEStatus in Invoice.valid_states:
                        result += 1
                        break
        return result

    def turnovers(self):
        """
            Return the realised turnovers
        """
        result = dict()
        for month in range(1, 13):
            invoices = Invoice.query().join(Project)\
               .filter(Project.company_id==self.request.context.id)\
               .filter(extract('year', Invoice.taskDate)==self.year)\
               .filter(extract('month', Invoice.taskDate)==month)\
               .filter(Invoice.CAEStatus.in_(Invoice.valid_states))
            invoice_sum = sum([invoice.total_ht() for invoice in invoices])
            cinvoices = CancelInvoice.query().join(Project)\
               .filter(Project.company_id==self.request.context.id)\
               .filter(extract('year', CancelInvoice.taskDate)==self.year)\
               .filter(extract('month', CancelInvoice.taskDate)==month)\
               .filter(CancelInvoice.CAEStatus.in_(CancelInvoice.valid_states))
            cinvoice_sum = sum([cinvoice.total_ht() for cinvoice in cinvoices])
            result[month] = invoice_sum + cinvoice_sum
        return result

    def turnover_projections(self):
        """
            Return a query for turnover projections
        """
        return TurnoverProjection.query()\
                .filter(TurnoverProjection.company_id==self.request.context.id)\
                .filter(TurnoverProjection.year==self.year)

    def submit_success(self, appstruct):
        """
            Add/Edit a turnover projection in the database
        """
        appstruct['year'] = self.year
        appstruct['company_id'] = self.request.context.id
        projection = self.turnover_projections()\
                .filter(TurnoverProjection.month==appstruct['month'])\
                .first() \
                or TurnoverProjection()
        projection = merge_session_with_post(projection, appstruct)
        if projection.id is not None:
            projection = self.request.dbsession.merge(projection)
        else:
            self.request.dbsession.add(projection)
        url = get_current_url(self.request)
        return HTTPFound(url)

    def __call__(self):
        year_form = self.get_year_form()
        # Passing a counter to avoid DOM conflict in field ids
        form = get_form(year_form.counter)
        if "submit" in self.request.POST:
            try:
                appstruct = form.validate(self.request.POST.items())
                self.submit_success(appstruct)
            except ValidationFailure as e:
                form = e
        turnover_projections = dict((t.month, t)
                        for t in self.turnover_projections())
        return dict(title=self.title,
                    estimations=self.estimations().count(),
                    validated_estimations=self.validated_estimations().count(),
                    clients=self.clients(),
                    turnovers=self.turnovers(),
                    turnover_projections=turnover_projections,
                    year_form=year_form,
                    form=form,
                    compute_difference=compute_difference,
                    compute_percent=compute_percent)


def compute_difference(index, projections, turnovers):
    """
        Compute the difference beetween the projection and the real value
    """
    projection = projections.get(index)
    if projection:
        turnover = turnovers.get(index, 0)
        return turnover - projection.value
    else:
        return None


def compute_percent(index, projections, turnovers):
    """
        Compute the percent the difference represents
    """
    turnover = turnovers.get(index)
    if turnover:
        projection = projections.get(index)
        if projection:
            if projection.value:
                value = turnover * 100.0 / projection.value
                return float(dec_round(Decimal(str(value)), 2))
    return None


def includeme(config):
    config.add_route("commercial_handling", "/company/{id:\d+}/commercial",
                        traverse='/companies/{id}')
    config.add_view(DisplayCommercialHandling,
                    route_name="commercial_handling",
                    renderer="treasury/commercial.mako",
                    permission="edit")
