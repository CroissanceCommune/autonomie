# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Form schema used to configure BusinessType and FileType association
"""
import colander
from colanderalchemy import SQLAlchemySchemaNode
from autonomie.models.project.file_types import BusinessTypeFileType
from autonomie.forms import customize_field


def _get_business_type_file_type_schema():
    """
    Build a schema for BusinessTypeFileType configuration

    :rtype: :class:`colanderalchemy.SQLAlchemySchemaNode`
    """
    schema = SQLAlchemySchemaNode(
        BusinessTypeFileType,
        includes=(
            'file_type_id', 'business_type_id', 'doctype', 'requirement_type',
            'validation',
        ),
    )
    customize_field(
        schema,
        'doctype',
        validator=colander.OneOf(
            ('invoice', 'cancelinvoice', 'estimation', 'business')
        )
    )
    customize_field(
        schema,
        'requirement_type',
        typ=colander.String(12),
        validator=colander.OneOf(
            (
                'business_mandatory',
                'project_mandatory',
                'mandatory',
                'recommended',
                'optionnal'
            ),
        ),
        missing=colander.drop,
    )
    customize_field(
        schema,
        'validation',
        typ=colander.String(),
        validator=colander.OneOf(
            ('on',),
        ),
        missing=colander.drop,
    )
    return schema


class BusinessTypeFileTypeEntry(colander.SequenceSchema):
    item = _get_business_type_file_type_schema()


class BusinessTypeFileTypeEntries(colander.MappingSchema):
    items = BusinessTypeFileTypeEntry()
