# -*- coding: utf-8 -*-
"""
Schema used for trainings manipulation
"""
import colander
from autonomie.forms.lists import BaseListsSchema
from autonomie.forms.company import (
    customer_filter_node_factory,
    company_filter_node_factory,
)


def get_training_list_schema(is_admin):
    """
    Build the Training list filter schema
    """
    schema = BaseListsSchema().clone()
    schema['search'].description = u"Numéro de facture"
    schema.add_before(
        "items_per_page",
        company_filter_node_factory(name='company_id')
    )
    schema.add_before(
        "items_per_page",
        customer_filter_node_factory(name='customer_id', is_admin=is_admin)
    )
    schema.add_before(
        "items_per_page",
        colander.SchemaNode(
            colander.Boolean(),
            name="include_closed",
            label=u"Inclure les affaires clôturées",
            missing=False
        )
    )
    return schema
