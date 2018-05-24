# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest


@pytest.fixture
def estimation(
    dbsession,
    tva,
    unity,
    project,
    customer,
    company,
    user,
    phase,
):
    from autonomie.models.task.estimation import Estimation
    estimation = Estimation(
        company=company,
        project=project,
        customer=customer,
        user=user,
        phase=phase,
    )
    dbsession.add(estimation)
    dbsession.flush()
    return estimation


@pytest.fixture
def invoice(
    dbsession,
    tva,
    unity,
    project,
    customer,
    company,
    user,
    phase,
):
    from autonomie.models.task.invoice import Invoice
    invoice = Invoice(
        company=company,
        project=project,
        customer=customer,
        user=user,
        phase=phase,
    )
    dbsession.add(invoice)
    dbsession.flush()
    return invoice


@pytest.fixture
def cancelinvoice(
    dbsession,
    tva,
    unity,
    project,
    customer,
    company,
    user,
    phase,
):
    from autonomie.models.task.invoice import CancelInvoice
    cancelinvoice = CancelInvoice(
        company=company,
        project=project,
        customer=customer,
        user=user,
        phase=phase,
    )
    dbsession.add(cancelinvoice)
    dbsession.flush()
    return cancelinvoice
