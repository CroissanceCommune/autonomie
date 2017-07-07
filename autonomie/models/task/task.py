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
)
from sqlalchemy.event import listen

from sqlalchemy.orm import (
    relationship,
    validates,
    deferred,
    backref,
)

from autonomie.models.tva import (
    Tva,
    Product,
)
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie import forms
from autonomie.forms.custom_types import (AmountType, QuantityType,)
from autonomie.models.user import get_deferred_user_choice

from .interfaces import ITask
from autonomie.compute.task import (
    LineCompute,
    DiscountLineCompute,
    GroupCompute,
)
from autonomie.models.node import Node
from autonomie.models.task.mentions import (
    TASK_MENTION,
    TaskMention,
)
from autonomie.models.task.unity import WorkUnit


log = logging.getLogger(__name__)


ALL_STATES = ('draft', 'wait', 'valid', 'invalid')
# , 'geninv', 'aboest', 'gencinv', 'resulted', 'paid', )


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

        tvas = Tva.query().filter(
            Tva.value.in_(list(tva_values))
        ).all()
        return dict([(tva.value, tva) for tva in tvas])

    @classmethod
    def get_valid_tasks(cls, task_cls, *args):
        from autonomie.models.task import Invoice, CancelInvoice
        query = super(task_cls, task_cls).query(*args)
        query = query.with_polymorphic([Invoice, CancelInvoice])
        query = query.filter(task_cls.status == 'valid')
        query = query.filter(task_cls.type_.in_(('invoice', 'cancelinvoice')))
        return query

    @classmethod
    def get_waiting_estimations(cls, *args):
        from autonomie.models.task import Estimation
        query = Estimation.query(*args)
        query = query.filter(Estimation.status == 'wait')
        query = query.order_by(Estimation.status_date)
        return query

    @classmethod
    def get_waiting_invoices(cls, task_cls, *args):
        from autonomie.models.task import Invoice, CancelInvoice
        query = super(task_cls, task_cls).query(*args)
        query = query.with_polymorphic([Invoice, CancelInvoice])
        query = query.filter(task_cls.type_.in_(('invoice', 'cancelinvoice')))
        query = query.filter(task_cls.status == 'wait')
        query = query.order_by(task_cls.type_).order_by(task_cls.status_date)
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
    status = Column(
        String(10),
        info={
            'colanderalchemy': {
                'title': u"Statut",
                'widget': deform.widget.SelectWidget(
                    values=zip(ALL_STATES, ALL_STATES)
                ),
                "validator": colander.OneOf(ALL_STATES),
            }
        }
    )
    status_comment = Column(
        Text,
        info={
            "colanderalchemy": {
                "title": u"Commentaires",
                'widget': deform.widget.TextAreaWidget()
            }
        },
    )
    status_person_id = Column(
        ForeignKey('accounts.id'),
        info={
            'colanderalchemy': {
                "title": u"Dernier utilisateur à avoir modifié le document",
                'widget': get_deferred_user_choice()
            },
            "export": {'exclude': True},
        },
    )
    status_date = Column(
        Date(),
        default=datetime.date.today,
        info={
            'colanderalchemy': {
                "title": u"Date du dernier changement de statut",
            }
        }
    )
    date = Column(
        Date(),
        info={
            "colanderalchemy": {
                "title": u"Date du document",
                "missing": colander.required
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
    description = Column(
        Text,
        info={
            'colanderalchemy': {
                "title": u"Objet",
                'widget': deform.widget.TextAreaWidget(),
                'validator': forms.textarea_node_validator,
                'missing': colander.required,
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
        default=0
    )
    tva = Column(
        BigInteger(),
        info={
            'colanderalchemy': {
                "title": u"Montant TVA (cache)",
                "typ": AmountType(5),
            }
        },
        default=0
    )
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
    official_number = Column(
        Integer,
        info={
            'colanderalchemy': {
                "title": u"Identifiant du document (facture/avoir)",
            }
        },
        default=None,
    )

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
                    "validator": colander.OneOf((0, 1))
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
                'colanderalchemy': {
                    'title': u'Frais',
                    'validator': forms.positive_validator
                }
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
                    'widget': deform.widget.TextAreaWidget(),
                    'validator': forms.textarea_node_validator,
                    'missing': colander.required,
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
                    'widget': deform.widget.TextAreaWidget(),
                    'validator': forms.textarea_node_validator
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

    # Organisationnal Relationships
    status_person = relationship(
        "User",
        primaryjoin="Task.status_person_id==User.id",
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
    # Content relationships
    discounts = relationship(
        "DiscountLine",
        info={'colanderalchemy': {'title': u"Remises"}},
        order_by='DiscountLine.tva',
        cascade="all, delete-orphan",
        back_populates='task',
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
            'colanderalchemy': {
                'children': forms.get_sequence_child_item(TaskMention),
            }
        },
    )

    line_groups = relationship(
        "TaskLineGroup",
        order_by='TaskLineGroup.order',
        cascade="all, delete-orphan",
        info={
            'colanderalchemy': {
                'title': u"Unités d'oeuvre",
                "validator": colander.Length(
                    min=1,
                    min_err=u"Une entrée est requise"
                ),
                "missing": colander.required
            }
        },
        primaryjoin="TaskLineGroup.task_id==Task.id",
        back_populates='task',
    )

    _name_tmpl = u"Task {}"
    _number_tmpl = u"{s.project.code}_{s.customer.code}_T{s.project_index}\
_{s.date:%m%y}"

    state_manager = None

    def __init__(self, company, customer, project, phase, user):
        company_index = self._get_company_index(company)
        project_index = self._get_project_index(project)

        self.status = 'draft'
        self.company = company
        self.customer = customer
        self.address = customer.full_address
        self.project = project
        self.phase = phase
        self.owner = user
        self.status_person = user
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
        return -1

    def _get_company_index(self, company):
        """
        Return the index of the current object in the associated company
        :param obj company: A Company instance in which we will look to get the
        current doc index
        :returns: The next number
        :rtype: int
        """
        return -1

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
            id=self.id,
            name=self.name,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat(),

            phase_id=self.phase_id,
            status=self.status,
            status_comment=self.status_comment,
            status_person_id=self.status_person_id,
            # status_date=self.status_date.isoformat(),
            date=self.date.isoformat(),
            owner_id=self.owner_id,
            description=self.description,
            ht=self.ht,
            tva=self.tva,
            ttc=self.ttc,
            company_id=self.company_id,
            project_id=self.project_id,
            customer_id=self.customer_id,
            project_index=self.project_index,
            company_index=self.company_index,
            official_number=self.official_number,
            internal_number=self.internal_number,
            display_units=self.display_units,
            expenses_ht=self.expenses_ht,
            address=self.address,
            workplace=self.workplace,
            payment_conditions=self.payment_conditions,
            prefix=self.prefix,
            status_history=[
                status.__json__(request) for status in self.statuses
            ],
            discounts=[
                discount.__json__(request) for discount in self.discounts
            ],
            payments=[
                payment.__json__(request) for payment in self.payments
            ],
            mentions=[
                mention.__json__(request)
                for mention in self.mentions
            ],
            line_groups=[
                group.__json__(request) for group in self.line_groups
            ],
        )

    def set_status(self, status, request, **kw):
        """
        set the status of a task through the state machine
        """
        return self.state_manager.process(
            status,
            self,
            request,
            **kw
        )

    def is_invoice(self):
        return False

    def is_estimation(self):
        return False

    def is_cancelinvoice(self):
        return False

    @validates('status')
    def change_status(self, key, status):
        """
        fired on status change, stores a new taskstatus for each status change
        """
        log.debug(u"# Task status change #")

        actual_status = self.status
        self.status_date = datetime.date.today()

        log.debug(u" + was {0}, becomes {1}".format(actual_status, status))
        if self.status_person is not None:
            # Can append in old dbs that are inconsistent
            status_record = TaskStatus(
                status_code=status,
                status_person_id=self.status_person.id,
                status_comment=self.status_comment,
                date=self.status_date,
            )
            self.statuses.append(status_record)

        return status

    def get_next_actions(self):
        """
            Return the next available actions regarding the current status
        """
        return self.state_machine.get_next_states(self.status)

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
        return u"<Task status:{s.status} id:{s.id}>".format(s=self)

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
        info={
            'colanderalchemy': {
                'title': u"Identifiant du document",
                'missing': colander.required,
            }
        }
    )
    description = Column(
        Text,
        info={
            'colanderalchemy': {
                'widget': deform.widget.TextAreaWidget(),
                'validator': forms.textarea_node_validator,
            }
        }
    )
    amount = Column(
        BigInteger(),
        info={
            'colanderalchemy': {
                'typ': AmountType(5),
                'title': 'Montant',
                'missing': colander.required,
            }
        },
    )
    tva = Column(
        Integer,
        nullable=False,
        default=196,
        info={
            "colanderalchemy": {
                "typ": AmountType(2),
                "validator": forms.get_deferred_select_validator(
                    Tva, id_key='value'
                ),
                "missing": colander.required
            }
        }
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
    status_code = Column(String(10))
    status_comment = Column(
        Text,
        info={"colanderalchemy": {'widget': deform.widget.TextAreaWidget()}},
    )
    status_person_id = Column(Integer, ForeignKey('accounts.id'))
    status_date = Column(
        Date(),
        default=datetime.date.today,
    )

    task = relationship(
        "Task",
        backref=backref(
            "statuses",
            cascade="all, delete-orphan",
            info={'colanderalchemy': forms.EXCLUDED}
        )
    )
    status_person = relationship(
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
        result = dict(date=self.status_date)
        result['code'] = self.status_code
        if self.status_person is not None:
            result['account'] = self.status_person.__json__(request)
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
        info={
            'colanderalchemy': {
                'title': u"Identifiant du document",
                'missing': colander.required,
            }
        }
    )
    description = Column(Text(), default="")
    title = Column(String(255), default="")
    order = Column(Integer, default=1)

    task = relationship(
        "Task",
        primaryjoin="TaskLineGroup.task_id==Task.id",
        info={'colanderalchemy': forms.EXCLUDED}
    )
    lines = relationship(
        "TaskLine",
        order_by='TaskLine.order',
        cascade="all, delete-orphan",
        back_populates='group',
        info={
            'colanderalchemy': {
                'title': u"Prestations",
                'validator': colander.Length(
                    min=1,
                    min_err=u"Une prestation au moins doit être incluse",
                )
            }
        }
    )

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


@colander.deferred
def deferred_tva_product_validator(node, kw):
    product_id = node.get('product_id')
    if product_id is not None:
        tva_id = node.get('tva_id')
        if tva_id is not None:
            tva = Tva.get(tva_id)
            if product_id not in [p.id for p in tva.products]:
                exc = colander.Invalid(
                    node,
                    u"Ce produit ne correspond pas à la TVA configurée"
                )
                exc['title'] = u"Le code produit doit correspondre à la TVA \
                    configuré pour cette prestation"
                raise exc


class TaskLine(DBBASE, LineCompute):
    """
        Estimation/Invoice/CancelInvoice lines
    """
    __colanderalchemy_config__ = {
        'validator': deferred_tva_product_validator
    }
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
                ),
                'validator': forms.textarea_node_validator,
            }
        },
    )
    cost = Column(
        BigInteger(),
        info={
            'colanderalchemy': {
                'typ': AmountType(5),
                'title': 'Montant',
                'missing': colander.required,
            }
        },
        default=0,
    )
    quantity = Column(
        Float(),
        info={
            'colanderalchemy': {
                "title": u"Quantité",
                'typ': QuantityType(),
                'missing': colander.required,
            }
        },
        default=1
    )
    unity = Column(
        String(100),
        info={
            'colanderalchemy': {
                'title': u"Unité",
                'validator': forms.get_deferred_select_validator(
                    WorkUnit, id_key='label',
                ),
                'missing': colander.required,
            }
        },

    )
    tva = Column(
        Integer,
        info={
            'colanderalchemy': {
                'typ': AmountType(2),
                'title': 'Tva (en %)',
                'validator': forms.get_deferred_select_validator(
                    Tva, id_key='value'
                ),
                'missing': colander.required
            }
        },
        nullable=False,
        default=196
    )
    product_id = Column(
        Integer,
        info={
            'colanderalchemy': {
                'validator': forms.get_deferred_select_validator(Product),
                'missing': colander.drop,
            }
        }
    )
    group = relationship(
        TaskLineGroup,
        primaryjoin="TaskLine.group_id==TaskLineGroup.id",
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


listen(Task, "before_insert", cache_amounts, propagate=True)
listen(Task, "before_update", cache_amounts, propagate=True)
listen(TaskLine, "before_insert", cache_parent_amounts, propagate=True)
listen(TaskLine, "before_update", cache_parent_amounts, propagate=True)
listen(DiscountLine, "before_insert", cache_parent_amounts, propagate=True)
listen(DiscountLine, "before_update", cache_parent_amounts, propagate=True)
