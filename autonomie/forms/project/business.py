# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
from colanderalchemy import SQLAlchemySchemaNode

from autonomie.forms import customize_field
from autonomie.forms.lists import BaseListsSchema
from autonomie.models.project.business import Business


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


def get_business_edit_schema():
    """
    Build the businedd edition schema

    :rtype: :class:`colander.Schema`
    """
    schema = SQLAlchemySchemaNode(
        Business,
        includes=('name',)
    )
    customize_field(schema, 'name', title=u"Nom de l'affaire")
    return schema
