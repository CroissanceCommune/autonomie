# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
# import deform_extensions
from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.project.types import (
    ProjectType,
    SubProjectType,
)
from autonomie.forms import (
    customize_field,
    reorder_schema,
    get_deferred_select,
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
        includes=(
            "name", "label", "private", "default",
        )
    )
    reorder_schema(schema, ('label', 'default'))
    customize_field(
        schema,
        "label",
        validator=get_deferred_unique_label_validator(ProjectType),
    )
    # customize_field(
    #     schema,
    #     "private",
    #     widget=deform_extensions.CheckboxToggleWidget(true_target="name")
    # )
    return schema


def get_admin_subproject_type_schema():
    schema = SQLAlchemySchemaNode(
        SubProjectType,
        includes=(
            'label', 'private', 'name', 'project_type_id'
        )
    )
    reorder_schema(schema, ('label', 'project_type_id'))
    customize_field(
        schema,
        "label",
        validator=get_deferred_unique_label_validator(SubProjectType),
    )
    # customize_field(
    #     schema,
    #     "private",
    #     widget=deform_extensions.CheckboxToggleWidget(true_target="name")
    # )
    customize_field(
        schema, 'project_type_id', widget=get_deferred_select(ProjectType)
    )
    return schema
