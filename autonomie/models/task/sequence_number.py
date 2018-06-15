from __future__ import unicode_literals

from datetime import date

from sqlalchemy import (
    extract,
    func,
    Column,
    ForeignKey,
    Integer,
    String,
)

from autonomie_base.models.base import (
    DBSESSION,
    DBBASE,
    default_table_args,
)

from autonomie.models.config import Config


class SequenceNumber(DBBASE):
    """
    Sequence numbers of different chronological sequences
    """
    __tablename__ = 'task_sequence_number'
    __table_args__ = default_table_args

    SEQUENCE_INVOICE_GLOBAL = 'invoice_global'
    SEQUENCE_INVOICE_YEAR = 'invoice_year'
    SEQUENCE_INVOICE_MONTH = 'invoice_month'
    SEQUENCE_INVOICE_MONTH_COMPANY = 'invoice_month_company'
    AVAILABLE_SEQUENCES = [
        SEQUENCE_INVOICE_GLOBAL,
        SEQUENCE_INVOICE_YEAR,
        SEQUENCE_INVOICE_MONTH,
        SEQUENCE_INVOICE_MONTH_COMPANY,
    ]

    id = Column("id", Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('task.id'), nullable=False)
    sequence = Column(String(100), nullable=False)
    index = Column(Integer, nullable=False)


class GlobalInvoiceSequence(object):
    db_key = SequenceNumber.SEQUENCE_INVOICE_GLOBAL

    @classmethod
    def _get_initial_value(cls, invoice):
        return Config.get_value('global_sequence_init_value', None, type_=int)

    @classmethod
    def get_next_index(cls, invoice):
        latest = cls.get_latest_index(invoice)
        if latest is None:
            initial_value = cls._get_initial_value(invoice)
            if initial_value is None:
                return 0
            else:
                return initial_value + 1
        else:
            return latest + 1

    @classmethod
    def _query(cls, invoice):
        from autonomie.models.task import Task

        q = DBSESSION().query(func.Max(SequenceNumber.index))
        q = q.filter(Task.type_.in_(('invoice', 'cancelinvoice')))
        q = q.filter_by(sequence=cls.db_key)
        return q

    @classmethod
    def get_latest_index(cls, invoice):
        """
        :rtype: int or None
        """
        return cls._query(invoice).scalar()


class YearInvoiceSequence(GlobalInvoiceSequence):
    db_key = SequenceNumber.SEQUENCE_INVOICE_YEAR

    @classmethod
    def _get_initial_value(cls, invoice):
        init_date = Config.get_value(
            'year_sequence_init_date',
            default=None,
            type_=date,
        )
        init_value = Config.get_value(
            'year_sequence_init_value',
            default=None,
            type_=int,
        )
        if init_date and init_value and init_date.year == invoice.date.year:
            return init_value

    @classmethod
    def _query(cls, invoice):
        from autonomie.models.task import Task

        assert invoice.date is not None, "validated invoice should have a date"
        q = super(YearInvoiceSequence, cls)._query(invoice)
        q = q.join((Task, Task.id == SequenceNumber.task_id))
        q = q.filter(extract('year', Task.date) == invoice.date.year)
        return q


class MonthInvoiceSequence(YearInvoiceSequence):
    db_key = SequenceNumber.SEQUENCE_INVOICE_MONTH

    @classmethod
    def _get_initial_value(cls, invoice):
        init_date = Config.get_value(
            'month_sequence_init_date',
            None,
            type_=date,
        )
        init_value = Config.get_value(
            'month_sequence_init_value',
            default=None,
            type_=int,
        )
        if (
                init_date and init_value
                and init_date.year == invoice.date.year
                and init_date.month == invoice.date.month
        ):
            return init_value
        else:
            return None

    @classmethod
    def _query(cls, invoice):
        from autonomie.models.task import Task

        q = super(MonthInvoiceSequence, cls)._query(invoice)
        q = q.filter(extract('month', Task.date) == invoice.date.month)
        return q


class MonthCompanyInvoiceSequence(MonthInvoiceSequence):
    db_key = SequenceNumber.SEQUENCE_INVOICE_MONTH_COMPANY

    @classmethod
    def _get_initial_value(cls, invoice):
        init_date = invoice.company.month_company_sequence_init_date
        init_value = invoice.company.month_company_sequence_init_value
        if (
                init_date and init_value
                and init_date.year == invoice.date.year
                and init_date.month == invoice.date.month
        ):
            return init_value
        else:
            return None

    @classmethod
    def _query(cls, invoice):
        from autonomie.models.task import Task

        q = super(MonthCompanyInvoiceSequence, cls)._query(invoice)
        q = q.filter(Task.company == invoice.company)
        return q
