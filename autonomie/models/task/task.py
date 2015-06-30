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
import colander
import deform

from zope.interface import implementer
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    Boolean,
    Float,
)
from sqlalchemy.event import listen

from sqlalchemy.orm import (
    relationship,
    validates,
    deferred,
    backref,
)

from autonomie.models.types import (
    CustomDateType,
    CustomDateType2,
)
from autonomie.models.utils import get_current_timestamp
from autonomie.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie import forms
from autonomie.models.user import get_deferred_user_choice
from autonomie.models.tva import Tva

from .interfaces import ITask
from .states import DEFAULT_STATE_MACHINES
from autonomie.compute.task import (
    LineCompute,
    GroupCompute,
)
from autonomie.models.node import Node

log = logging.getLogger(__name__)


ALL_STATES = ('draft', 'wait', 'valid', 'invalid', 'geninv',
              'aboest', 'gencinv', 'resulted', 'paid', )


@implementer(ITask)
class Task(Node):
    """
        Metadata pour une tâche (estimation, invoice)
    """
    __tablename__ = 'task'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'task'}

    id = Column(Integer, ForeignKey('node.id'), primary_key=True)
    phase_id = Column(
        ForeignKey('phase.id'),
        info={
            'colanderalchemy': forms.EXCLUDED,
            "export": {'exclude': True},
        },
    )
    CAEStatus = Column(
        String(10),
        info={
            'colanderalchemy': {
                'widget': deform.widget.SelectWidget(
                    values=zip(ALL_STATES, ALL_STATES)
                )
            }
        }
    )
    statusComment = Column(
        Text,
        info={"colanderalchemy": {'widget': deform.widget.TextAreaWidget()}},
    )
    statusPerson = Column(
        ForeignKey('accounts.id'),
        info={
            'colanderalchemy': {'widget': get_deferred_user_choice()},
            "export": {'exclude': True},
        },
    )
    statusDate = Column(
        CustomDateType,
        default=get_current_timestamp,
        info={'colanderalchemy': {'typ': colander.Date}}
    )
    taskDate = Column(
        CustomDateType2,
        info={'colanderalchemy': {'typ': colander.Date}}
    )
    owner_id = Column(
        ForeignKey('accounts.id'),
        info={
            'colanderalchemy': forms.EXCLUDED,
            "export": {'exclude': True},
        },
    )
    creationDate = deferred(
        Column(
            CustomDateType,
            default=get_current_timestamp,
            info={
                'colanderalchemy': forms.EXCLUDED,
                "export": {'exclude': True},
            },
        )
    )
    updateDate = Column(
        CustomDateType,
        default=get_current_timestamp,
        onupdate=get_current_timestamp,
        info={
            'colanderalchemy': forms.EXCLUDED,
            "export": {'exclude': True},
        },
    )
    description = Column(
        Text,
        info={'colanderalchemy': {'widget': deform.widget.TextAreaWidget()}},
    )
    ht = Column(Integer, default=0)
    tva = Column(Integer, default=0)
    ttc = Column(Integer, default=0)
    project_id = Column(
        Integer,
        ForeignKey('project.id'),
        info={'colanderalchemy': {'exclude': True}},
    )
    customer_id = Column(
        Integer,
        ForeignKey('customer.id'),
        info={'colanderalchemy': {'exclude': True}},
    )
    sequence_number = deferred(
        Column(Integer),
        group='edit',
    )
    _number = Column(
        String(100),
        nullable=False,
    )
    official_number = deferred(
        Column(
            Integer,
            default=None,
        ),
        group='edit'
    )
    display_units = deferred(
        Column(
            Integer,
            default=0
        ),
        group='edit'
    )
    # Not used in latest invoices
    expenses = deferred(
        Column(Integer, default=0),
        group='edit'
    )
    expenses_ht = deferred(
        Column(
            Integer,
            default=0
        ),
        group='edit',
    )
    address = deferred(
        Column(
            Text,
            default="",
            info={
                'colanderalchemy': {
                    'widget': deform.widget.TextAreaWidget()
                }
            },
        ),
        group='edit',
    )
    payment_conditions = deferred(
        Column(
            Text,
            info={
                'colanderalchemy': {
                    'widget': deform.widget.TextAreaWidget()
                }
            },
        ),
        group='edit',
    )
    round_floor = deferred(
        Column(
            Boolean(),
            default=False,
            info={
                'colanderalchemy': {
                    'title': u"Méthode d'arrondi 'à l'ancienne' ?"
                }
            }
        ),
        group='edit',
    )

    # Relationships
    statusPersonAccount = relationship(
        "User",
        primaryjoin="Task.statusPerson==User.id",
        backref=backref(
            "taskStatuses",
            info={
                'colanderalchemy': forms.EXCLUDED,
                'export': {'exclude': True},
            },
        ),
        info={
            'colanderalchemy': forms.EXCLUDED,
            'export': {'exclude': True},
        },
    )
    owner = relationship(
        "User",
        primaryjoin="Task.owner_id==User.id",
        backref=backref(
            "ownedTasks",
            info={
                'colanderalchemy': forms.EXCLUDED,
                'export': {'exclude': True},
            },
        ),
        info={
            'colanderalchemy': forms.EXCLUDED,
            'export': {'exclude': True},
        },
    )

    phase = relationship(
        "Phase",
        primaryjoin="Task.phase_id==Phase.id",
        backref=backref(
            "tasks",
            order_by='Task.taskDate',
            info={
                'colanderalchemy': forms.EXCLUDED,
                'export': {'exclude': True},
            },
        ),
        info={
            'colanderalchemy': forms.EXCLUDED,
            'export': {'exclude': True},
        },
        lazy="joined"
    )

    discounts = relationship(
        "DiscountLine",
        order_by='DiscountLine.tva',
        cascade="all, delete-orphan",
        backref=backref('task'),
    )

    project = relationship(
        "Project",
        primaryjoin="Task.project_id==Project.id",
        backref=backref(
            'tasks',
            order_by='Task.taskDate',
            info={
                'colanderalchemy': forms.EXCLUDED,
                'export': {'exclude': True},
            },
        ),
        info={
            'colanderalchemy': forms.EXCLUDED,
            'export': {'exclude': True},
        },
    )

    customer = relationship(
        "Customer",
        primaryjoin="Customer.id==Task.customer_id",
        backref=backref(
            'tasks',
            order_by='Task.taskDate',
            info={
                'colanderalchemy': forms.EXCLUDED,
                'export': {'exclude': True},
            },
        ),
        info={
            'colanderalchemy': forms.EXCLUDED,
            "export": {'exclude': True},
        },
    )
    payments = relationship(
        "Payment",
        primaryjoin="Task.id==Payment.task_id",
        backref=backref(
            'task',
        ),
        order_by='Payment.date',
        cascade="all, delete-orphan"
    )

    state_machine = DEFAULT_STATE_MACHINES['base']

    def __init__(self, **kwargs):
        if 'CAEStatus' not in kwargs:
            self.CAEStatus = self.state_machine.default_state

        for key, value in kwargs.items():
            setattr(self, key, value)

        # We add a default task line group
        self.line_groups.append(TaskLineGroup(order=0))

    @property
    def default_line_group(self):
        return self.line_groups[0]

    def __json__(self, request):
        """
        Return the datas used by the json renderer to represent this task
        """
        return dict(
            phase_id=self.phase_id,
            status=self.CAEStatus,
            date=self.taskDate,
            owner_id=self.owner_id,
            customer_id=self.customer_id,
            display_units=self.display_units,
            expenses_ht=self.expenses_ht,
            address=self.address,
            payment_conditions=self.payment_conditions,
            description=self.description,
            status_history=[
                status.__json__(request) for status in self.statuses
            ],
            discounts=[
                discount.__json__(request) for discount in self.discounts
            ],
        )

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
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        info={'colanderalchemy': {'widget': deform.widget.HiddenWidget()}}
    )
    task_id = Column(
        Integer,
        ForeignKey(
            'task.id',
            ondelete="cascade",
        ),
        info={'colanderalchemy': forms.EXCLUDED}
    )
    tva = Column(
        Integer,
        nullable=False,
        default=196
    )
    amount = Column(Integer)
    description = Column(
        Text,
        info={'colanderalchemy': {'widget': deform.widget.TextAreaWidget()}}
    )

    def __json__(self, request):
        return dict(
            descriptin=self.description,
            amount=self.amount,
            tva=self.tva,
        )

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
    id = Column(Integer, primary_key=True)
    task_id = Column(
        Integer,
        ForeignKey('task.id', ondelete="cascade"),
    )
    statusCode = Column(String(10))
    statusComment = Column(
        Text,
        info={"colanderalchemy": {'widget': deform.widget.TextAreaWidget()}},
    )
    statusPerson = Column(Integer, ForeignKey('accounts.id'))
    statusDate = Column(
        CustomDateType,
        default=get_current_timestamp,
        info={'colanderalchemy': {'typ': colander.Date}}
    )
    task = relationship(
        "Task",
        backref=backref(
            "statuses",
            cascade="all, delete-orphan",
            info={'colanderalchemy': forms.EXCLUDED}
        )
    )
    statusPersonAccount = relationship(
        "User",
        backref=backref(
            "task_statuses",
            info={
                'colanderalchemy': forms.EXCLUDED,
                'export': forms.EXCLUDED,
            },
        )
    )

    def __json__(self, request):
        result = dict(date=self.statusDate)
        result['code'] = self.statusCode
        if self.statusPersonAccount is not None:
            result['account'] = self.statusPersonAccount.__json__(request)
        return result


class TaskLineGroup(DBBASE, GroupCompute):
    """
    Group of lines
    """
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': {'widget': deform.widget.HiddenWidget()}}
    )
    task_id = Column(
        Integer,
        ForeignKey('task.id', ondelete="cascade"),
        info={'colanderalchemy': forms.EXCLUDED}
    )
    task = relationship(
        "Task",
        primaryjoin="TaskLineGroup.task_id==Task.id",
        backref=backref(
            "line_groups",
            order_by='TaskLineGroup.order',
            cascade="all, delete-orphan",
            info={'colanderalchemy': {'title': u"Unités d'oeuvre"}}
        ),
        info={'colanderalchemy': forms.EXCLUDED}
    )
    description = Column(Text(), default="")
    title = Column(String(255), default="")
    order = Column(Integer, default=1)

    def __json__(self, request):
        return dict(
            title=self.title,
            description=self.description,
            task_id=self.task_id,
            order=self.order,
            lines=[line.__json__(self, request) for line in self.lines]
        )

    def duplicate(self):
        group = TaskLineGroup(
            title=self.title,
            description=self.description,
            task_id=self.task_id,
            lines=[line.duplicate() for line in self.lines],
        )
        return group

    def gen_cancelinvoice_group(self):
        res = self.duplicate()
        for line in res.lines:
            line.cost = -1 * line.cost
        return res


class TaskLine(DBBASE, LineCompute):
    """
        Estimation/Invoice/CancelInvoice lines
    """
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': {'widget': deform.widget.HiddenWidget()}}
    )
    group_id = Column(
        Integer,
        ForeignKey('task_line_group.id', ondelete="cascade"),
        info={'colanderalchemy': forms.EXCLUDED}
    )
    group = relationship(
        TaskLineGroup,
        primaryjoin="TaskLine.group_id==TaskLineGroup.id",
        backref=backref(
            "lines",
            order_by='TaskLine.order',
            cascade="all, delete-orphan",
            info={'colanderalchemy': {'title': u"Prestations"}}
        )
    )
    order = Column(Integer, default=1,)
    description = Column(
        Text,
        info={
            'colanderalchemy': {
                'widget': deform.widget.RichTextWidget(
                    options={
                        'language': "fr_FR",
                        'content_css': "/fanstatic/fanstatic/css/richtext.css",
                    },
                )
            }
        },
    )
    cost = Column(Integer, default=0,)
    tva = Column(Integer, nullable=False, default=196)
    quantity = Column(Float(), default=1)
    unity = Column(String(100),)
    product_id = Column(
        Integer,
        info={'colanderalchemy': forms.EXCLUDED}
    )
    product = relationship(
        "Product",
        primaryjoin="Product.id==TaskLine.product_id",
        uselist=False,
        foreign_keys=product_id,
        info={'colanderalchemy': forms.EXCLUDED}
    )

    def duplicate(self):
        """
            duplicate a line
        """
        newone = TaskLine()
        newone.order = self.order
        newone.cost = self.cost
        newone.tva = self.tva
        newone.description = self.description
        newone.quantity = self.quantity
        newone.unity = self.unity
        newone.product_id = self.product_id
        return newone

    def gen_cancelinvoice_line(self):
        """
            Return a cancel invoice line duplicating this one
        """
        newone = TaskLine()
        newone.order = self.order
        newone.cost = -1 * self.cost
        newone.tva = self.tva
        newone.description = self.description
        newone.quantity = self.quantity
        newone.unity = self.unity
        newone.product_id = self.product_id
        return newone

    def __repr__(self):
        return u"<TaskLine id:{s.id} task_id:{s.group.task_id} cost:{s.cost} \
 quantity:{s.quantity} tva:{s.tva}>".format(s=self)


def _cache_amounts(mapper, connection, target):
    """
    Set amounts in the cached amount vars to be able to provide advanced search
    ... options in the invoice list page
    """
    log.info("Caching the task amounts")
    target.ht = target.total_ht()
    target.ttc = target.total()
    target.tva = target.tva_amount()


listen(Task, "before_insert", _cache_amounts, propagate=True)
listen(Task, "before_update", _cache_amounts, propagate=True)
