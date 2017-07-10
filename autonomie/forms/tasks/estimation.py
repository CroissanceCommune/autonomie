# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
import deform
from autonomie.models.task.invoice import get_invoice_years
from autonomie.models import company
from autonomie import forms
from autonomie.forms.tasks.lists import (
    PeriodSchema,
    AmountRangeSchema,
    TEMPLATES_URL,
)

from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.task import Estimation


def validate_estimation(estimation_object, request):
    """
    Globally validate an estimation_object

    :param obj estimation_object: An instance of Estimation
    :param obj request: The pyramid request
    :raises: colander.Invalid

    try:
        validate_estimation(est, self.request)
    except colander.Invalid as err:
        error_messages = err.messages
    """
    schema = SQLAlchemySchemaNode(Estimation)
    schema = schema.bind(request=request, translate=False)
    appstruct = estimation_object.__json__(request)
    cstruct = schema.deserialize(appstruct)
    return cstruct


STATUS_OPTIONS = (
    ('all', u"Tous les devis", ),
    ('waiting', u"Devis en cours", ),
    ('signed', u'Devis signé'),
    ('geninv', u"Devis concrétisés (avec facture)", ),
    ('aborted', u"Devis annulés", ),
)


def get_list_schema(is_global=False):
    """
    Return the estimation list schema

    :param bool is_global: Should we include global search fields (CAE wide)
    :returns: The list schema
    :rtype: colander.SchemaNode
    """
    schema = forms.lists.BaseListsSchema().clone()

    del schema['search']

    schema.insert(0, company.customer_node(is_global))

    if is_global:
        schema.insert(
            0,
            company.company_node(
                name='company_id',
                missing=colander.drop,
                widget_options={'default': ('', u'Toutes les entreprises')}
            )
        )

    schema.insert(
        0,
        PeriodSchema(
            name='period',
            title="",
            validator=colander.Function(
                forms.range_validator,
                msg=u"La date de début doit précéder la date de début"
            ),
            widget=deform.widget.MappingWidget(
                template=TEMPLATES_URL + 'clean_mapping.pt',
            ),
            missing=colander.drop,
        )
    )
    schema.insert(
        0,
        AmountRangeSchema(
            name='ttc',
            title="",
            validator=colander.Function(
                forms.range_validator,
                msg=u"Le montant de départ doit être inférieur ou égale \
à celui de la fin"
            ),
            widget=deform.widget.MappingWidget(
                template=TEMPLATES_URL + 'clean_mapping.pt',
            ),
            missing=colander.drop,
        )
    )

    schema.insert(0, colander.SchemaNode(
        colander.String(),
        name='status',
        widget=deform.widget.SelectWidget(values=STATUS_OPTIONS),
        validator=colander.OneOf([s[0] for s in STATUS_OPTIONS]),
        default='all',
        missing='all'
    ))
    node = forms.year_select_node(
        name='year',
        query_func=get_invoice_years,
    )
    schema.insert(0, node)

    return schema
