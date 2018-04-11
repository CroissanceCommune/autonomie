# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie.models import tva
from autonomie.views.admin.sale.tva import TVA_URL


def test_tva_add_view_success(config, get_csrf_request_with_db, dbsession):
    from autonomie.views.admin.sale.tva import TvaAddView
    TvaAddView.back_link = TVA_URL
    config.add_route(TVA_URL, '/')

    appstruct = {
        'name': "test",
        'value': 0,
        "default": True,
        "mention": "Test",
        "products": []
    }
    view = TvaAddView(get_csrf_request_with_db())
    view.submit_success(appstruct)

    assert dbsession.query(tva.Tva).filter(tva.Tva.name == 'test').count() == 1


def test_tva_edit_view_success(config, get_csrf_request_with_db, dbsession,
                               tva):
    from autonomie.views.admin.sale.tva import TvaEditView
    config.add_route(TVA_URL, '/')
    TvaEditView.back_link = TVA_URL
    appstruct = {
        'name': "21%", 'value': 2100, "default": True, 'products': []
    }
    request = get_csrf_request_with_db()
    request.context = tva
    view = TvaEditView(request)
    view.submit_success(appstruct)

    assert tva.name == '21%'


def test_tva_disable_view_sucess(config, get_csrf_request_with_db, dbsession,
                                 tva):
    from autonomie.views.admin.sale.tva import TvaDisableView
    config.add_route(TVA_URL, '/')
    TvaDisableView.back_link = TVA_URL
    request = get_csrf_request_with_db()
    request.context = tva
    view = TvaDisableView(request)
    view.__call__()
    assert not tva.active
