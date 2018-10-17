# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie.models.services.business_status import BusinessStatusService


def test_populate_indicators(business):
    BusinessStatusService.populate_indicators(business)
    indicator = business.indicators[0]
    assert indicator.label == u"Facturation"
    assert indicator.status == u"danger"
    assert indicator.name == "invoiced"


def test_update_invoicing_indicator(business, invoice):
    from autonomie.models.services.business import BusinessService
    BusinessService.populate_deadlines(business)
    BusinessStatusService.populate_indicators(business)

    BusinessStatusService.update_invoicing_indicator(business)
    assert business.indicators[0].status == u"danger"

    for deadline in business.payment_deadlines:
        deadline.invoiced = True

    BusinessStatusService.update_invoicing_indicator(business)
    assert business.indicators[0].status == u"success"


def test_update_invoicing_status(dbsession, business, invoice):
    from autonomie.models.services.business import BusinessService
    BusinessService.populate_deadlines(business)

    deadline = business.payment_deadlines[0]
    deadline.invoice = invoice
    dbsession.merge(deadline)
    dbsession.flush()
    BusinessStatusService.update_invoicing_status(business, invoice)
    assert deadline.invoiced is True


def test_compute_status(business):
    BusinessStatusService.populate_indicators(business)
    assert BusinessStatusService._compute_status(business) == u"danger"

    for indicator in business.indicators:
        indicator.status = indicator.SUCCESS_STATUS

    assert BusinessStatusService._compute_status(business) == u"success"


def test_update_status(business):
    BusinessStatusService.populate_indicators(business)

    for indicator in business.indicators:
        indicator.status = indicator.SUCCESS_STATUS

    BusinessStatusService.update_status(business) == u"success"
    assert business.status == "success"
