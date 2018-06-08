from __future__ import unicode_literals

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)

from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)


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
    task = Column(Integer, ForeignKey('task.id'), nullable=False)
    sequence = Column(String(100), nullable=False)
    index = Column(Integer, nullable=False)
