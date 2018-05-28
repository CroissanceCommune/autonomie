# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
from autonomie.forms.lists import BaseListsSchema


def get_list_schema():
    """
    Return the schema for the project search form
    :rtype: colander.Schema
    """
    schema = BaseListsSchema().clone()

    schema['search'].description = u"Nom de l'affaire"

    schema.add(
        colander.SchemaNode(
            colander.Boolean(),
            name='closed',
            label=u"Inclure les affaires terminées",
            missing=True,
        )
    )

    return schema
