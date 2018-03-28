# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import functools
import deform
import colander
from colanderalchemy import SQLAlchemySchemaNode
from autonomie.models.tva import (
    Tva,
    Product,
)
from autonomie.models.task import WorkUnit
from autonomie.models.task.mentions import TaskMention
from autonomie.models.task.task import (
    DiscountLine,
    TaskLineGroup,
    TaskLine,
    ALL_STATES,
)

from autonomie import forms
from autonomie.forms.custom_types import (
    AmountType,
    QuantityType,
)
from autonomie.forms.user import get_deferred_user_choice
from autonomie.forms.tasks.base import (
    taskline_after_bind,
    task_after_bind,
)


def tva_product_validator(node, value):
    """
    Validator checking that tva and product_id matches
    """
    product_id = value.get('product_id')
    if product_id is not None:
        tva_id = value.get('tva_id')
        if tva_id is not None:
            tva = Tva.get(tva_id)
            if product_id not in [p.id for p in tva.products]:
                exc = colander.Invalid(
                    node,
                    u"Ce produit ne correspond pas à la TVA configurée"
                )
                exc['product_id'] = u"Le code produit doit correspondre à la \
                    TVA configurée pour cette prestation"
                raise exc


def _customize_discountline_fields(schema):
    """
    Customize DiscountLine colander schema related fields

    :param obj schema: The schema to modify
    """
    customize = functools.partial(forms.customize_field, schema)
    customize("id", widget=deform.widget.HiddenWidget())
    customize("task_id", missing=colander.required)
    customize(
        "description",
        widget=deform.widget.TextAreaWidget(),
        validator=forms.textarea_node_validator
    )
    customize(
        "amount",
        typ=AmountType(5),
        missing=colander.required,
    )
    customize(
        "tva",
        typ=AmountType(2),
        validator=forms.get_deferred_select_validator(Tva, id_key='value'),
        missing=colander.required,
    )

    return schema


def _customize_taskline_fields(schema):
    """
    Customize TaskLine colander schema related fields

    :param obj schema: The schema to modify
    """
    schema.validator = tva_product_validator
    schema.after_bind = taskline_after_bind
    customize = functools.partial(forms.customize_field, schema)
    customize('id', widget=deform.widget.HiddenWidget())
    customize(
        "description",
        widget=deform.widget.TextAreaWidget(),
        validator=forms.textarea_node_validator,
    )
    customize("cost", typ=AmountType(5), missing=colander.required)
    customize("quantity", typ=QuantityType(), missing=colander.required)
    customize(
        "unity",
        validator=forms.get_deferred_select_validator(WorkUnit, id_key='label'),
        missing=colander.drop,
    )
    customize(
        "tva",
        typ=AmountType(2),
        validator=forms.get_deferred_select_validator(Tva, id_key='value'),
        missing=colander.required,
    )
    customize(
        "product_id",
        validator=forms.get_deferred_select_validator(Product),
        missing=colander.drop,
    )
    return schema


def _customize_tasklinegroup_fields(schema):
    """
    Customize TaskLineGroup colander schema related fields

    :param obj schema: The schema to modify
    """
    # pré-remplissage de la variable schema de la fonction
    # forms.customize_field
    customize = functools.partial(forms.customize_field, schema)
    customize("id", widget=deform.widget.HiddenWidget())
    customize("task_id", missing=colander.required)
    customize("description", widget=deform.widget.TextAreaWidget())
    customize(
        "lines",
        validator=colander.Length(
            min=1,
            min_err=u"Une prestation au moins doit être incluse",
        )
    )
    if 'lines' in schema:
        child_schema = schema['lines'].children[0]
        _customize_taskline_fields(child_schema)

    return schema


def _customize_task_fields(schema):
    """
    Add Field customization to the task form schema

    :param obj schema: The schema to modify
    """
    schema.after_bind = task_after_bind
    customize = functools.partial(forms.customize_field, schema)
    customize("id", widget=deform.widget.HiddenWidget(), missing=colander.drop)

    customize(
        "status",
        widget=deform.widget.SelectWidget(values=zip(ALL_STATES, ALL_STATES)),
        validator=colander.OneOf(ALL_STATES),
    )
    customize(
        "status_comment",
        widget=deform.widget.TextAreaWidget(),
    )
    customize(
        "status_person_id",
        widget=get_deferred_user_choice
    )
    customize(
        "description",
        widget=deform.widget.TextAreaWidget(),
        validator=forms.textarea_node_validator,
        missing=colander.required,
    )
    customize("date", missing=colander.required)
    for field_name in "ht", "ttc", "tva", "expenses_ht":
        customize(
            field_name,
            typ=AmountType(5)
        )

    customize(
        "address",
        widget=deform.widget.TextAreaWidget(),
        validator=forms.textarea_node_validator,
        missing=colander.required,
    )
    customize(
        "workplace",
        widget=deform.widget.TextAreaWidget(),
    )
    customize(
        "payment_conditions",
        widget=deform.widget.TextAreaWidget(),
        validator=forms.textarea_node_validator,
        missing=colander.required,
    )
    customize(
        "mentions",
        children=forms.get_sequence_child_item(TaskMention),
    )
    customize(
        "line_groups",
        validator=colander.Length(min=1, min_err=u"Une entrée est requise"),
        missing=colander.required,
    )
    if 'line_groups' in schema:
        child_schema = schema['line_groups'].children[0]
        _customize_tasklinegroup_fields(child_schema)

    if "discount_lines" in schema:
        child_schema = schema['discount_lines'].children[0]
        _customize_discountline_fields(child_schema)
    return schema


def get_add_edit_discountline_schema(includes=None, excludes=None):
    """
    Return add edit schema for DiscountLine edition

    :param tuple includes: field that should be included (if None,
    excludes will be used instead)
    :param tuple excludes: Model attributes that should be excluded for schema
    generation (if None, a default one is provided)

    :rtype: `colanderalchemy.SQLAlchemySchemaNode`
    """
    if includes is not None:
        excludes = None

    schema = SQLAlchemySchemaNode(
        DiscountLine,
        includes=includes,
        excludes=excludes,
    )
    schema = _customize_discountline_fields(schema)
    return schema


def get_add_edit_taskline_schema(includes=None, excludes=None):
    """
    Return add edit schema for TaskLine edition

    :param tuple includes: field that should be included (if None,
    excludes will be used instead)
    :param tuple excludes: Model attributes that should be excluded for schema
    generation (if None, a default one is provided)

    :rtype: `colanderalchemy.SQLAlchemySchemaNode`
    """
    if includes is not None:
        excludes = None

    schema = SQLAlchemySchemaNode(
        TaskLine,
        includes=includes,
        excludes=excludes,
    )
    schema = _customize_taskline_fields(schema)
    return schema


def get_add_edit_tasklinegroup_schema(includes=None, excludes=None):
    """
    Return add edit schema for TaskLineGroup edition

    :param tuple includes: field that should be included (if None,
    excludes will be used instead)
    :param tuple excludes: Model attributes that should be excluded for schema
    generation (if None, a default one is provided)

    :rtype: `colanderalchemy.SQLAlchemySchemaNode`
    """
    if includes is not None:
        excludes = None

    schema = SQLAlchemySchemaNode(
        TaskLineGroup,
        includes=includes,
        excludes=excludes
    )
    schema = _customize_tasklinegroup_fields(schema)
    return schema


def get_add_edit_task_schema(
    factory, isadmin=False, includes=None, excludes=None, **kw
):
    """
    Return a schema for task edition

    :param class factory: The type of task we want to edit
    :param bool isadmin: Are we asking for an admin schema ?
    :param tuple includes: field that should be included (if None,
    excludes will be used instead)
    :param tuple excludes: Model attributes that should be excluded for schema
    generation (if None, a default one is provided)
    :returns: `colanderalchemy.SQLAlchemySchemaNode`
    """
    if includes is not None:
        excludes = None
    elif excludes is None:
        excludes = (
            'id', 'children', 'parent', "exclude", "phase_id", 'owner_id',
            'company_id', "project_id", "customer_id", "expenses",
        )
        if not isadmin:
            excludes = excludes + ('status',)

    schema = SQLAlchemySchemaNode(
        factory,
        excludes=excludes,
        includes=includes,
        **kw
    )
    schema = _customize_task_fields(schema)
    return schema
