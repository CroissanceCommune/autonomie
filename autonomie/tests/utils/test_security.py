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
        type_='estimation',
    )


@pytest.fixture
def invoice(dummy_company):
    return Dummy(
        status='draft',
        company=dummy_company,
        paid_status='waiting',
        exported=False,
        type_='invoice',
    )


@pytest.fixture
def cancelinvoice(dummy_company):
    return Dummy(
        status='draft',
        company=dummy_company,
        exported=False,
        type_='cancelinvoice',
    )


@pytest.fixture
def expense_sheet(dummy_company):
    return Dummy(
        status='draft',
        company=dummy_company,
        paid_status='waiting',
        exported=False,
        type_='expensesheet',
    )


def test_estimation_default_acls(estimation, dummy_company):
    from autonomie.utils.security import get_estimation_default_acl

    # Draft acls
    acl = get_estimation_default_acl(estimation)
    # User
    for ace in ('wait.estimation', 'edit.estimation', 'delete.estimation',
                'draft.estimation', 'add.file', 'view.file'):
        assert check_acl(acl, ace, 'user1')
    assert not check_acl(acl, 'valid.estimation', 'user1')

    assert not check_acl(acl, 'geninv.estimation', 'user1')
    assert not check_acl(acl, 'set_signed_status.estimation', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        for ace in ('edit.estimation', 'delete.estimation',
                    'draft.estimation', 'add.file', 'view.file'):
            assert check_acl(acl, ace, group)

        assert check_acl(acl, 'valid.estimation', group)
        assert not check_acl(acl, 'wait.estimation', group)

        assert not check_acl(acl, 'geninv.estimation', group)
        assert not check_acl(acl, 'set_signed_status.estimation', group)

    # Invalid acls
    estimation.status = 'invalid'
    acl = get_estimation_default_acl(estimation)
    # User
    for ace in ('wait.estimation', 'edit.estimation', 'delete.estimation',
                'draft.estimation', 'add.file', 'view.file'):
        assert check_acl(acl, ace, 'user1')
    assert not check_acl(acl, 'valid.estimation', 'user1')

    assert not check_acl(acl, 'geninv.estimation', 'user1')
    assert not check_acl(acl, 'set_signed_status.estimation', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        for ace in ('edit.estimation', 'delete.estimation',
                    'draft.estimation', 'add.file', 'view.file'):
            assert check_acl(acl, ace, group)

        assert check_acl(acl, 'valid.estimation', group)
        assert not check_acl(acl, 'wait.estimation', group)

        assert not check_acl(acl, 'geninv.estimation', group)
        assert not check_acl(acl, 'set_signed_status.estimation', group)
    assert check_acl(acl, 'valid.estimation', 'group:estimation_validation')

    # Wait acls
    estimation.status = 'wait'
    acl = get_estimation_default_acl(estimation)
    # #  User
    assert check_acl(acl, 'draft.estimation', 'user1')
    assert not check_acl(acl, 'wait.estimation', 'user1')
    assert not check_acl(acl, 'edit.estimation', 'user1')
    assert not check_acl(acl, 'valid.estimation', 'user1')

    assert not check_acl(acl, 'set_date.estimation', 'user1')
    assert not check_acl(acl, 'geninv.estimation', 'user1')
    assert not check_acl(acl, 'set_signed_status.estimation', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert check_acl(acl, 'valid.estimation', group)
        assert check_acl(acl, 'invalid.estimation', group)
        assert check_acl(acl, 'edit.estimation', group)
        assert check_acl(acl, 'delete.estimation', group)
        assert check_acl(acl, 'draft.estimation', 'user1')
        assert not check_acl(acl, 'geninv.estimation', group)
        assert not check_acl(acl, 'set_signed_status.estimation', group)

    # Valid acls
    estimation.status = 'valid'
    acl = get_estimation_default_acl(estimation)
    # # User
    assert not check_acl(acl, 'edit.estimation', 'user1')
    assert not check_acl(acl, 'delete.estimation', 'user1')

    assert not check_acl(acl, 'set_date.estimation', 'user1')
    assert check_acl(acl, 'geninv.estimation', 'user1')
    assert check_acl(acl, 'set_signed_status.estimation', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert not check_acl(acl, 'edit.estimation', group)
        assert not check_acl(acl, 'delete.estimation', group)

        assert check_acl(acl, 'set_date.estimation', group)
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
    # status related acl
    for ace in (
        'wait.invoice', 'edit.invoice', 'delete.invoice',
        'view.file', 'add.file'
    ):
        assert check_acl(acl, ace, 'user1')
    assert not check_acl(acl, 'valid.invoice', 'user1')
    # specific acl
    assert not check_acl(acl, 'gencinv.invoice', 'user1')
    assert not check_acl(acl, 'add_payment.invoice', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        for ace in (
            'edit.invoice', 'delete.invoice',
            'view.file', 'add.file'
        ):
            assert check_acl(acl, ace, group)

        assert check_acl(acl, 'valid.invoice', group)
        assert not check_acl(acl, 'wait.invoice', group)
        assert not check_acl(acl, 'gencinv.invoice', group)
        assert not check_acl(acl, 'add_payment.invoice', group)
    assert check_acl(acl, 'valid.invoice', 'group:invoice_validation')

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
    assert check_acl(acl, 'add.file', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert check_acl(acl, 'edit.invoice', group)
        assert check_acl(acl, 'delete.invoice', group)
        assert check_acl(acl, 'valid.invoice', group)
        assert not check_acl(acl, 'gencinv.invoice', group)
        assert not check_acl(acl, 'add_payment.invoice', group)
        assert check_acl(acl, 'add.file', group)

    # Valid acls
    invoice.status = 'valid'
    acl = get_invoice_default_acl(invoice)
    # # User
    assert not check_acl(acl, 'edit.invoice', 'user1')
    assert not check_acl(acl, 'set_date.invoice', 'user1')
    assert not check_acl(acl, 'delete.invoice', 'user1')
    assert check_acl(acl, 'gencinv.invoice', 'user1')
    assert check_acl(acl, 'view.invoice', 'user1')
    assert not check_acl(acl, 'add_payment.invoice', 'user1')
    assert check_acl(acl, 'add.file', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert not check_acl(acl, 'edit.invoice', group)
        assert not check_acl(acl, 'delete.invoice', group)
        assert check_acl(acl, 'view.invoice', group)
        assert check_acl(acl, 'set_date.invoice', group)
        assert check_acl(acl, 'gencinv.invoice', group)
        assert check_acl(acl, 'add.file', group)

    # Paid acls
    invoice.paid_status = 'paid'

    acl = get_invoice_default_acl(invoice)
    # # User
    assert check_acl(acl, 'gencinv.invoice', 'user1')
    assert check_acl(acl, 'add.file', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert check_acl(acl, 'gencinv.invoice', group)
        assert check_acl(acl, 'add_payment.invoice', group)
        assert not check_acl(acl, 'set_date.invoice', group)
        assert check_acl(acl, 'add.file', group)

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
        assert check_acl(acl, 'add.file', group)

    # exported acls
    invoice.paid_status = 'waiting'
    invoice.exported = True
    acl = get_invoice_default_acl(invoice)
    # # User
    assert check_acl(acl, 'gencinv.invoice', 'user1')
    assert check_acl(acl, 'add.file', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert check_acl(acl, 'gencinv.invoice', group)
        assert check_acl(acl, 'add_payment.invoice', group)
        assert not check_acl(acl, 'set_date.invoice', group)
        assert not check_acl(acl, 'set_treasury.invoice', group)
        assert check_acl(acl, 'add.file', group)


def test_cancelinvoice_default_acls(cancelinvoice, dummy_company):
    from autonomie.utils.security import get_cancelinvoice_default_acl

    # Draft acls
    acl = get_cancelinvoice_default_acl(cancelinvoice)
    # User
    # status related acl
    for ace in (
        'wait.cancelinvoice', 'edit.cancelinvoice', 'delete.cancelinvoice',
        'view.file', 'add.file'
    ):
        assert check_acl(acl, ace, 'user1')
    assert not check_acl(acl, 'valid.cancelinvoice', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        for ace in (
            'edit.cancelinvoice', 'delete.cancelinvoice',
            'view.file', 'add.file'
        ):
            assert check_acl(acl, ace, group)

        assert check_acl(acl, 'valid.cancelinvoice', group)
        assert not check_acl(acl, 'wait.cancelinvoice', group)
    assert check_acl(acl, 'valid.cancelinvoice', 'group:invoice_validation')

    # Wait acls
    cancelinvoice.status = 'wait'
    acl = get_cancelinvoice_default_acl(cancelinvoice)
    # #  User
    assert check_acl(acl, 'view.cancelinvoice', 'user1')
    assert not check_acl(acl, 'edit.cancelinvoice', 'user1')
    assert not check_acl(acl, 'set_date.cancelinvoice', 'user1')
    assert not check_acl(acl, 'valid.cancelinvoice', 'user1')
    assert check_acl(acl, 'add.file', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert check_acl(acl, 'edit.cancelinvoice', group)
        assert check_acl(acl, 'delete.cancelinvoice', group)
        assert check_acl(acl, 'valid.cancelinvoice', group)
        assert check_acl(acl, 'add.file', group)

    # Valid acls
    cancelinvoice.status = 'valid'
    acl = get_cancelinvoice_default_acl(cancelinvoice)
    # # User
    assert not check_acl(acl, 'edit.cancelinvoice', 'user1')
    assert not check_acl(acl, 'set_date.cancelinvoice', 'user1')
    assert not check_acl(acl, 'delete.cancelinvoice', 'user1')
    assert check_acl(acl, 'view.cancelinvoice', 'user1')
    assert check_acl(acl, 'add.file', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert not check_acl(acl, 'edit.cancelinvoice', group)
        assert not check_acl(acl, 'delete.cancelinvoice', group)
        assert check_acl(acl, 'view.cancelinvoice', group)
        assert check_acl(acl, 'set_date.cancelinvoice', group)
        assert check_acl(acl, 'add.file', group)

    # exported acls
    cancelinvoice.exported = True
    acl = get_cancelinvoice_default_acl(cancelinvoice)
    # # User

    assert check_acl(acl, 'add.file', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert not check_acl(acl, 'set_date.cancelinvoice', group)
        assert not check_acl(acl, 'set_treasury.cancelinvoice', group)
        assert check_acl(acl, 'add.file', group)


def test_expense_sheet_default_acls(expense_sheet, dummy_company):
    from autonomie.utils.security import get_expense_sheet_default_acl

    acl = get_expense_sheet_default_acl(expense_sheet)

    # User
    # status related acl
    for ace in (
        'wait.expensesheet', 'edit.expensesheet', 'delete.expensesheet',
        'view.file', 'add.file'
    ):
        assert check_acl(acl, ace, 'user1')
    assert not check_acl(acl, 'valid.expensesheet', 'user1')
    # specific acl
    assert not check_acl(acl, 'add_payment.expensesheet', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        for ace in (
            'edit.expensesheet', 'delete.expensesheet',
            'view.file', 'add.file'
        ):
            assert check_acl(acl, ace, group)

        assert check_acl(acl, 'valid.expensesheet', group)
        assert not check_acl(acl, 'wait.expensesheet', group)
        assert not check_acl(acl, 'add_payment.expensesheet', group)

    # Wait acls
    expense_sheet.status = 'wait'
    acl = get_expense_sheet_default_acl(expense_sheet)
    # #  User
    assert check_acl(acl, 'view.expensesheet', 'user1')
    assert not check_acl(acl, 'edit.expensesheet', 'user1')
    assert not check_acl(acl, 'valid.expensesheet', 'user1')
    assert not check_acl(acl, 'add_payment.expensesheet', 'user1')
    assert check_acl(acl, 'add.file', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert check_acl(acl, 'edit.expensesheet', group)
        assert check_acl(acl, 'delete.expensesheet', group)
        assert check_acl(acl, 'valid.expensesheet', group)
        assert not check_acl(acl, 'add_payment.expensesheet', group)
        assert check_acl(acl, 'add.file', group)

    # Valid acls
    expense_sheet.status = 'valid'
    acl = get_expense_sheet_default_acl(expense_sheet)
    # # User
    assert not check_acl(acl, 'edit.expensesheet', 'user1')
    assert not check_acl(acl, 'delete.expensesheet', 'user1')
    assert check_acl(acl, 'view.expensesheet', 'user1')
    assert not check_acl(acl, 'add_payment.expensesheet', 'user1')
    assert check_acl(acl, 'add.file', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert not check_acl(acl, 'edit.expensesheet', group)
        assert not check_acl(acl, 'delete.expensesheet', group)
        assert check_acl(acl, 'view.expensesheet', group)
        assert check_acl(acl, 'add.file', group)

    # Paid acls
    expense_sheet.paid_status = 'paid'

    acl = get_expense_sheet_default_acl(expense_sheet)
    # # User
    assert check_acl(acl, 'add.file', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert check_acl(acl, 'add_payment.expensesheet', group)
        assert check_acl(acl, 'add.file', group)

    # Resulted acls
    expense_sheet.paid_status = 'resulted'
    acl = get_expense_sheet_default_acl(expense_sheet)
    # # User

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert not check_acl(acl, 'add_payment.expensesheet', group)
        assert check_acl(acl, 'add.file', group)

    # exported acls
    expense_sheet.paid_status = 'waiting'
    expense_sheet.exported = True
    acl = get_expense_sheet_default_acl(expense_sheet)
    # # User
    assert check_acl(acl, 'add.file', 'user1')

    # # Admins
    for group in ('group:admin', 'group:manager'):
        assert check_acl(acl, 'add_payment.expensesheet', group)
        assert not check_acl(acl, 'set_treasury.expensesheet', group)
        assert check_acl(acl, 'add.file', group)
