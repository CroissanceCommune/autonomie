# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie.models.statistics import StatisticEntry
from autonomie.views.statistics import (
	CRITERION_MODELS,
	get_inspector,
)
from autonomie.statistics import EntryQueryFactory


def get_query(model, where):
    """
    Return a query on the given model based on a filter list


    E.g :

        get_query(
            UserDatas,
            [
                {
                    "key":"created_at",
                    "method":"dr",
                    "type":"date",
                    "search1":"1999-01-01",
                    "search2":"2016-12-31"
                }
            ]
        )

    Filter syntax

        key

            The model attribute

        method

            See autonomie.statistics.__init__.py for keywords and their meaning

        type

            One of
                string
                number
                bool

        search1

            The first search entry

        search2

            Regarding the method of this filter, we may need a second parameter



    :param cls model: The model to get items from
    :param list where: List of criteria in dict form
    :returns: A SQLA query
    :rtype: obj
    """
    entry = StatisticEntry(title="script related entry", description="")

    for criterion_dict in where:
        criterion_factory = CRITERION_MODELS[criterion_dict['type']]
        entry.criteria.append(criterion_factory(**criterion_dict))

    inspector = get_inspector(model)
    query_factory = EntryQueryFactory(model, entry, inspector)
    return query_factory.query()
