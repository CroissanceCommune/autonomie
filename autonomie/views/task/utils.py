# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Common utilities used for task edition
"""
from autonomie.models.task import (
    PaymentConditions,
    WorkUnit,
)
from autonomie.models.tva import (
    Tva,
    Product,
)


def json_mentions(request):
    """
    Return the taskmentions available for the task related forms

    :param obj request: The current request object
    :returns: List of TaskMention in their json repr
    """
    context = request.context
    doctype = context.type_
    business_type = context.business_type
    mentions = business_type.optionnal_mentions(doctype)
    return [item.__json__(request) for item in mentions]


def json_tvas(request):
    """
    Return the tva objects available for this form

    :param obj request: The current request object
    :returns: List of Tva objects in their json repr
    """
    query = Tva.query()
    return [item.__json__(request) for item in query]


def json_products(request):
    """
    Return the product objects available for this form

    :param obj request: The current request object
    :returns: List of Product objects in their json repr
    """
    query = Product.query()
    return [item.__json__(request) for item in query]


def json_workunits(request):
    """
    Return the workunit objects available for the given form

    :param obj request: The current request object
    :returns: List of Workunits in their json repr
    """
    query = WorkUnit.query()
    return [item.__json__(request) for item in query]


def json_payment_conditions(request):
    """
    Return The PaymentConditions objects available for the given form

    :param obj request: The current request object
    :returns: List of PaymentConditions in their json repr
    """
    query = PaymentConditions.query()
    return [item.__json__(request) for item in query]
