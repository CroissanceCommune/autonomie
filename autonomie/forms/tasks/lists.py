# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
from autonomie.forms.custom_types import AmountType


TEMPLATES_URL = 'autonomie:deform_templates/'


class PeriodSchema(colander.MappingSchema):
    """
        A form used to select a period
    """
    start = colander.SchemaNode(
        colander.Date(),
        title="",
        description=u"Émises entre le",
        missing=colander.drop,
    )
    end = colander.SchemaNode(
        colander.Date(),
        title="",
        description=u"et le",
        missing=colander.drop,
    )


class AmountRangeSchema(colander.MappingSchema):
    """
    Used to filter on a range of amount
    """
    start = colander.SchemaNode(
        AmountType(5),
        title="",
        missing=colander.drop,
        description=u"TTC entre",
    )
    end = colander.SchemaNode(
        AmountType(5),
        title="",
        missing=colander.drop,
        description=u"et",
    )
