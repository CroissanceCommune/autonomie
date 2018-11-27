import string
from sqlalchemy import extract

from autonomie_base.models.base import DBSESSION
from autonomie.models.task.sequence_number import (
    GlobalInvoiceSequence,
    MonthInvoiceSequence,
    MonthCompanyInvoiceSequence,
    SequenceNumber,
    YearInvoiceSequence,
)


ALLOWED_VARS = ['YYYY', 'YY', 'MM', 'ANA']


class InvoiceNumberFormatter(string.Formatter):
    """
    str.format()-like but with custom vars to allow applying an invoice number
    template. containing vars and sequence numbers.
    """
    def __init__(self, invoice, sequences_map):
        self._invoice = invoice
        self._sequences_map = sequences_map

    def _get_var_value(self, key):
        if key == 'YYYY':
            return '{:%Y}'.format(self._invoice.date)
        elif key == 'YY':
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


class InvoiceNumberService(object):
    SEQUENCES_MAP = {
        'SEQGLOBAL': GlobalInvoiceSequence,
        'SEQYEAR': YearInvoiceSequence,
        'SEQMONTH': MonthInvoiceSequence,
        'SEQMONTHANA': MonthCompanyInvoiceSequence,
    }
    ALLOWED_KEYS = ALLOWED_VARS + SEQUENCES_MAP.keys()

    @classmethod
    def validate_template(cls, template):
        """
        Validate the correctness of the invoice number template
        """
        fmt = string.Formatter()
        tpl_vars = fmt.parse(template)

        for _, key, _, _ in tpl_vars:
            if key is not None and key not in cls.ALLOWED_KEYS:
                raise ValueError(
                    "{{{}}} n'est pas une clef valide (disponibles : {})".format(
                        key,
                        ', '.join('{{{}}}'.format(i) for i in cls.ALLOWED_KEYS)
                    ))

    @classmethod
    def get_involved_sequences(cls, invoice, template):
        """
        Tell which sequences are to be used and what indexes they will give

        :returns: the sequences that would be used by this template and their
           next index
        :rtype: list of couples [<sequence>, <sequence_number>]
        """
        out = []
        used_sequences = set()  # to avoid duplicates in out
        tpl_vars = string.Formatter().parse(template)

        for _, key, _, _ in tpl_vars:
            if key in cls.SEQUENCES_MAP:

                seq = cls.SEQUENCES_MAP[key]
                if seq not in used_sequences:
                    out.append([seq, seq.get_next_index(invoice)])
                    used_sequences.add(seq)

        return out

    @classmethod
    def assign_number(cls, invoice, template):
        """
        This function should be run within an SQL transaction to enforce
        sequence index unicity.
        """
        if invoice.official_number:
            raise ValueError('This invoice already have an official number')
        cls.validate_template(template)

        db = DBSESSION()
        formatter = InvoiceNumberFormatter(invoice, cls.SEQUENCES_MAP)
        invoice_number = formatter.format(template)

        involved_sequences = cls.get_involved_sequences(invoice, template)

        with db.begin_nested():
            # Create SequenceNumber objects (the index useages have not been
            # booked until now).
            for sequence, next_index in involved_sequences:
                sn = SequenceNumber(
                    sequence=sequence.db_key,
                    index=next_index,
                    task_id=invoice.id,
                )
                db.add(sn)
            invoice.official_number = invoice_number
            db.merge(invoice)

            # Imported here to avoid circular dependencies
            from autonomie.models.task import Task, Invoice, CancelInvoice

            query = Task.query().with_polymorphic([Invoice, CancelInvoice])
            query = query.filter(
                Task.official_number == invoice_number,
                Task.id != invoice.id,
                extract('year', Task.date),
            ).scalar()

            if query is not None:
                # This case is exceptionnal, we can afford a crash here
                # Context manager will take care of rolling back
                # subtransaction.
                raise ValueError(
                    'Invoice number collision, rolling back to avoid it'
                )

        return invoice_number
