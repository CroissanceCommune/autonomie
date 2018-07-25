# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie.views.project.routes import PROJECT_ITEM_ROUTE

def test_invoice_valid_view(
    config, get_csrf_request_with_db, full_invoice, user
):
    config.add_route(PROJECT_ITEM_ROUTE, PROJECT_ITEM_ROUTE)
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True
    )
    from autonomie.views.invoices.rest_api import InvoiceStatusRestView

    request = get_csrf_request_with_db(
        post={'submit': 'valid', 'comment': u"Test comment"}
    )
    request.context = full_invoice
    request.user = user
    request.is_xhr = True

    view = InvoiceStatusRestView(request)
    result = view.__call__()
    assert result == {
        'redirect': PROJECT_ITEM_ROUTE.format(id=full_invoice.project_id)}
    assert full_invoice.status == 'valid'
    assert full_invoice.statuses[-1].status_comment == u"Test comment"
    assert full_invoice.statuses[-1].status_code == 'valid'


def test_cancelinvoice_valid_view(
    config, get_csrf_request_with_db, full_cancelinvoice, full_invoice, user
):
    config.add_route(PROJECT_ITEM_ROUTE, PROJECT_ITEM_ROUTE)
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True
    )
    from autonomie.views.invoices.rest_api import CancelInvoiceStatusRestView

    request = get_csrf_request_with_db(
        post={'submit': 'valid', 'comment': u"Test comment"}
    )
    request.context = full_cancelinvoice
    request.user = user
    request.is_xhr = True

    view = CancelInvoiceStatusRestView(request)
    result = view.__call__()
    assert result == {
        'redirect': PROJECT_ITEM_ROUTE.format(id=full_cancelinvoice.project_id)
    }
    assert full_cancelinvoice.status == 'valid'
    assert full_cancelinvoice.statuses[-1].status_comment == u"Test comment"
    assert full_cancelinvoice.statuses[-1].status_code == 'valid'
    assert full_invoice.paid_status == 'resulted'
