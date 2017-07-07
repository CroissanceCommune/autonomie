# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import datetime
import logging
import colander
from sqlalchemy import (distinct, extract)

from autonomie.forms.tasks.estimation import (
    get_list_schema,
)

from autonomie.models.company import Company
from autonomie.models.customer import Customer
from autonomie.models.task import (
    Estimation,
    Task,
)
from autonomie.views import BaseListView

logger = logging.getLogger(__name__)


class GlobalEstimationList(BaseListView):
    title = u""
    add_template_vars = (u'title', 'is_admin',)
    schema = get_list_schema(is_global=True)
    sort_columns = dict(
        date=Estimation.date,
        customer=Customer.name,
        company=Company.name,
    )
    default_sort = 'date'
    default_direction = 'desc'
    is_admin = True

    def query(self):
        query = self.request.dbsession.query(
            distinct(Estimation.id),
            Estimation.name,
            Estimation.internal_number,
            Estimation.status,
            Estimation.signed_status,
            Estimation.geninv,
            Estimation.date,
            Estimation.description,
            Estimation.ht,
            Estimation.tva,
            Estimation.ttc,
            Customer.id,
            Customer.name,
            Company.id,
            Company.name
        )
        query = query.outerjoin(Task.company)
        query = query.outerjoin(Task.customer)
        query = query.filter(Estimation.status == 'valid')
        return query

    def filter_date(self, query, appstruct):
        period = appstruct.get('period', {})
        if period.get('start') not in (colander.null, None):
            logger.debug("  + Filtering by date : %s" % period)
            start = period.get('start')
            end = period.get('end')
            if end not in (None, colander.null):
                end = datetime.date.today()
            query = query.filter(Task.date.between(start, end))
        else:
            year = appstruct.get('year')
            if year is not None:
                query = query.filter(extract('year', Estimation.date) == year)
        return query

    def filter_ttc(self, query, appstruct):
        ttc = appstruct.get('ttc', {})
        if ttc.get('start') not in (None, colander.null):
            logger.info(u"  + Filtering by ttc amount : %s" % ttc)
            start = ttc.get('start')
            end = ttc.get('end')
            if end in (None, colander.null):
                query = query.filter(Estimation.ttc >= start)
            else:
                query = query.filter(Estimation.ttc.between(start, end))
        return query

    def _get_company_id(self, appstruct):
        return appstruct.get('company_id')

    def filter_company(self, query, appstruct):
        company_id = self._get_company_id(appstruct)
        if company_id not in (None, colander.null):
            logger.info("  + Filtering on the company id : %s" % company_id)
            query = query.filter(Task.company_id == company_id)
        return query

    def filter_customer(self, query, appstruct):
        """
            filter estimations by customer
        """
        customer_id = appstruct.get('customer_id')
        if customer_id not in (None, colander.null):
            logger.info("  + Filtering on the customer id : %s" % customer_id)
            query = query.filter(Estimation.customer_id == customer_id)
        return query

    def filter_status(self, query, appstruct):
        """
            Filter estimations by status
        """
        status = appstruct['status']
        logger.info("  + Status filtering : %s" % status)
        if status == 'geninv':
            query = query.filter(Estimation.geninv == True)
        elif status != 'all':
            query = query.filter(Estimation.signed_status == status)

        return query

    def more_template_vars(self, response_dict):
        """
        Add template vars to the response dict

        :param obj result: A Sqla Query
        :returns: vars to pass to the template
        :rtype: dict
        """
        ret_dict = BaseListView.more_template_vars(self, response_dict)
        records = response_dict['records']
        ret_dict['totalht'] = sum(r[8] for r in records)
        ret_dict['totaltva'] = sum(r[9] for r in records)
        ret_dict['totalttc'] = sum(r[10] for r in records)
        return ret_dict


class EstimationList(GlobalEstimationList):
    schema = get_list_schema(is_global=False)
    is_admin = False

    def _get_company_id(self, appstruct):
        """
        Return the current context's company id
        """
        return self.request.context.id


def add_routes(config):
    """
    Add module's specific routes
    """
    config.add_route(
        "company_estimations",
        "/company/{id:\d+}/estimations",
        traverse="/companies/{id}"
    )
    config.add_route(
        "estimations",
        "/estimations",
    )


def add_views(config):
    """
    Add the views defined in this module
    """
    # Estimation list related views
    config.add_view(
        EstimationList,
        route_name="company_estimations",
        renderer="estimations.mako",
        permission="list_estimations",
    )

    config.add_view(
        GlobalEstimationList,
        route_name="estimations",
        renderer="estimations.mako",
        permission="admin_tasks",
    )


def includeme(config):
    add_routes(config)
    add_views(config)
