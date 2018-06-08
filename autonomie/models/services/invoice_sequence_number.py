import string

ALLOWED_VARS = ['AAAA', 'AA', 'MM', 'ANA']


class InvoiceNumberFormatter(string.Formatter):
    """
    str.format()-like but with custom vars to allow applying an invoice number
    template. containing vars and sequence numbers.
    """
    def __init__(self, invoice, sequences_map):
        self._invoice = invoice
        self._sequences_map = sequences_map

    def _get_var_value(self, key):
        if key == 'AAAA':
            return '{:%Y}'.format(self._invoice.date)
        elif key == 'AA':
            return '{:%y}'.format(self._invoice.date)
        elif key == 'MM':
            return '{:%m}'.format(self._invoice.date)
        elif key == 'ANA':
            return '{}'.format(self._invoice.company.code_compta)

    def _get_seq_value(self, key):
        return self._sequences_map[key].get_next_index(self._invoice)

    def get_value(self, key, args, kwargs):
        if key in ALLOWED_VARS:
            return self._get_var_value(key)
        elif key in self._sequences_map:
            return self._get_seq_value(key)
        else:
            return super(InvoiceNumberFormatter, self).get_value(
                key, args, kwargs)
