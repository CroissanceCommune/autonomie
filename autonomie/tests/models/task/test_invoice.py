# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import datetime
import pytest
import colander

def test_set_numbers(invoice, cancelinvoice):
    invoice.date = datetime.date(2012, 12, 1)
    invoice.set_numbers(15, 1)
    assert invoice.internal_number == u"Company 2012-12 F15"
    assert invoice.name == u"Facture 1"

    cancelinvoice.date = datetime.date(2012, 12, 1)
    cancelinvoice.set_numbers(15, 5)
    assert cancelinvoice.name == u"Avoir 5"
    assert cancelinvoice.internal_number == u"Company 2012-12 A15"


def test_set_deposit_label(invoice):
    invoice.set_numbers(5, 8)
    invoice.set_deposit_label()
    assert invoice.name == u"Facture d'acompte 8"


def test_set_sold_label(invoice):
    invoice.set_numbers(5, 8)
    invoice.set_sold_label()
    assert invoice.name == u"Facture de solde 8"


def test_duplicate_invoice(dbsession, full_invoice, user):
    newinvoice = full_invoice.duplicate(
        user=user,
        project=full_invoice.project,
        phase=full_invoice.phase,
        customer=full_invoice.customer,
    )
    assert len(full_invoice.default_line_group.lines) == len(
        newinvoice.default_line_group.lines
    )
    assert len(full_invoice.discounts) == len(newinvoice.discounts)
    assert newinvoice.project == full_invoice.project
    assert newinvoice.company == full_invoice.company
    assert newinvoice.status_person == user
    assert newinvoice.phase == full_invoice.phase
    assert newinvoice.mentions == full_invoice.mentions
    for key in "customer", "address", "expenses_ht", "workplace":
        assert getattr(newinvoice, key) == getattr(full_invoice, key)


def test_duplicate_invoice_financial_year(dbsession, full_invoice, user):
    full_invoice.financial_year = 1900
    newinvoice = full_invoice.duplicate(
        user=full_invoice.owner,
        project=full_invoice.project,
        phase=full_invoice.phase,
        customer=full_invoice.customer,
    )
    assert newinvoice.financial_year == datetime.date.today().year


def test_duplicate_invoice_integration(dbsession, invoice):
    dbsession.add(invoice)
    dbsession.flush()
    newest = invoice.duplicate(
        user=invoice.owner,
        project=invoice.project,
        phase=invoice.phase,
        customer=invoice.customer,
    )
    dbsession.add(newest)
    dbsession.flush()
    assert newest.phase_id == invoice.phase_id
    assert newest.owner_id == invoice.owner_id
    assert newest.status_person_id == invoice.status_person_id
    assert newest.project_id == invoice.project_id
    assert newest.company_id == invoice.company_id


def test_valid_invoice(config, dbsession, invoice, request_with_config, user):
    request_with_config.user = user
    dbsession.add(invoice)
    dbsession.flush()
    config.testing_securitypolicy(userid='test', permissive=True)

    invoice.set_status('wait', request_with_config)
    dbsession.merge(invoice)
    dbsession.flush()
    invoice.set_status('valid', request_with_config)
    assert invoice.official_number == 1


def test_official_number_distinct_year(
    config, dbsession, invoice, request_with_config,
    user
):
    request_with_config.user = invoice.owner
    invoice2 = invoice.duplicate(
        user=invoice.owner,
        project=invoice.project,
        phase=invoice.phase,
        customer=invoice.customer
    )
    invoice.official_number = 150
    invoice.date = datetime.date(2017, 12, 30)
    dbsession.add(invoice)
    dbsession.flush()

    invoice2.date = datetime.date(2018, 1, 1)
    dbsession.add(invoice2)
    dbsession.flush()
    invoice2.set_status('wait', request_with_config)
    dbsession.merge(invoice2)
    dbsession.flush()
    invoice2.set_status('valid', request_with_config)
    assert invoice2.official_number == 1

def test_official_number_same_year(
    config, dbsession, invoice, request_with_config,
    user
):
    request_with_config.user = invoice.owner
    invoice2 = invoice.duplicate(
        user=invoice.owner,
        project=invoice.project,
        phase=invoice.phase,
        customer=invoice.customer
    )
    invoice.official_number = 150
    invoice.date = datetime.date(2017, 12, 30)
    dbsession.add(invoice)
    dbsession.flush()

    invoice2.date = datetime.date(2017, 12, 31)
    dbsession.add(invoice2)
    dbsession.flush()
    invoice2.set_status('wait', request_with_config)
    dbsession.merge(invoice2)
    dbsession.flush()
    invoice2.set_status('valid', request_with_config)
    assert invoice2.official_number == 151


def test_gen_cancelinvoice(dbsession, full_invoice, user):
    cinv = full_invoice.gen_cancelinvoice(user)
    dbsession.add(cinv)
    dbsession.flush()

    assert cinv.total_ht() == -1 * full_invoice.total_ht()
    today = datetime.date.today()
    assert cinv.date == today
    assert cinv.prefix == full_invoice.prefix
    assert cinv.financial_year == full_invoice.financial_year
    assert cinv.mentions == full_invoice.mentions
    assert cinv.address == full_invoice.address
    assert cinv.workplace == full_invoice.workplace
    assert cinv.project == full_invoice.project
    assert cinv.company == full_invoice.company
    assert cinv.phase == full_invoice.phase


def test_gen_cancelinvoice_with_payment(
    dbsession, full_invoice, tva, mode, user
):
    from autonomie.models.task.invoice import Payment
    payment = Payment(mode=mode.label, amount=10000000, tva=tva)
    full_invoice.payments = [payment]
    cinv = full_invoice.gen_cancelinvoice(user)
    assert len(cinv.default_line_group.lines) == len(
        full_invoice.default_line_group.lines) + len(full_invoice.discounts) + 1

    # Le paiement est indiqué ttc, ici on a le HT (tva inversée)
    assert cinv.default_line_group.lines[-1].cost == 8333333
    assert cinv.default_line_group.lines[-1].tva == 2000


def test_record_payment(full_invoice, request_with_config, user):
    value = {'amount': 2000000, 'mode': 'cheque'}
    full_invoice.record_payment(user_id=user.id, **value)
    assert len(full_invoice.payments) == 1
    assert full_invoice.payments[0].amount == 2000000


def test_payment_get_amount():
    from autonomie.models.task.invoice import Payment
    payment = Payment(amount=1895000, mode="test")
    assert payment.get_amount() == 1895000


def test_invoice_topay(full_invoice, user):
    value = {'amount': 2000000, 'mode': 'cheque'}
    full_invoice.record_payment(user_id=user.id, **value)
    assert full_invoice.paid() == 2000000
    assert full_invoice.topay() == full_invoice.total() - 2000000
    assert full_invoice.payments[-1].user_id == user.id

def test_resulted_manual(full_invoice, request_with_config, user):
    full_invoice.status = 'valid'
    full_invoice.paid_status = 'paid'
    request_params = {'amount': 0, 'mode': 'cheque', 'resulted': True}
    full_invoice.record_payment(user_id=user.id, **request_params)
    assert full_invoice.paid_status == 'resulted'


def test_resulted_auto(full_invoice, request_with_config, user):
    full_invoice.status = 'valid'
    full_invoice.paid_status = 'paid'
    request_params = {'amount': int(full_invoice.topay()), 'mode': 'cheque'}
    full_invoice.record_payment(user_id=user.id, **request_params)
    assert full_invoice.paid_status == 'resulted'


def test_resulted_auto_more(full_invoice, request_with_config, user):
    full_invoice.status = 'valid'
    full_invoice.paid_status = 'paid'
    request_params = {'amount': int(full_invoice.topay()) + 1, 'mode': 'cheque'}
    full_invoice.record_payment(user_id=user.id, **request_params)
    assert full_invoice.paid_status == 'resulted'


def test_status_register(full_invoice, request_with_config, user):
    full_invoice.status = 'valid'
    full_invoice.paid_status = 'paid'
    request_params = {'amount': int(full_invoice.topay()), 'mode': 'cheque'}
    full_invoice.record_payment(user_id=user.id, **request_params)
    assert full_invoice.statuses[-1].status_code == 'resulted'
    assert full_invoice.statuses[-1].status_person_id == user.id
