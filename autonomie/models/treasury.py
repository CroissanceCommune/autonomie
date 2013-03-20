# -*- coding: utf-8 -*-
# * File Name : treasury.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 04-02-2013
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Models related to the treasury module
"""
from datetime import date
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Enum
from sqlalchemy import Text
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from autonomie.models.base import DBBASE
from autonomie.models.base import default_table_args
from autonomie.models.statemachine import StateMachine

MANAGER_PERMS = "manage"

class TurnoverProjection(DBBASE):
    """
        Turnover projection
        :param company_id: The company this projection is related to
        :param month: The month number this projection is made for
        :param year: The year this projection is made for
    """
    __tablename__ = 'turnover_projection'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="cascade"))
    month = Column(Integer)
    year = Column(Integer)
    comment = Column(Text, default="")
    value = Column(Integer)
    company = relationship("Company",
            backref=backref("turnoverprojections",
                order_by="TurnoverProjection.month",
                cascade="all, delete-orphan"))


class ExpenseType(DBBASE):
    """
        Base Type for expenses
        :param label: Label of the expense type that will be used in the UI
        :param code: Analytic code related to this expense
        :param type: Column for polymorphic discrimination
    """
    __tablename__ = 'expense_type'
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_on="type",
                           polymorphic_identity="expense",
                           with_polymorphic='*')
    id = Column(Integer, primary_key=True)
    type = Column(String(30), nullable=False)
    label = Column(String(50))
    code = Column(String(15))


class ExpenseKmType(ExpenseType):
    """
        Type of expenses related to kilometric fees
    """
    __tablename__ = 'expensekm_type'
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_identity='expensekm')
    id = Column(Integer, ForeignKey('expense_type.id'), primary_key=True)
    amount = Column(Float(precision=4))


class ExpenseTelType(ExpenseType):
    """
        Type of expenses related to telefonic fees
    """
    __tablename__ = 'expensetel_type'
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_identity='expensetel')
    id = Column(Integer, ForeignKey('expense_type.id'), primary_key=True)
    percentage = Column(Integer)


def build_state_machine():
    """
        Return a state machine that allows ExpenseSheet status handling
    """
    reset = ('reset', None, None, False,)
    valid = ('valid', MANAGER_PERMS, )
    invalid = ('invalid', MANAGER_PERMS,)
    states = {}
    states['draft'] = ('draft', 'wait', reset, valid,)
    states['invalid'] = ('draft', 'wait',)
    states['wait'] = (valid, invalid,)
    return states


class ExpenseStates(StateMachine):
    """
        Expense state machine
    """
    status_attr = "status"
    userid_attr = "status_user_id"


class ExpenseSheet(DBBASE):
    """
        Model representing a whole ExpenseSheet
        An expensesheet is related to a company and an employee (one user may
        have multiple expense sheets if it has multiple companies)
        :param company_id: The user's company id
        :param user_id: The user's id
        :param year: The year the expense is related to
        :param month: The month the expense is related to
        :param status: Status of the sheet
        :param comments: Comments added to this expense sheet
        :param status_user: The user related to statuschange
        :param lines: expense lines of this sheet
    """
    __tablename__ = 'expense_sheet'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    month = Column(Integer)
    year = Column(Integer)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="cascade"))
    user_id = Column(Integer, ForeignKey("accounts.id", ondelete="cascade"))
    status = Column(String(10), default='draft')
    comments = Column(Text)
    status_user_id = Column(Integer, ForeignKey("accounts.id"))
    status_date = Column(Date(), default=date.today(), onupdate=date.today())
    company = relationship("Company",
            backref=backref("expenses",
                order_by="ExpenseSheet.month",
                cascade="all, delete-orphan"))
    user = relationship("User",
            primaryjoin="ExpenseSheet.user_id==User.id",
            backref=backref("expenses",
                order_by="ExpenseSheet.month",
                cascade="all, delete-orphan"))
    status_user = relationship("User",
            primaryjoin="ExpenseSheet.status_user_id==User.id")

    state_machine = ExpenseStates('draft', build_state_machine())


    def __json__(self, request):
        return dict(id=self.id,
                    lines=[line.__json__(request) for line in self.lines],
                    kmlines=[line.__json__(request) for line in self.kmlines],
                    month=self.month,
                    year=self.year)


    def set_status(self, status, request, user_id, **kw):
        """
            Set the status of a task through a state machine
        """
        return self.state_machine.process(self, request, user_id, status, **kw)

    def get_next_actions(self):
        """
            Return the next available actions regarding the current status
        """
        return self.state_machine.get_next_states(self.status)

    def get_company_id(self):
        """
            Return the if of the company associated to this model
        """
        return self.company_id


class BaseExpenseLine(DBBASE):
    """
        Base models for expense lines
        :param type: Column for polymorphic discrimination
        :param date: Date of the expense
        :param description: description of the expense
        :param code: analytic code related to this expense
        :param valid: validation status of the expense
        :param sheet_id: id of the expense sheet this expense is related to
    """
    __tablename__ = 'baseexpense_line'
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_on="type",
            polymorphic_identity="line",
            with_polymorphic='*')
    id = Column(Integer, primary_key=True)
    type = Column(String(30), nullable=False)
    date = Column(Date(), default=date.today())
    description = Column(String(255))
    category = Column(Enum('1', '2'), default='1')
    code = Column(String(15))
    valid = Column(Boolean(), default=True)
    sheet_id = Column(Integer,
            ForeignKey("expense_sheet.id", ondelete="cascade"))


class ExpenseLine(BaseExpenseLine):
    """
        Common Expense line
    """
    __tablename__ = "expense_line"
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_identity='expenseline')
    id = Column(Integer, ForeignKey('baseexpense_line.id'), primary_key=True)
    ht = Column(Integer)
    tva = Column(Integer)
    sheet = relationship("ExpenseSheet",
                backref=backref("lines",
                    order_by="ExpenseLine.date",
                    cascade="all, delete-orphan"))

    def __json__(self, request):
        return dict(
                    id=self.id,
                    date=self.date,
                    valid=self.valid,
                    category=self.category,
                    description=self.description,
                    ht=self.ht,
                    tva=self.tva,
                    code=self.code)


class ExpenseKmLine(BaseExpenseLine):
    """
        Model representing a specific expense related to kilometric fees
        :param start: starting point
        :param end: endpoint
        :param km: Number of kilometers
    """
    __tablename__ = "expensekm_line"
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_identity='expensekmline')
    id = Column(Integer, ForeignKey('baseexpense_line.id'), primary_key=True)
    start = Column(String(150), default="")
    end = Column(String(150), default="")
    km = Column(Integer)
    sheet = relationship("ExpenseSheet",
                backref=backref("kmlines",
                    order_by="ExpenseLine.date",
                    cascade="all, delete-orphan"))

    def __json__(self, request):
        return dict(id=self.id,
                    date=self.date,
                    valid=self.valid,
                    category=self.category,
                    description=self.description,
                    km=self.km,
                    start=self.start,
                    end=self.end,
                    code=self.code)


