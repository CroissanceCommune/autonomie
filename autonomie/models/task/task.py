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
import datetime

from zope.interface import implementer
from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    ForeignKey,
    Text,
    Boolean,
    Float,
    Date,
    or_,
    and_
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
)
from autonomie.models.tva import Tva
from autonomie.models.utils import get_current_timestamp
from autonomie.models.base import (
    DBBASE,
    DBSESSION,
    default_table_args,
)
from autonomie import forms
from autonomie.forms.custom_types import (AmountType, QuantityType,)
from autonomie.models.user import get_deferred_user_choice

from .interfaces import ITask
from .states import DEFAULT_STATE_MACHINES
from autonomie.compute.task import (
    LineCompute,
    DiscountLineCompute,
    GroupCompute,
)
from autonomie.models.node import Node
from autonomie.models.task.mentions import TASK_MENTION


log = logging.getLogger(__name__)


ALL_STATES = ('draft', 'wait', 'valid', 'invalid', 'geninv',
              'aboest', 'gencinv', 'resulted', 'paid', )


class TaskService(object):
    models = None

    @classmethod
    def get_tva_objects(cls, task_obj):
        """
        :param task_obj: The Task object we want to collect tvas for
        :returns: tva stored by amount
        :rtype: dict
        """
        tva_values = set()
        for group in task_obj.line_groups:
            for line in group.lines:
                tva_values.add(line.tva)

        tvas = cls.models.Tva.query().filter(
            Tva.value.in_(list(tva_values))
        ).all()
        return dict([(tva.value, tva) for tva in tvas])

    @classmethod
    def get_valid_tasks(cls, task_cls, *args):
        from autonomie.models.task import Invoice, CancelInvoice
        query = super(task_cls, task_cls).query(*args)
        query = query.with_polymorphic([Invoice, CancelInvoice])
        query = query.filter(
            or_(
                and_(
                    task_cls.CAEStatus.in_(Invoice.valid_states),
                    task_cls.type_ == 'invoice'
                ),
                and_(
                    task_cls.CAEStatus.in_(CancelInvoice.valid_states),
                    task_cls.type_ == 'cancelinvoice'
                )
            )
        )
        return query

    @classmethod
    def get_waiting_estimations(cls, *args):
        from autonomie.models.task import Estimation
        query = Estimation.query(*args)
        query = query.filter(Estimation.CAEStatus == 'wait')
        query = query.order_by(Estimation.statusDate)
        return query

    @classmethod
    def get_waiting_invoices(cls, task_cls, *args):
        from autonomie.models.task import Invoice, CancelInvoice
        query = super(task_cls, task_cls).query(*args)
        query = query.with_polymorphic([Invoice, CancelInvoice])
        query = query.filter(
            task_cls.type_.in_(('invoice', 'cancelinvoice'))
        )
        query = query.filter(task_cls.CAEStatus == 'wait')
        query = query.order_by(task_cls.type_).order_by(task_cls.statusDate)
        return query


@implementer(ITask)
class Task(Node):
    """
        Metadata pour une tâche (estimation, invoice)
    """
    __tablename__ = 'task'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'task'}
    _autonomie_service = TaskService
    __colanderalchemy_config__ = {
        'title': u"Formulaire d'édition forcée de devis/factures/avoirs",
        'help_msg': u"Les montants sont *10^5   10 000==1€",
    }

    id = Column(
        Integer,
        ForeignKey('node.id'),
        info={'colanderalchemy': {'exclude': deform.widget.HiddenWidget()}},
        primary_key=True,
    )
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
                'title': u"Statut",
                'widget': deform.widget.SelectWidget(
                    values=zip(ALL_STATES, ALL_STATES)
                )
            }
        }
    )
    statusComment = Column(
        Text,
        info={
            "colanderalchemy": {
                "title": u"Commentaires",
                'widget': deform.widget.TextAreaWidget()
            }
        },
    )
    statusPerson = Column(
        ForeignKey('accounts.id'),
        info={
            'colanderalchemy': {
                "title": u"Dernier utilisateur à avoir modifié le document",
                'widget': get_deferred_user_choice()
            },
            "export": {'exclude': True},
        },
    )
    statusDate = Column(
        CustomDateType,
        default=get_current_timestamp,
        info={
            'colanderalchemy': {
                "title": u"Date du dernier changement de statut",
                'typ': colander.Date
            }
        }
    )
    date = Column(
        Date(),
        info={
            "colanderalchemy": {
                "title": u"Date du document",
            }
        },
        default=datetime.date.today
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
        info={
            'colanderalchemy': {
                "title": u"Objet",
                'widget': deform.widget.TextAreaWidget()
            }
        },
    )
    ht = Column(
        BigInteger(),
        info={
            'colanderalchemy': {
                "title": u"Montant HT (cache)",
                "typ": AmountType(5),
            }
        },
        default=0)
    tva = Column(
        BigInteger(),
        info={
            'colanderalchemy': {
                "title": u"Montant TVA (cache)",
                "typ": AmountType(5),
            }
        },
        default=0)
    ttc = Column(
        BigInteger(),
        info={
            'colanderalchemy': {
                "title": u"Montant TTC (cache)",
                "typ": AmountType(5),
            }
        },
        default=0
    )
    company_id = Column(
        Integer,
        ForeignKey('company.id'),
        info={'colanderalchemy': {'exclude': True}},
    )
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
    project_index = deferred(
        Column(
            Integer,
            info={
                'colanderalchemy': {
                    "title": u"Index dans le projet",
                }
            },
        ),
        group='edit',
    )
    company_index = deferred(
        Column(
            Integer,
            info={
                'colanderalchemy': {
                    "title": u"Index du document à l'échelle de l'entreprise",
                }
            },
        ),
        group='edit',
    )
    # TODO : remove in version > 3.3.0
    _number = Column(
        String(100),
        info={
            'colanderalchemy': {'exclude': True}
        },
    )
    official_number = Column(
        Integer,
        info={
            'colanderalchemy': {
                "title": u"Identifiant du document (facture/avoir)"
            }
        },
        default=None)

    internal_number = deferred(
        Column(
            String(255),
            default=None,
            info={
                'colanderalchemy': {
                    "title": u"Identifiant du document dans la CAE",
                }
            }
        ),
        group='edit'
    )

    display_units = deferred(
        Column(
            Integer,
            info={
                'colanderalchemy': {
                    "title": u"Afficher le détail ?",
                }
            },
            default=0
        ),
        group='edit'
    )

    # Not used in latest invoices
    expenses = deferred(
        Column(
            BigInteger(),
            info={
                'colanderalchemy': {'exclude': True}
            },
            default=0
        ),
        group='edit'
    )

    expenses_ht = deferred(
        Column(
            BigInteger(),
            info={
                'colanderalchemy': {'title': u'Frais'}
            },
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
                    'title': u'Adresse',
                    'widget': deform.widget.TextAreaWidget()
                }
            },
        ),
        group='edit',
    )
    workplace = deferred(
        Column(
            Text,
            default='',
            info={
                'colanderalchemy': {
                    'title': u"Lieu d'éxécution des travaux",
                    'widget': deform.widget.TextAreaWidget(),
                }
            }
        )
    )
    payment_conditions = deferred(
        Column(
            Text,
            info={
                'colanderalchemy': {
                    "title": u"Conditions de paiement",
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
                    'exlude': True,
                    'title': u"Méthode d'arrondi 'à l'ancienne' ? (floor)"
                }
            }
        ),
        group='edit',
    )
    prefix = Column(
        String(15),
        default='',
        info={
            "colanderalchemy": {
                'title': u"Préfixe du numéro de document",
            }
        }
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
            order_by='Task.date',
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

    discounts = relationship(
        "DiscountLine",
        info={'colanderalchemy': {'title': u"Remises"}},
        order_by='DiscountLine.tva',
        cascade="all, delete-orphan",
        back_populates='task',
    )

    company = relationship(
        "Company",
        primaryjoin="Task.company_id==Company.id",
        info={
            'colanderalchemy': forms.EXCLUDED,
            'export': {'exclude': True},
        },
    )

    project = relationship(
        "Project",
        primaryjoin="Task.project_id==Project.id",
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
            order_by='Task.date',
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
        info={'colanderalchemy': {'exclude': True}},
        backref=backref(
            'task',
        ),
        order_by='Payment.date',
        cascade="all, delete-orphan"
    )
    mentions = relationship(
        "TaskMention",
        secondary=TASK_MENTION,
        order_by="TaskMention.order",
        back_populates="tasks",
        info={
            "colanderalchemy": {'exclude': True}
        },
    )
    line_groups = relationship(
        "TaskLineGroup",
        order_by='TaskLineGroup.order',
        cascade="all, delete-orphan",
        info={'colanderalchemy': {'title': u"Unités d'oeuvre"}},
        primaryjoin="TaskLineGroup.task_id==Task.id",
        back_populates='task',
    )

    _name_tmpl = u"Task {}"
    _number_tmpl = u"{s.project.code}_{s.customer.code}_T{s.project_index}\
_{s.date:%m%y}"

    state_machine = DEFAULT_STATE_MACHINES['base']

    def __init__(self, company, customer, project, phase, user):
        company_index = self._get_company_index(company)
        project_index = self._get_project_index(project)

        self.CAEStatus = self.state_machine.default_state
        self.company = company
        self.customer = customer
        self.project = project
        self.phase = phase
        self.owner = user
        self.statusPersonAccount = user
        self.date = datetime.date.today()
        self.set_numbers(company_index, project_index)

        # We add a default task line group
        self.line_groups.append(TaskLineGroup(order=0))

    def _get_project_index(self, project):
        """
        Return the index of the current object in the associated project
        :param obj project: A Project instance in which we will look to get the
        current doc index
        :returns: The next number
        :rtype: int
        """
        raise NotImplemented("Implement this method please")

    def _get_company_index(self, company):
        """
        Return the index of the current object in the associated company
        :param obj company: A Company instance in which we will look to get the
        current doc index
        :returns: The next number
        :rtype: int
        """
        raise NotImplemented("Implement this method please")

    def set_numbers(self, company_index, project_index):
        """
        Handle all attributes related to the given number

        :param int company_index: The index of the task in the company
        :param int project_index: The index of the task in its project
        """
        if company_index is None or project_index is None:
            raise Exception("Indexes should not be None")

        self.company_index = company_index
        self.project_index = project_index

        self.internal_number = self._number_tmpl.format(s=self)
        self.name = self._name_tmpl.format(project_index)

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
            date=self.date,
            owner_id=self.owner_id,
            customer_id=self.customer_id,
            display_units=self.display_units,
            expenses_ht=self.expenses_ht,
            address=self.address,
            workplace=self.workplace,
            payment_conditions=self.payment_conditions,
            description=self.description,
            prefix=self.prefix,
            mentions=[
                mention.__json__(request)
                for mention in self.mentions
            ],
            lines=[
                line.__json__(request)
                for line in self.default_line_group.lines
            ],
            groups=[
                group.__json__(request) for group in self.get_groups()
                if group.id != self.default_line_group.id
            ],
            status_history=[
                status.__json__(request) for status in self.statuses
            ],
            discounts=[
                discount.__json__(request) for discount in self.discounts
            ],
            statusComment=self.statusComment,
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
        return self.company

    def get_customer(self):
        """
            Return the customer of the current task
        """
        return self.customer

    def get_company_id(self):
        """
            Return the id of the company owning this task
        """
        return self.company.id

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

    def get_groups(self):
        return [group for group in self.line_groups if group.lines]

    @property
    def all_lines(self):
        """
        Returns a list with all task lines of the current task
        """
        result = []
        for group in self.line_groups:
            result.extend(group.lines)
        return result

    def get_tva_objects(self):
        return self._autonomie_service.get_tva_objects(self)

    @classmethod
    def get_valid_tasks(cls, *args):
        return cls._autonomie_service.get_valid_tasks(cls, *args)

    @classmethod
    def get_waiting_estimations(cls, *args):
        return cls._autonomie_service.get_waiting_estimations(*args)

    @classmethod
    def get_waiting_invoices(cls, *args):
        return cls._autonomie_service.get_waiting_invoices(cls, *args)


class DiscountLine(DBBASE, DiscountLineCompute):
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
    amount = Column(
        BigInteger(),
        info={'colanderalchemy': {'typ': AmountType(5), 'title': 'Montant'}},
    )
    description = Column(
        Text,
        info={'colanderalchemy': {'widget': deform.widget.TextAreaWidget()}}
    )
    task = relationship(
        "Task",
        uselist=False,
        info={'colanderalchemy': {'exclude': True}},
    )

    def __json__(self, request):
        return dict(
            description=self.description,
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

    def __repr__(self):
        return u"<DiscountLine amount : {s.amount} tva:{s.tva} id:{s.id}>"\
            .format(s=self)


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
            lines=[line.__json__(request) for line in self.lines]
        )

    def duplicate(self):
        group = TaskLineGroup(
            title=self.title,
            description=self.description,
            task_id=self.task_id,
            lines=[line.duplicate() for line in self.lines],
            order=self.order,
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
    cost = Column(
        BigInteger(),
        info={'colanderalchemy': {'typ': AmountType(5), 'title': 'Montant'}},
        default=0,
    )
    tva = Column(
        Integer,
        info={'colanderalchemy': {'typ': AmountType(2), 'title': 'Tva (en %)'}},
        nullable=False,
        default=196
    )
    quantity = Column(
        Float(),
        info={'colanderalchemy': {'typ': QuantityType()}},
        default=1)
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

    def __json__(self, request):
        result = dict(
            id=self.id,
            order=self.order,
            cost=self.cost,
            tva=self.tva,
            description=self.description,
            quantity=self.quantity,
            unity=self.unity,
            group_id=self.group_id,
        )
        if self.product_id is not None:
            result['product_id'] = self.product_id
        return result

    @property
    def task(self):
        return self.group.task


def cache_amounts(mapper, connection, target):
    """
    Set amounts in the cached amount vars to be able to provide advanced search
    ... options in the invoice list page
    """
    log.info("Caching the task amounts")
    if hasattr(target, 'total_ht'):
        target.ht = target.total_ht()
    if hasattr(target, 'total'):
        target.ttc = target.total()
    if hasattr(target, 'tva_amount'):
        target.tva = target.tva_amount()


def cache_parent_amounts(mapper, connection, target):
    """
    Set amounts in the cached amount vars to be able to provide advanced search
    ... options in the invoice list page
    """
    log.info("Caching the parent task amounts")
    print(target)
    if hasattr(target, 'task'):
        print("target has a task")
        task = target.task
        print(task)
        if hasattr(task, 'total_ht'):
            task.ht = task.total_ht()
        if hasattr(task, 'total'):
            task.ttc = task.total()
        if hasattr(task, 'tva_amount'):
            task.tva = task.tva_amount()
        DBSESSION().merge(task)


listen(Task, "before_insert", cache_amounts, propagate=True)
listen(Task, "before_update", cache_amounts, propagate=True)
listen(TaskLine, "before_insert", cache_parent_amounts, propagate=True)
listen(TaskLine, "before_update", cache_parent_amounts, propagate=True)
listen(DiscountLine, "before_insert", cache_parent_amounts, propagate=True)
listen(DiscountLine, "before_update", cache_parent_amounts, propagate=True)
