# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Boolean,
    ForeignKey,
)
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie_base.models.types import PersistentACLMixin
from sqlalchemy.orm import (
    relationship,
    backref,
)


class ExpensePayment(DBBASE, PersistentACLMixin):
    """
        Expense Payment entry
    """
    __tablename__ = 'expense_payment'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime(),
        info={
            'colanderalchemy': {
                'exclude': True, 'title': u"Créé(e) le",
            }
        },
        default=datetime.datetime.now,
    )

    updated_at = Column(
        DateTime(),
        info={
            'colanderalchemy': {
                'exclude': True, 'title': u"Mis(e) à jour le",
            }
        },
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now
    )

    mode = Column(String(50))
    amount = Column(Integer)
    date = Column(DateTime(), default=datetime.datetime.now)
    # est-ce un abandon de créance
    waiver = Column(Boolean(), default=False)
    exported = Column(Boolean(), default=False)
    expense_sheet_id = Column(
        Integer,
        ForeignKey('expense_sheet.id', ondelete="cascade")
    )
    user_id = Column(ForeignKey('accounts.id'))
    user = relationship("User")

    bank_id = Column(ForeignKey('bank_account.id'))
    bank = relationship(
        "BankAccount",
        backref=backref(
            'expense_payments',
            order_by="ExpensePayment.date",
            info={'colanderalchemy': {'exclude': True}},
        ),
    )
    expense = relationship(
        "ExpenseSheet",
        backref=backref(
            'payments',
            order_by="ExpensePayment.date",
            info={'colanderalchemy': {'exclude': True}},
        ),
    )
    # formatting precision
    precision = 2

    def get_amount(self):
        return self.amount

    @property
    def parent(self):
        return self.expense

    def __repr__(self):
        return u"<ExpensePayment id:{s.id} \
expense_sheet_id:{s.expense_sheet_id} \
amount:{s.amount} \
mode:{s.mode} \
date:{s.date}".format(s=self)
