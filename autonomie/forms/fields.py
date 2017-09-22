# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
import datetime

from autonomie import forms


@colander.deferred
def deferred_january_first(node, kw):
    """
    Deferly returns the first january value
    """
    today = datetime.date.today()
    return datetime.date(today.year, 1, 1)


class YearPeriodSchema(colander.MappingSchema):
    """
    A form used to select a period
    """
    start_date = colander.SchemaNode(
        colander.Date(),
        title=u"Début",
        missing=colander.drop,
        default=deferred_january_first
    )
    end_date = colander.SchemaNode(
        colander.Date(),
        title=u"Fin",
        missing=colander.drop,
        default=forms.deferred_today
    )

    def validator(self, form, value):
        """
            Validate the period
        """
        if value['start_date'] > value['end_date']:
            exc = colander.Invalid(
                form,
                u"La date de début doit précéder la date de fin"
            )
            exc['start_date'] = u"Doit précéder la date de fin"
            raise exc
