# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.project.types import (
    ProjectType,
    SubProjectType,
)
from autonomie.forms import (
    customize_field,
    get_deferred_model_select,
    get_sequence_child_item,
    get_deferred_model_select_checkbox
)


def _build_unique_label_validator(class_, type_id=None):
    """
    Return a unique label validator

    :param int type_id: Exception id
    :returns: A validator
    :rtype: function
    """
    def validator(node, value):
        if not class_.unique_label(value, type_id):
            message = u"Ce nom n'est pas disponible : {0}".format(value)
            raise colander.Invalid(node, message)

    return validator


def get_deferred_unique_label_validator(class_):
    """
    Returns a unique label validator for the given class

    :param obj class_: The classname ProjectType/SubProjectType
    """
    @colander.deferred
    def deferred_unique_label_validator(node, kw):
        """
        Deferred unique validator
        """
        context = kw['request'].context
        if isinstance(context, (ProjectType, SubProjectType)):
            type_id = context.id
        else:
            type_id = None
        return _build_unique_label_validator(class_, type_id=type_id)
    return deferred_unique_label_validator


def get_admin_project_type_schema():
    schema = SQLAlchemySchemaNode(
        ProjectType,
        includes=("label",)
    )
    customize_field(
        schema,
        "label",
        validator=get_deferred_unique_label_validator(ProjectType),
    )
    return schema


def get_admin_subproject_type_schema():
    schema = SQLAlchemySchemaNode(
        SubProjectType,
        includes=(
            'label', 'project_type_id', 'other_project_types'
        )
    )
    customize_field(
        schema,
        "label",
        validator=get_deferred_unique_label_validator(SubProjectType),
    )
    customize_field(
        schema, 'project_type_id', widget=get_deferred_model_select(ProjectType)
    )
    customize_field(
        schema,
        'other_project_types',
        children=get_sequence_child_item(ProjectType),
        widget=get_deferred_model_select_checkbox(
            ProjectType,
            filters=[['active', True]],
        )
    )

    return schema
