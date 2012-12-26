# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 03-09-2012
# * Last Modified :
#
# * Project :
#
"""
    Task model
    represents a base task, with a status, an owner, a phase
"""
import logging

from zope.interface import implementer
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.orm import deferred
from sqlalchemy.orm import backref

from autonomie.models.types import CustomDateType
from autonomie.models.types import CustomDateType2
from autonomie.models.utils import get_current_timestamp
from autonomie.models import DBBASE
from autonomie.models import default_table_args
from autonomie.exception import Forbidden

from .interfaces import ITask
from .states import DEFAULT_STATE_MACHINES

log = logging.getLogger(__name__)


@implementer(ITask)
class Task(DBBASE):
    """
        Metadata pour une tâche (estimation, invoice)
    """
    __tablename__ = 'task'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'task'}

    id = Column(Integer, primary_key=True)
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
        onupdate=get_current_timestamp)
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
        backref="tasks",
        lazy="joined")

    type_ = Column('type_', String(30), nullable=False)
    __mapper_args__ = {'polymorphic_on': type_,
                       'polymorphic_identity': 'task'}

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
    def validate_status(self, key, status):
        """
            validate the caestatus change
        """
        log.debug(u"# CAEStatus change #")

        actual_status = self.CAEStatus
        if actual_status is None and status == self.state_machine.default_state:
            return status
        log.debug(u" + was {0}, becomes {1}".format(actual_status, status))

        allowed_status = self.state_machine.get_next_status(actual_status)

        if status != actual_status and status not in allowed_status:
            message = u"Vous n'êtes pas autorisé à assigner ce statut {0} à \
ce document.".format(status)
            raise Forbidden(message)
        self.statuses.append(TaskStatus(statusCode=status,
                                        statusPerson=self.statusPerson))
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

    def get_client(self):
        """
            Return the client of the current task
        """
        return self.client

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


class DiscountLine(DBBASE):
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
