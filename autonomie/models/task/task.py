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
    Task model
    represents a base task, with a status, an owner, a phase
"""
import logging

from zope.interface import implementer
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    )
from sqlalchemy.orm import (
        relationship,
        validates,
        deferred,
        backref,
        )

from autonomie.models.types import (
        CustomDateType,
        CustomDateType2)
from autonomie.models.utils import get_current_timestamp
from autonomie.models.base import (
        DBBASE,
        default_table_args,
        )
from autonomie.models.tva import Tva
from autonomie.exception import Forbidden

from .interfaces import ITask
from .states import DEFAULT_STATE_MACHINES
from autonomie.compute.task import LineCompute
from autonomie.models.node import Node

log = logging.getLogger(__name__)


@implementer(ITask)
class Task(Node):
    """
        Metadata pour une tâche (estimation, invoice)
    """
    __tablename__ = 'task'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'task'}

    id = Column(Integer, ForeignKey('node.id'), primary_key=True)
    phase_id = Column("phase_id", ForeignKey('phase.id'))
    name = Column("name", String(255))
    CAEStatus = Column('CAEStatus', String(10))
    statusComment = Column("statusComment", Text)
    statusPerson = Column("statusPerson",
                          ForeignKey('accounts.id'))
    statusDate = Column(
        "statusDate",
        CustomDateType,
        default=get_current_timestamp,
        )
    taskDate = Column("taskDate", CustomDateType2)
    owner_id = Column("owner_id", ForeignKey('accounts.id'))
    creationDate = deferred(
        Column("creationDate", CustomDateType,
               default=get_current_timestamp)
    )
    updateDate = Column(
        "updateDate", CustomDateType,
        default=get_current_timestamp,
        onupdate=get_current_timestamp)
    description = Column("description", Text)
    statusPersonAccount = relationship(
        "User",
        primaryjoin="Task.statusPerson==User.id",
        backref="taskStatuses")
    owner = relationship(
        "User",
        primaryjoin="Task.owner_id==User.id",
        backref="ownedTasks")

    phase = relationship(
        "Phase",
        primaryjoin="Task.phase_id==Phase.id",
        backref=backref("tasks", order_by='Task.taskDate'),
        lazy="joined")

    state_machine = DEFAULT_STATE_MACHINES['base']

    def __init__(self, **kwargs):
        if not 'CAEStatus' in kwargs:
            self.CAEStatus = self.state_machine.default_state

        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_status(self, status, request, user_id, **kw):
        """
            set the status of a task through the state machine
        """
        return self.state_machine.process(self, request, user_id, status, **kw)

    def is_invoice(self):
        return False

    def is_estimation(self):
        return False

    def is_cancelinvoice(self):
        return False

    @validates('CAEStatus')
    def change_status(self, key, status):
        """
        fired on status change, stores a new taskstatus for each status change
        """
        log.debug(u"# CAEStatus change #")

        actual_status = self.CAEStatus
        if actual_status is None and status == self.state_machine.default_state:
            return status

        self.statusDate = get_current_timestamp()

        log.debug(u" + was {0}, becomes {1}".format(actual_status, status))
        status_record = TaskStatus(
            statusCode=status,
            statusPerson=self.statusPerson,
            )
        self.statuses.append(status_record)

        return status

    def get_next_actions(self):
        """
            Return the next available actions regarding the current status
        """
        return self.state_machine.get_next_states(self.CAEStatus)

    def get_company(self):
        """
            Return the company owning this task
        """
        if self.project:
            return self.project.company
        else:
            return None

    @property
    def company(self):
        return self.get_company()

    def get_customer(self):
        """
            Return the customer of the current task
        """
        return self.customer

    def get_company_id(self):
        """
            Return the id of the company owning this task
        """
        return self.project.company.id

    def is_deletable(self, request):
        """
            Return True if the task is deletable
        """
        for action in self.get_next_actions():
            if action.name == 'delete':
                if action.allowed(self, request):
                    return True
        return False

    def __repr__(self):
        return u"<Task status:{s.CAEStatus} id:{s.id}>".format(s=self)


class DiscountLine(DBBASE, LineCompute):
    """
         A discount line
    """
    __tablename__ = 'discount'
    __table_args__ = default_table_args
    id = Column("id", Integer, primary_key=True, nullable=False)
    task_id = Column(Integer, ForeignKey('task.id', ondelete="cascade"))
    tva = Column("tva", Integer, nullable=False, default=196)
    amount = Column("amount", Integer)
    description = Column("description", Text)
    task = relationship("Task",
        backref=backref('discounts',
            order_by='DiscountLine.tva',
            cascade="all, delete-orphan"))

    def duplicate(self):
        """
            return the equivalent InvoiceLine
        """
        line = DiscountLine()
        line.tva = self.tva
        line.amount = self.amount
        line.description = self.description
        return line

    def total_ht(self):
        """
            Compute the line's total
        """
        return float(self.amount)

    def tva_amount(self):
        """
            compute the tva amount of a line
        """
        totalht = self.total_ht()
        result = float(totalht) * (max(int(self.tva), 0) / 10000.0)
        return result

    def total(self):
        return self.tva_amount() + self.total_ht()

    def __repr__(self):
        return u"<DiscountLine amount : {s.amount} tva:{s.tva} id:{s.id}>"\
                .format(s=self)

    def get_tva(self):
        return Tva.query(include_inactive=True).filter(Tva.value == self.tva)


class TaskStatus(DBBASE):
    """
        Task status, should be used to record the task's status
    """
    __tablename__ = 'task_status'
    __table_args__ = default_table_args
    id = Column("id", Integer, primary_key=True)
    task_id = Column('task_id',
        Integer,
        ForeignKey('task.id', ondelete="cascade"))
    statusCode = Column("statusCode", String(10))
    statusComment = Column("statusComment", Text)
    statusPerson = Column("statusPerson", Integer, ForeignKey('accounts.id'))
    statusDate = Column("statusDate",
        CustomDateType,
        default=get_current_timestamp)
    task = relationship("Task",
        backref=backref("statuses",
            cascade="all, delete-orphan"))
    statusPersonAccount = relationship("User", backref="task_statuses")
