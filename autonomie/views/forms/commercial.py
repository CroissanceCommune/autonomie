# -*- coding: utf-8 -*-
# * File Name :
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
# * Project :
#
import colander
from datetime import date
from deform import widget

from beaker.cache import cache_region
from autonomie.models.task import Invoice


def get_taskdates(dbsession):
    """
        Return all taskdates
    """
    @cache_region("long_term", "taskdates")
    def taskdates():
        """
            Cached version
        """
        return dbsession.query(Invoice.financial_year)
    return taskdates()


def get_years(dbsession):
    """
        We consider that all documents should be dated after 2000
    """
    inv = get_taskdates(dbsession)

    @cache_region("long_term", "taskyears")
    def years():
        """
            cached version
        """
        return sorted(set([i.financial_year for i in inv.all()]))
    return years()


@colander.deferred
def default_year(node, kw):
    return date.today().year


@colander.deferred
def deferred_year_select_widget(node, kw):
    years = get_years(kw['request'].dbsession)
    return widget.SelectWidget(values=[(year, year)for year in years])


class CommercialFormSchema(colander.MappingSchema):
    year = colander.SchemaNode(colander.Integer(),
            widget=deferred_year_select_widget,
            default=default_year,
            missing=default_year)
