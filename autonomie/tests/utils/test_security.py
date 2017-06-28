# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest
from autonomie.tests.tools import (
    Dummy,
    check_acl,
)


@pytest.fixture
def dummy_company():
    user1 = Dummy(login='user1')
    company = Dummy(employees=[user1])
    return company


@pytest.fixture
def estimation(dummy_company):
    return Dummy(
        status='draft',
        company=dummy_company,
        signed_status='waiting',
        geninv=False,
    )


@pytest.fixture
def invoice(dummy_company):
    return Dummy(
        status='draft',
        company=dummy_company,
        paid_status='waiting',
        exported=False,
    )


def test_estimation_default_acls(estimation, dummy_company):
    from autonomie.utils.security import get_estimation_default_acl

    # Draft acls
    acl = get_estimation_default_acl(estimation)
    # User
    assert check_acl(acl, 'wait.estimation', 'user1')
    assert check_acl(acl, 'edit.estimation', 'user1')
    assert check_acl(acl, 'delete.estimation', 'user1')
    assert not check_acl(acl, 'geninv.estimation', 'user1')
    assert not check_acl(acl, 'set_signed_status.estimation', 'user1')
    assert not check_acl(acl, 'valid.estimation', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager',
                  'group:estimation_validation'):
        assert check_acl(acl, 'valid.estimation', group)
        assert not check_acl(acl, 'geninv.estimation', group)
        assert not check_acl(acl, 'set_signed_status.estimation', group)

    # Wait acls
    estimation.status = 'wait'
    acl = get_estimation_default_acl(estimation)
    # #  User
    assert not check_acl(acl, 'edit.estimation', 'user1')
    assert not check_acl(acl, 'set_date.estimation', 'user1')
    assert not check_acl(acl, 'geninv.estimation')
    assert not check_acl(acl, 'set_signed_status.estimation')
    assert not check_acl(acl, 'valid.estimation', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert check_acl(acl, 'valid.estimation', group)
        assert check_acl(acl, 'edit.estimation', group)
        assert check_acl(acl, 'delete.estimation', group)
        assert not check_acl(acl, 'geninv.estimation', group)
        assert not check_acl(acl, 'set_signed_status.estimation', group)

    # Valid acls
    estimation.status = 'valid'
    acl = get_estimation_default_acl(estimation)
    # # User
    assert not check_acl(acl, 'edit.estimation', 'user1')
    assert not check_acl(acl, 'set_date.estimation', 'user1')
    assert not check_acl(acl, 'delete.estimation', 'user1')
    assert check_acl(acl, 'geninv.estimation', 'user1')
    assert check_acl(acl, 'set_signed_status.estimation', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert not check_acl(acl, 'edit.estimation', group)
        assert not check_acl(acl, 'delete.estimation', group)
        assert check_acl(acl, 'geninv.estimation', group)
        assert check_acl(acl, 'set_signed_status.estimation', group)

    # Aborted acls
    estimation.signed_status = 'aborted'

    acl = get_estimation_default_acl(estimation)
    # # User
    assert not check_acl(acl, 'geninv.estimation', 'user1')
    assert check_acl(acl, 'set_signed_status.estimation', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert not check_acl(acl, 'geninv.estimation', group)
        assert check_acl(acl, 'set_signed_status.estimation', group)

    # Signed acls
    estimation.signed_status = 'signed'
    acl = get_estimation_default_acl(estimation)
    # # User
    assert check_acl(acl, 'geninv.estimation', 'user1')
    assert check_acl(acl, 'set_signed_status.estimation', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert check_acl(acl, 'geninv.estimation', group)
        assert check_acl(acl, 'set_signed_status.estimation', group)
        assert not check_acl(acl, 'set_date.estimation', group)

    # geninv acls
    estimation.signed_status = 'waiting'
    estimation.geninv = True
    acl = get_estimation_default_acl(estimation)
    # # User
    assert check_acl(acl, 'geninv.estimation', 'user1')
    assert check_acl(acl, 'set_signed_status.estimation', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert check_acl(acl, 'geninv.estimation', group)
        assert check_acl(acl, 'set_signed_status.estimation', group)
        assert not check_acl(acl, 'set_date.estimation', group)


def test_invoice_default_acls(invoice, dummy_company):
    from autonomie.utils.security import get_invoice_default_acl

    # Draft acls
    acl = get_invoice_default_acl(invoice)
    # User
    assert check_acl(acl, 'wait.invoice', 'user1')
    assert check_acl(acl, 'edit.invoice', 'user1')
    assert check_acl(acl, 'delete.invoice', 'user1')
    assert not check_acl(acl, 'gencinv.invoice', 'user1')
    assert not check_acl(acl, 'valid.invoice', 'user1')
    assert not check_acl(acl, 'add_payment.invoice', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager',
                  'group:invoice_validation'):
        assert check_acl(acl, 'valid.invoice', group)
        assert not check_acl(acl, 'gencinv.invoice', group)
        assert not check_acl(acl, 'add_payment.invoice', group)

    # Wait acls
    invoice.status = 'wait'
    acl = get_invoice_default_acl(invoice)
    # #  User
    assert check_acl(acl, 'view.invoice', 'user1')
    assert not check_acl(acl, 'edit.invoice', 'user1')
    assert not check_acl(acl, 'set_date.invoice', 'user1')
    assert not check_acl(acl, 'gencinv.invoice')
    assert not check_acl(acl, 'valid.invoice', 'user1')
    assert not check_acl(acl, 'add_payment.invoice', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert check_acl(acl, 'edit.invoice', group)
        assert check_acl(acl, 'delete.invoice', group)
        assert check_acl(acl, 'valid.invoice', group)
        assert not check_acl(acl, 'gencinv.invoice', group)
        assert not check_acl(acl, 'add_payment.invoice', group)

    # Valid acls
    invoice.status = 'valid'
    acl = get_invoice_default_acl(invoice)
    # # User
    assert not check_acl(acl, 'edit.invoice', 'user1')
    assert not check_acl(acl, 'set_date.invoice', 'user1')
    assert not check_acl(acl, 'delete.invoice', 'user1')
    assert check_acl(acl, 'gencinv.invoice', 'user1')
    assert not check_acl(acl, 'add_payment.invoice', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert not check_acl(acl, 'edit.invoice', group)
        assert not check_acl(acl, 'delete.invoice', group)
        assert check_acl(acl, 'set_date.invoice', group)
        assert check_acl(acl, 'gencinv.invoice', group)

    # Paid acls
    invoice.paid_status = 'paid'

    acl = get_invoice_default_acl(invoice)
    # # User
    assert check_acl(acl, 'gencinv.invoice', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert check_acl(acl, 'gencinv.invoice', group)
        assert check_acl(acl, 'add_payment.invoice', group)
        assert not check_acl(acl, 'set_date.invoice', group)

    # Resulted acls
    invoice.paid_status = 'resulted'
    acl = get_invoice_default_acl(invoice)
    # # User
    assert not check_acl(acl, 'gencinv.invoice', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert not check_acl(acl, 'gencinv.invoice', group)
        assert not check_acl(acl, 'add_payment.invoice', group)
        assert not check_acl(acl, 'set_date.invoice', group)

    # exported acls
    invoice.paid_status = 'waiting'
    invoice.exported = True
    acl = get_invoice_default_acl(invoice)
    # # User
    assert check_acl(acl, 'gencinv.invoice', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert check_acl(acl, 'gencinv.invoice', group)
        assert check_acl(acl, 'add_payment.invoice', group)
        assert not check_acl(acl, 'set_date.invoice', group)
        assert not check_acl(acl, 'set_treasury.invoice', group)
