# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
from autonomie.models.project.business import Business
from autonomie.models.task import (Estimation, Invoice, CancelInvoice)
from autonomie.models.indicators import (
    CustomBusinessIndicator,
    SaleFileRequirement,
)


logger = logging.getLogger(__name__)


class IndicatorChanged:
    """
    Fired when an indicator is forced or if it has a status and the status was
    set
    """
    def __init__(self, request, indicator):
        self.request = request
        self.indicator = indicator


def on_indicator_change(event):
    logger.debug(u"On indicator change")
    if isinstance(event.indicator, SaleFileRequirement):
        logger.debug(u"The indicator is a SaleFileRequirement")
        node = event.indicator.node
        if isinstance(node, Business):
            businesses = [node]
        elif isinstance(node, Estimation):
            businesses = node.businesses
        elif isinstance(node, (Invoice, CancelInvoice)):
            businesses = [node.business]
        else:
            raise Exception(u"Unexpected {}".format(type(event.indicator.node)))
        for business in businesses:
            business.status_service.update_status(business)

    elif isinstance(event.indicator, CustomBusinessIndicator):
        logger.debug(u"The indicator is a CustomBusinessIndicator")
        business = event.indicator.business
        business.status_service.update_status(business)


def includeme(config):
    config.add_subscriber(on_indicator_change, IndicatorChanged)
