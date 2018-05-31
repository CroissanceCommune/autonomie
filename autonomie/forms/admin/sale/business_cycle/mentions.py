# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Form schema used to configure BusinessType and TaskMention association
"""
import colander
from colanderalchemy import SQLAlchemySchemaNode
from autonomie.models.project.mentions import BusinessTypeTaskMention
from autonomie.forms import customize_field


def _get_business_type_task_mention_schema():
    """
    Build a schema for BusinessTypeTaskMention configuration

    :rtype: :class:`colanderalchemy.SQLAlchemySchemaNode`
    """
    schema = SQLAlchemySchemaNode(
        BusinessTypeTaskMention,
        includes=(
            'task_mention_id', 'business_type_id', 'doctype', 'mandatory'
        ),
    )
    customize_field(
        schema,
        'doctype',
        validator=colander.OneOf(
            ('invoice', 'cancelinvoice', 'estimation')
        )
    )
    customize_field(
        schema,
        'mandatory',
        typ=colander.String(),
        validator=colander.OneOf(
            ('true', 'false'),
        ),
        missing=colander.drop,
    )
    return schema


class BusinessTypeMentionEntry(colander.SequenceSchema):
    item = _get_business_type_task_mention_schema()


class BusinessTypeMentionEntries(colander.MappingSchema):
    items = BusinessTypeMentionEntry()
