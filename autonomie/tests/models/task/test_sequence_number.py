from autonomie.models.task.sequence_number import GlobalInvoiceSequence


def test_global_invoice_sequence_next_first(invoice):
    seq_num = GlobalInvoiceSequence.get_next_index(invoice)
    assert seq_num == 0


def test_global_invoice_sequence_next_then(invoice, global_seq_1):
    seq_num = GlobalInvoiceSequence.get_next_index(invoice)
    assert seq_num == 1
