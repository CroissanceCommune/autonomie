from datetime import date

import pytest

from autonomie.models.services.invoice_sequence_number import (
    InvoiceNumberFormatter,
    InvoiceNumberService,
)
from autonomie.models.task.sequence_number import (
    GlobalInvoiceSequence,
    MonthInvoiceSequence,
    MonthCompanyInvoiceSequence,
    YearInvoiceSequence,
)


def test_global_invoice_sequence_next_first(invoice):
    seq_num = GlobalInvoiceSequence.get_next_index(invoice)
    assert seq_num == 0


def test_global_invoice_sequence_next_then(invoice, global_seq_1):
    seq_num = GlobalInvoiceSequence.get_next_index(invoice)
    assert seq_num == 1


def test_year_invoice_sequence(mk_invoice, set_year_seq_index):
    YIS = YearInvoiceSequence

    assert YIS.get_next_index(mk_invoice(date=date(2017, 1, 1))) == 0
    set_year_seq_index(index=0, year=2017)
    assert YIS.get_next_index(mk_invoice(date=date(2017, 2, 1))) == 1
    set_year_seq_index(index=1, year=2017)

    assert YIS.get_next_index(mk_invoice(date=date(2018, 2, 1))) == 0
    set_year_seq_index(index=0, year=2018)

    assert YIS.get_next_index(mk_invoice(date=date(2018, 2, 1))) == 1
    set_year_seq_index(index=1, year=2018)

    assert YIS.get_next_index(mk_invoice(date=date(2017, 2, 1))) == 2


def test_month_invoice_sequence(mk_invoice, set_month_seq_index):
    MIS = MonthInvoiceSequence

    assert MIS.get_next_index(mk_invoice(date=date(2017, 1, 1))) == 0
    set_month_seq_index(index=0, year=2017, month=1)

    # same year same month
    assert MIS.get_next_index(mk_invoice(date=date(2017, 1, 1))) == 1
    set_month_seq_index(index=1, year=2017, month=1)

    # same year different month
    assert MIS.get_next_index(mk_invoice(date=date(2017, 2, 1))) == 0
    set_month_seq_index(index=1, year=2017, month=2)

    # same month different year
    assert MIS.get_next_index(mk_invoice(date=date(2018, 1, 1))) == 0
    set_month_seq_index(index=0, year=2018, month=1)
    assert MIS.get_next_index(mk_invoice(date=date(2018, 1, 1))) == 1


def test_month_company_invoice_sequence(
        mk_invoice,
        set_month_company_seq_index,
        company,
        company2,
):
    MCIS = MonthCompanyInvoiceSequence

    # company
    assert MCIS.get_next_index(mk_invoice(date(2017, 1, 1), company)) == 0
    set_month_company_seq_index(index=0, year=2017, month=1, company=company)

    # same year same month, company
    assert MCIS.get_next_index(mk_invoice(date(2017, 1, 1), company)) == 1
    set_month_company_seq_index(index=1, year=2017, month=1, company=company)

    # same year same month, company2
    assert MCIS.get_next_index(mk_invoice(date(2017, 1, 1), company2)) == 0
    set_month_company_seq_index(index=1, year=2017, month=1, company=company2)

    # same year different month, company
    assert MCIS.get_next_index(mk_invoice(date(2017, 2, 1), company)) == 0
    set_month_company_seq_index(index=1, year=2017, month=1, company=company)

    # same month different year company
    assert MCIS.get_next_index(mk_invoice(date=date(2018, 1, 1))) == 0


def test_invoice_number_formatter(invoice_20170707, DummySequence):
    fmt = InvoiceNumberFormatter(
        invoice=invoice_20170707,
        sequences_map={'DUMMY': DummySequence},
    )
    assert fmt.format('') == ''
    assert fmt.format('{AAAA}') == '2017'
    assert fmt.format('{AA}') == '17'
    assert fmt.format('{MM}') == '07'
    assert fmt.format('{ANA}') == '0USER'
    assert fmt.format('{DUMMY}') == '12'
    assert fmt.format('@{DUMMY}-{AAAA}') == '@12-2017'

    with pytest.raises(KeyError):
        assert fmt.format('{DONOTEXIST}')


def test_invoice_number_service_validation():
    InvoiceNumberService.validate_template('')
    InvoiceNumberService.validate_template('aaa')
    InvoiceNumberService.validate_template('@{SEQGLOBAL}-{AAAA}')

    with pytest.raises(ValueError):
        InvoiceNumberService.validate_template('@{DONOTEXIST}')


def test_invoice_number_service_generation(invoice_20170707, invoice_20170808):
    tpl = 'FC-{AAAA}{MM}-{SEQGLOBAL}'

    InvoiceNumberService.assign_number(invoice_20170707, tpl)
    InvoiceNumberService.assign_number(invoice_20170808, tpl)
    assert invoice_20170707.official_number == 'FC-201707-0'
    assert invoice_20170808.official_number == 'FC-201707-1'

    # Will not re-assign
    with pytest.raises(ValueError):
        InvoiceNumberService.assign_number(invoice_20170707, tpl)
