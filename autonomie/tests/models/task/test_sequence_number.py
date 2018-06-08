import pytest
from autonomie.models.services.invoice_sequence_number import (
    InvoiceNumberFormatter,
    InvoiceNumberService,
)
from autonomie.models.task.sequence_number import GlobalInvoiceSequence


def test_global_invoice_sequence_next_first(invoice):
    seq_num = GlobalInvoiceSequence.get_next_index(invoice)
    assert seq_num == 0


def test_global_invoice_sequence_next_then(invoice, global_seq_1):
    seq_num = GlobalInvoiceSequence.get_next_index(invoice)
    assert seq_num == 1


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
