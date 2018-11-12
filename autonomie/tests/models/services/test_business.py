# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie.models.services.business import BusinessService


def test_to_invoice(business, full_estimation):
    assert BusinessService.to_invoice(business) == full_estimation.ht


def test_populate_deadlines(business, full_estimation):
    BusinessService.populate_deadlines(business)
    assert len(business.payment_deadlines) == 3
    for deadline in business.payment_deadlines:
        assert deadline.invoiced is False
    assert business.status == "danger"


def test_populate_find_deadline(business):
    BusinessService.populate_deadlines(business)
    id_ = business.payment_deadlines[1].id
    assert BusinessService.find_deadline(business, id_) == \
        business.payment_deadlines[1]


def test_find_deadline_from_invoice(dbsession, business, invoice):
    BusinessService.populate_deadlines(business)
    business.payment_deadlines[1].invoice = invoice
    dbsession.merge(business.payment_deadlines[1])
    dbsession.flush()

    assert BusinessService.find_deadline_from_invoice(business, invoice) == \
        business.payment_deadlines[1]


def test_gen_invoices_one(business, full_estimation, user):
    BusinessService.populate_deadlines(business)

    invoices = BusinessService.gen_invoices(
        business,
        user,
        business.payment_deadlines[1]
    )
    assert len(invoices) == 1
    assert business.payment_deadlines[1].invoice == invoices[0]


def test_gen_invoices_all(business, full_estimation, user):
    BusinessService.populate_deadlines(business)

    invoices = BusinessService.gen_invoices(
        business,
        user,
    )
    assert len(invoices) == 3
    for i in range(2):
        assert business.payment_deadlines[i].invoice == invoices[i]


def test_is_visible(dbsession, business, project, mk_project_type):
    business.project = project
    dbsession.merge(business)
    assert BusinessService.is_default_project_type(business) == True
    project.project_type = mk_project_type(name="newone")
    dbsession.merge(project)
    assert BusinessService.is_default_project_type(business) == False
