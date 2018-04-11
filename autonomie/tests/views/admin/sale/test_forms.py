# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie.models.payments import PaymentMode
from autonomie.models.task import WorkUnit


def test_payment_mode_success(config, dbsession, get_csrf_request_with_db):
    from autonomie.views.admin.sale.forms import (
        PaymentModeAdminView,
        SALE_URL,
    )
    config.add_route(SALE_URL, '/')
    appstruct = {'datas': [
        {'label': u"Chèque"},
        {'label': u"Expèce"},
    ]}
    view = PaymentModeAdminView(get_csrf_request_with_db())
    view.submit_success(appstruct)
    assert dbsession.query(PaymentMode).count() == 2
    appstruct = {'datas': [
        {'label': u"Chèque"},
    ]}
    view.submit_success(appstruct)
    assert dbsession.query(PaymentMode).count() == 1


def test_workunit_success(config, dbsession, get_csrf_request_with_db):
    from autonomie.views.admin.sale.forms import (
        WorkUnitAdminView,
        SALE_URL,
    )
    config.add_route(SALE_URL, '/')
    appstruct = {'datas': [
        {'label': u"Semaines"},
        {'label': u"Jours"}
    ]}
    view = WorkUnitAdminView(get_csrf_request_with_db())
    view.submit_success(appstruct)
    assert dbsession.query(WorkUnit).count() == 2
    appstruct = {'datas': [
        {'label': u"Semaines"},
    ]}
    view.submit_success(appstruct)
    assert dbsession.query(WorkUnit).count() == 1
