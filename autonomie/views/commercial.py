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
    Commercial Management module
"""
import datetime
import colander

from sqlalchemy import (
    extract,
    and_,
    or_,
)
from sqlalchemy.orm import (
    load_only,
)
from deform import Form
from deform.exception import ValidationFailure
from pyramid.httpexceptions import HTTPFound

from autonomie.compute.math_utils import percent
from autonomie.models.task import (
    Estimation,
    Invoice,
    CancelInvoice,
)
from autonomie.models.commercial import TurnoverProjection
from autonomie.forms import (
    merge_session_with_post,
)
from autonomie.views import (
    submit_btn,
    BaseView,
)
from autonomie.forms.commercial import (
    CommercialFormSchema,
    CommercialSetFormSchema,
)
from autonomie.resources import commercial_js


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
        nxt_month = month + 1
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

    def __init__(self, context, request):
        super(DisplayCommercialHandling, self).__init__(context, request)
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
        return self.request.context.get_estimations(valid=True).filter(
            extract('year', Estimation.date) == self.year
        )

    def validated_estimations(self):
        """
            Query for estimations where an invoice has been generated
        """
        return self.estimations().filter(Estimation.geninv == True)

    def customers(self):
        """
            Return the number of real customers (with invoices)
            for the current year
        """
        return self.request.context.get_real_customers(self.year).count()

    def turnovers(self):
        """
            Return the realised turnovers
        """
        result = dict(year_total=0)
        for month in range(1, 13):

            invoices = self.request.context.get_invoices(valid=True).options(
                load_only('ht')
            )

            date_condition = and_(
                extract('year', Invoice.date) == self.year,
                extract('month', Invoice.date) == month,
                Invoice.financial_year == self.year,
            )
            if month not in (1, 12):
                invoices = invoices.filter(date_condition)
            else:
                if month == 12:
                    # for december, we also like to have invoices edited in
                    # january and reported to the previous comptability year
                    reported_condition = and_(
                        Invoice.financial_year == self.year,
                        extract('year', Invoice.date) > self.year,
                    )
                else:  # month=1
                    # for january, we also like to have invoices edited in
                    # december and reported to the next comptability year
                    reported_condition = and_(
                        Invoice.financial_year == self.year,
                        extract('year', Invoice.date) < self.year,
                    )
                invoices = invoices.filter(
                    or_(date_condition, reported_condition)
                )

            invoice_sum = sum([invoice.ht for invoice in invoices])

            cinvoices = self.request.context.get_cancelinvoices(
                valid=True
            ).options(
                load_only('ht')
            )

            date_condition = and_(
                extract('year', CancelInvoice.date) == self.year,
                extract('month', CancelInvoice.date) == month,
                CancelInvoice.financial_year == self.year,
            )
            if month not in (1, 12):
                cinvoices = cinvoices.filter(date_condition)
            else:
                if month == 12:
                    reported_condition = and_(
                        CancelInvoice.financial_year == self.year,
                        extract('year', CancelInvoice.date) > self.year,
                    )
                else:  # month=1
                    reported_condition = and_(
                        CancelInvoice.financial_year == self.year,
                        extract('year', CancelInvoice.date) < self.year,
                    )

                cinvoices = cinvoices.filter(
                    or_(date_condition, reported_condition)
                )

            cinvoice_sum = sum([cinvoice.ht for cinvoice in cinvoices])

            result[month] = invoice_sum + cinvoice_sum
            result['year_total'] += result[month]
        return result

    def turnover_projections(self):
        """
            Return a query for turnover projections
        """
        query = TurnoverProjection.query()
        query = query.filter(
            TurnoverProjection.company_id == self.request.context.id
            )
        result = query.filter(TurnoverProjection.year == self.year)

        return result

    def submit_success(self, appstruct):
        """
            Add/Edit a turnover projection in the database
        """
        appstruct['year'] = self.year
        appstruct['company_id'] = self.request.context.id

        query = self.turnover_projections()
        query = query.filter(TurnoverProjection.month == appstruct['month'])
        result = query.first()

        projection = result or TurnoverProjection()

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

        turnover_projections = dict(year_total=0)
        for projection in self.turnover_projections():
            turnover_projections[projection.month] = projection
            turnover_projections['year_total'] += projection.value

        return dict(
            title=self.title,
            estimations=self.estimations().count(),
            validated_estimations=self.validated_estimations().count(),
            customers=self.customers(),
            turnovers=self.turnovers(),
            turnover_projections=turnover_projections,
            year_form=year_form,
            form=form,
            compute_turnover_difference=compute_turnover_difference,
            compute_percent=percent,
            compute_turnover_percent=compute_turnover_percent,
        )


def compute_turnover_difference(index, projections, turnovers):
    """
        Compute the difference beetween the projection and the real value
    """
    projection = projections.get(index)
    if projection:
        turnover = turnovers.get(index, 0)
        return turnover - projection.value
    else:
        return None


def compute_turnover_percent(index, projections, turnovers):
    """
        Compute the percent the difference represents
    """
    turnover = turnovers.get(index)
    if turnover is not None:
        projection = projections.get(index)
        if projection is not None:
            if projection.value is not None:
                return percent(turnover, projection.value, 0)
    return None


def includeme(config):
    config.add_route(
        "commercial_handling",
        "/company/{id:\d+}/commercial",
        traverse='/companies/{id}',
    )
    config.add_view(
        DisplayCommercialHandling,
        route_name="commercial_handling",
        renderer="treasury/commercial.mako",
        permission="edit_commercial_handling",
    )
