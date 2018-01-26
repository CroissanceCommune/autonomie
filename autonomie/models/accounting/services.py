# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from sqlalchemy import (
    desc,
    extract,
    distinct,
)
from autonomie_base.models.base import DBSESSION


class TreasuryMeasureGridService(object):
    @classmethod
    def last(cls, grid_class, company_id):
        query = DBSESSION().query(grid_class).filter_by(company_id=company_id)
        query = query.order_by(desc(grid_class.date))
        return query.first()

    @classmethod
    def get_years(cls, grid_class):
        query = DBSESSION().query(distinct(extract('year', grid_class.date)))
        result = [a[0] for a in query.all()]
        result.sort()
        return result

    @classmethod
    def measure_by_internal_id(cls, instance, internal_id):
        from autonomie.models.accounting.treasury_measures import (
            TreasuryMeasure,
            TreasuryMeasureType,
        )
        type_id = TreasuryMeasureType.get_by_internal_id(internal_id)

        if type_id is not None:
            query = TreasuryMeasure.query().filter_by(grid_id=instance.id)
            query = query.filter_by(measure_type_id=type_id)
            result = query.first()
        else:
            result = None
        return result


class IncomeStatementMeasureGridService(object):

    @classmethod
    def get_type_measure(cls, grid_id, measure_type_id):
        from autonomie.models.accounting.income_statement_measures import (
            IncomeStatementMeasure,
            IncomeStatementMeasureType,
        )
        query = DBSESSION().query(IncomeStatementMeasure)
        query = query.filter_by(grid_id=grid_id)
        query = query.filter_by(measure_type_id=measure_type_id)
        return query.first()

    @classmethod
    def get_years(cls, grid_class, company_id=None):
        query = DBSESSION().query(distinct(extract('year', grid_class.date)))

        if company_id is not None:
            query = query.filter_by(company_id=company_id)

        result = [a[0] for a in query.all()]
        result.sort()
        return result
