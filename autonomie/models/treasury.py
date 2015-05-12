# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
#

"""
    Models related to the treasury module
"""
from datetime import date
from beaker.cache import cache_region
from sqlalchemy import (
    Column,
    Date,
    Integer,
    String,
    Float,
    Enum,
    Text,
    Boolean,
    ForeignKey,
    distinct,
)
from sqlalchemy.orm import (
    relationship,
    backref,
)

from autonomie.models.base import (
    DBBASE,
    DBSESSION,
    default_table_args,
)
from autonomie.forms import EXCLUDED
from autonomie.compute import math_utils

from autonomie.models.types import PersistentACLMixin
from autonomie.models.statemachine import StateMachine
from autonomie.models.node import Node

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
    company = relationship(
        "Company",
        backref=backref(
            "turnoverprojections",
            order_by="TurnoverProjection.month",
            cascade="all, delete-orphan",
            info={
                'export': {'exclude': True},
            },
        )
    )


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
    active = Column(Boolean(), default=True)

    code_tva = Column(String(15), default="")
    compte_tva = Column(String(15), default="")
    contribution = Column(Boolean(), default=False)

    def __json__(self, request=None):
        return {
            "id": self.id,
            "value": str(self.id),
            "active": self.active,
            "code": self.code,
            "label": u"{0} ({1})".format(self.label, self.code),
        }


class ExpenseKmType(ExpenseType):
    """
        Type of expenses related to kilometric fees
    """
    __tablename__ = 'expensekm_type'
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_identity='expensekm')
    id = Column(Integer, ForeignKey('expense_type.id'), primary_key=True)
    amount = Column(Float(precision=4))

    def __json__(self, request=None):
        res = ExpenseType.__json__(self)
        res['amount'] = self.amount
        return res


class ExpenseTelType(ExpenseType):
    """
        Type of expenses related to telefonic fees
    """
    __tablename__ = 'expensetel_type'
    __table_args__ = default_table_args
    __mapper_args__ = dict(polymorphic_identity='expensetel')
    id = Column(Integer, ForeignKey('expense_type.id'), primary_key=True)
    percentage = Column(Integer)
    initialize = Column(Boolean, default=True)

    def __json__(self, request=None):
        res = ExpenseType.__json__(self)
        res['percentage'] = self.percentage
        return res


def build_state_machine():
    """
        Return a state machine that allows ExpenseSheet status handling
    """
    reset = ('reset', None, None, False,)
    valid = ('valid', MANAGER_PERMS, )
    invalid = ('invalid', MANAGER_PERMS,)
    resulted = ('resulted', MANAGER_PERMS, )
    states = {}
    states['draft'] = ('draft', 'wait', reset, valid,)
    states['invalid'] = ('draft', 'wait',)
    states['wait'] = (valid, invalid,)
    states['valid'] = (resulted,)
    return states


class ExpenseStates(StateMachine):
    """
        Expense state machine
    """
    status_attr = "status"
    userid_attr = "status_user_id"


class ExpenseSheet(Node):
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
    __mapper_args__ = {'polymorphic_identity': 'expensesheet'}
    id = Column(ForeignKey('node.id'), primary_key=True)
    month = Column(Integer)
    year = Column(Integer)
    company_id = Column(Integer, ForeignKey("company.id", ondelete="cascade"))
    user_id = Column(Integer, ForeignKey("accounts.id"))
    status = Column(String(10), default='draft')
    status_user_id = Column(Integer, ForeignKey("accounts.id"))
    status_date = Column(
        Date(),
        default=date.today,
        onupdate=date.today
    )
    exported = Column(Boolean(), default=False)
    company = relationship(
        "Company",
        backref=backref(
            "expenses",
            order_by="ExpenseSheet.month",
            cascade="all, delete-orphan",
        )
    )
    user = relationship(
        "User",
        primaryjoin="ExpenseSheet.user_id==User.id",
        backref=backref(
            "expenses",
            order_by="ExpenseSheet.month",
            info={
                'colanderalchemy': EXCLUDED,
                'export': {'exclude': True},
            },
            cascade="all, delete-orphan"
        ),
    )
    status_user = relationship(
        "User",
        primaryjoin="ExpenseSheet.status_user_id==User.id",
    )

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

    @property
    def total(self):
        """
            return the total of the current expense
        """
        return sum([line.total for line in self.lines]) \
                + sum([line.total for line in self.kmlines])

    def get_lines_by_type(self):
        """
        Return lines grouped by type
        """
        ret_dict = {}
        for line in self.lines:
            ret_dict.setdefault(line.type_object.code, []).append(line)
        for line in self.kmlines:
            ret_dict.setdefault(line.type_object.code, []).append(line)
        return ret_dict.values()


class BaseExpenseLine(DBBASE, PersistentACLMixin):
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
    valid = Column(Boolean(), default=True)
    type_id = Column(Integer)
    sheet_id = Column(Integer,
            ForeignKey("expense_sheet.id", ondelete="cascade"))
    type_object = relationship(
        "ExpenseType",
        primaryjoin='BaseExpenseLine.type_id==ExpenseType.id',
        uselist=False,
        foreign_keys=type_id,
    )


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
    sheet = relationship(
        "ExpenseSheet",
        backref=backref(
            "lines",
            order_by="ExpenseLine.date",
            cascade="all, delete-orphan"
        )
    )

    def __json__(self, request):
        return dict(
                    id=self.id,
                    date=self.date,
                    valid=self.valid,
                    category=self.category,
                    description=self.description,
                    ht=self.ht,
                    tva=self.tva,
                    type_id=self.type_id)

    def _compute_value(self, val):
        result = 0
        # In the first versions it was possible to delete expensetypes (now they
        # are disabled instead)
        if self.type_object is not None:
            if self.type_object.type == 'expensetel':
                percentage = self.type_object.percentage
                val = val * percentage / 100.0
            result = math_utils.floor(val)
        return result

    @property
    def total(self):
        """
            return the total
        """
        return self.total_ht + self.total_tva

    @property
    def total_ht(self):
        """
        Return the HT total of the line
        """
        return self._compute_value(self.ht)

    @property
    def total_tva(self):
        return self._compute_value(self.tva)


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
    type_label = Column(String(50))
    start = Column(String(150), default="")
    end = Column(String(150), default="")
    km = Column(Integer)
    sheet = relationship(
        "ExpenseSheet",
        backref=backref(
            "kmlines",
            order_by="ExpenseLine.date",
            cascade="all, delete-orphan"
        )
    )

    def __json__(self, request):
        return dict(id=self.id,
                    date=self.date,
                    valid=self.valid,
                    category=self.category,
                    description=self.description,
                    type_label=self.type_label,
                    km=self.km,
                    start=self.start,
                    end=self.end,
                    type_id=self.type_id)

    @property
    def total(self):
        indemnity = self.type_object.amount
        return math_utils.floor(indemnity * self.km)

    @property
    def vehicle(self):
        return self.type_object.label

    @property
    def ht(self):
        # Deprecated function kept for compatibility
        return self.total

    @property
    def total_ht(self):
        return self.total

    @property
    def total_tva(self):
        return 0


class Communication(DBBASE):
    """
        Communication Class, logs communications between the contractor and its
        CAE
    """
    __tablename__ = "communication"
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("accounts.id"))
    content = Column(Text)
    date = Column(Date(), default=date.today(), onupdate=date.today())
    expense_sheet_id = Column(Integer, ForeignKey("expense_sheet.id"))

    expense_sheet = relationship(
        "ExpenseSheet",
        backref=backref(
            "communications",
            order_by="Communication.date",
            cascade="all, delete-orphan"
        )
    )

    user = relationship(
        "User",
        primaryjoin="Communication.user_id==User.id",
        backref=backref(
            "expense_communications",
            order_by="Communication.date",
            cascade="all, delete-orphan",
            info={
                'colanderalchemy': EXCLUDED,
                'export': {'exclude': True},
            },
        )
    )


def get_expense_years():
    """
    Return the list of years that there were some expense configured
    """
    @cache_region("long_term", "expenseyears")
    def expenseyears():
        """
        return distinct expense years available in the database
        """
        query = DBSESSION().query(distinct(ExpenseSheet.year))\
                .order_by(ExpenseSheet.year)
        years = [year[0] for year in query]
        current = date.today().year
        if current not in years:
            years.append(current)
        return years
    return expenseyears()


def get_expense_sheet_name(month, year):
    """
    Return the name of an expensesheet
    """
    return u"expense_{0}_{1}".format(month, year)

