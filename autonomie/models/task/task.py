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
from sqlalchemy.ext.orderinglist import ordering_list

from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
    DBSESSION,
)

from autonomie.utils.strings import (
    format_status_string,
)
from autonomie.compute.task import (
    LineCompute,
    DiscountLineCompute,
    GroupCompute,
)
from autonomie.compute.math_utils import (
    integer_to_amount,
    amount,
)
from autonomie.models.node import Node
from autonomie.models.project.business import Business
from autonomie.models.services.task_mentions import (
    TaskMentionService,
)
from autonomie.models.services.sale_file_requirements import (
    TaskFileRequirementService,
)
from autonomie.models.task.mentions import (
    MANDATORY_TASK_MENTION,
    TASK_MENTION,
)
from autonomie.models.tva import (
    Tva,
)


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


class Task(Node):
    """
        Metadata pour une tâche (estimation, invoice)
    """
    __tablename__ = 'task'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'task'}
    _autonomie_service = TaskService
    file_requirement_service = TaskFileRequirementService
    mention_service = TaskMentionService

    id = Column(
        Integer,
        ForeignKey('node.id'),
        info={'export': {'exclude': True}},
        primary_key=True,
    )
    phase_id = Column(
        ForeignKey('phase.id'),
        info={"export": {'exclude': True}},
    )
    status = Column(
        String(10),
        info={
            'colanderalchemy': {'title': u"Statut"},
            'export': {'exclude': True}
        }
    )
    status_comment = Column(
        Text,
        info={
            "colanderalchemy": {"title": u"Commentaires"},
            'export': {'exclude': True}
        },
        default="",
    )
    status_person_id = Column(
        ForeignKey('accounts.id'),
        info={
            'colanderalchemy': {
                "title": u"Dernier utilisateur à avoir modifié le document",
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
            },
            'export': {'exclude': True}
        }
    )
    date = Column(
        Date(),
        info={"colanderalchemy": {"title": u"Date du document"}},
        default=datetime.date.today
    )
    owner_id = Column(
        ForeignKey('accounts.id'),
        info={
            "export": {'exclude': True},
        },
    )
    description = Column(
        Text,
        info={'colanderalchemy': {"title": u"Objet"}},
    )
    ht = Column(
        BigInteger(),
        info={
            'colanderalchemy': {"title": u"Montant HT (cache)"},
            'export': {'exclude': True},
        },
        default=0
    )
    tva = Column(
        BigInteger(),
        info={
            'colanderalchemy': {"title": u"Montant TVA (cache)"},
            'export': {'exclude': True},
        },
        default=0
    )
    ttc = Column(
        BigInteger(),
        info={
            'colanderalchemy': {"title": u"Montant TTC (cache)"},
            'export': {'exclude': True},
        },
        default=0
    )
    company_id = Column(
        Integer,
        ForeignKey('company.id'),
        info={
            'export': {'exclude': True},
        },
    )
    project_id = Column(
        Integer,
        ForeignKey('project.id'),
        info={
            'export': {'exclude': True},
        },
    )
    customer_id = Column(
        Integer,
        ForeignKey('customer.id'),
        info={
            'export': {'exclude': True},
        },
    )
    project_index = deferred(
        Column(
            Integer,
            info={
                'colanderalchemy': {
                    "title": u"Index dans le projet",
                },
                'export': {'exclude': True},
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
                },
                'export': {'exclude': True},
            },
        ),
        group='edit',
    )
    official_number = Column(
        String(255),
        info={
            'colanderalchemy': {
                "title": u"Identifiant du document (facture/avoir)",
            },
            'export': {'label': u"Numéro de facture"},
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
                },
                'export': {'exclude': True},
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
                },
                'export': {'exclude': True},
            },
            default=0
        ),
        group='edit'
    )

    expenses_ht = deferred(
        Column(
            BigInteger(),
            info={
                'colanderalchemy': {'title': u'Frais'},
                'export': {'exclude': True},
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
                'colanderalchemy': {'title': u'Adresse'},
                'export': {'exclude': True},
            },
        ),
        group='edit',
    )
    workplace = deferred(
        Column(
            Text,
            default='',
            info={
                'colanderalchemy': {'title': u"Lieu d'éxécution des travaux"},
            }
        )
    )
    payment_conditions = deferred(
        Column(
            Text,
            info={
                'colanderalchemy': {
                    "title": u"Conditions de paiement",
                },
                'export': {'exclude': True},
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
                },
                'export': {'exclude': True},
            }
        ),
        group='edit',
    )
    business_type_id = Column(ForeignKey("business_type.id"))
    business_id = Column(ForeignKey("business.id"))

    # Organisationnal Relationships
    status_person = relationship(
        "User",
        primaryjoin="Task.status_person_id==User.id",
        backref=backref(
            "taskStatuses",
            info={
                'colanderalchemy': {'exclude': True},
                'export': {'exclude': True},
            },
        ),
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        },
    )
    owner = relationship(
        "User",
        primaryjoin="Task.owner_id==User.id",
        backref=backref(
            "ownedTasks",
            info={
                'colanderalchemy': {'exclude': True},
                'export': {'exclude': True},
            },
        ),
        info={
            'colanderalchemy': {'exclude': True},
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
                'colanderalchemy': {'exclude': True},
                'export': {'exclude': True},
            },
        ),
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        },
    )

    company = relationship(
        "Company",
        primaryjoin="Task.company_id==Company.id",
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'related_key': "name", "label": "Entreprise"},
        },
    )

    project = relationship(
        "Project",
        primaryjoin="Task.project_id==Project.id",
        info={
            'colanderalchemy': {'exclude': True},
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
                'colanderalchemy': {'exclude': True},
                "export": {'exclude': True},
            },
        ),
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'related_key': 'label', 'label': u"Client"},
        },
    )
    business_type = relationship(
        "BusinessType",
        info={'colanderalchemy': {'exclude': True}}
    )
    business = relationship(
        "Business",
        primaryjoin="Business.id==Task.business_id",
        info={'colanderalchemy': {'exclude': True}}
    )

    # Content relationships
    discounts = relationship(
        "DiscountLine",
        info={
            'colanderalchemy': {'title': u"Remises"},
            'export': {'exclude': True},
        },
        order_by='DiscountLine.tva',
        cascade="all, delete-orphan",
        back_populates='task',
    )

    payments = relationship(
        "Payment",
        primaryjoin="Task.id==Payment.task_id",
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        },
        order_by='Payment.date',
        cascade="all, delete-orphan",
        back_populates='task',
    )

    mentions = relationship(
        "TaskMention",
        secondary=TASK_MENTION,
        order_by="TaskMention.order",
        info={'export': {'exclude': True}},
    )

    mandatory_mentions = relationship(
        "TaskMention",
        secondary=MANDATORY_TASK_MENTION,
        order_by="TaskMention.order",
        info={'export': {'exclude': True}},
    )

    line_groups = relationship(
        "TaskLineGroup",
        order_by='TaskLineGroup.order',
        cascade="all, delete-orphan",
        collection_class=ordering_list('order'),
        info={
            'colanderalchemy': {
                'title': u"Unités d'oeuvre",
                "validator": colander.Length(
                    min=1,
                    min_err=u"Une entrée est requise"
                ),
                "missing": colander.required
            },
            'export': {'exclude': True},
        },
        primaryjoin="TaskLineGroup.task_id==Task.id",
        back_populates='task',
    )

    statuses = relationship(
        "TaskStatus",
        order_by="desc(TaskStatus.status_date), desc(TaskStatus.id)",
        cascade="all, delete-orphan",
        back_populates='task',
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True},
        }
    )

    # Not used in latest invoices
    expenses = deferred(
        Column(
            BigInteger(),
            info={
                'export': {'exclude': True},
            },
            default=0
        ),
        group='edit'
    )

    _name_tmpl = u"Task {}"
    _number_tmpl = u"{s.project.code}_{s.customer.code}_T{s.project_index}\
_{s.date:%m%y}"

    state_manager = None

    def __init__(self, user, company, **kw):
        project = kw['project']
        company_index = self._get_company_index(company)
        project_index = self._get_project_index(project)

        self.status = 'draft'
        self.company = company
        customer = kw['customer']
        self.address = customer.full_address
        self.owner = user
        self.status_person = user
        self.date = datetime.date.today()
        self.set_numbers(company_index, project_index)

        for key, value in kw.items():
            setattr(self, key, value)

        # We add a default task line group
        self.line_groups.append(TaskLineGroup(order=0))

    def initialize_business_datas(self, business=None):
        """
        Initialize the business datas related to this task

        :param obj business: instance of
        :class:`autonomie.models.project.business.Business`
        """
        if business is not None:
            self.business = business

        self.file_requirement_service.populate(self)
        self.mention_service.populate(self)

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
            ht=integer_to_amount(self.ht, 5),
            tva=integer_to_amount(self.tva, 5),
            ttc=integer_to_amount(self.ttc, 5),
            company_id=self.company_id,
            project_id=self.project_id,
            customer_id=self.customer_id,
            project_index=self.project_index,
            company_index=self.company_index,
            official_number=self.official_number,
            internal_number=self.internal_number,
            display_units=self.display_units,
            expenses_ht=integer_to_amount(self.expenses_ht, 5),
            address=self.address,
            workplace=self.workplace,
            payment_conditions=self.payment_conditions,
            status_history=[
                status.__json__(request) for status in self.statuses
            ],
            discounts=[
                discount.__json__(request) for discount in self.discounts
            ],
            payments=[
                payment.__json__(request) for payment in self.payments
            ],
            mentions=[mention.id for mention in self.mentions],
            line_groups=[
                group.__json__(request) for group in self.line_groups
            ],
            attachments=[
                f.__json__(request)for f in self.children if f.type_ == 'file'
            ]
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

    def check_status_allowed(self, status, request, **kw):
        return self.state_manager.check_allowed(status, self, request)

    @validates('status')
    def change_status(self, key, status):
        """
        fired on status change, stores a new taskstatus for each status change
        """
        log.debug(u"# Task status change #")
        actual_status = self.status
        log.debug(u" + was {0}, becomes {1}".format(actual_status, status))
        return status

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

    def gen_business(self):
        """
        Generate a business based on this Task

        :returns: A new business instance
        :rtype: :class:`autonomie.models.project.business.Business`
        """
        business = Business(
            name=self.name,
            project_id=self.project_id,
            business_type_id=self.business_type_id,
        )
        business.file_requirement_service.populate(self)
        DBSESSION().add(business)
        DBSESSION().flush()
        self.business_id = business.id
        DBSESSION().merge(self)
        return business

    def is_training(self):
        return self.business_type.name == 'training'


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
            }
        }
    )
    description = Column(Text)
    amount = Column(
        BigInteger(),
        info={'colanderalchemy': {'title': 'Montant'}}
    )
    tva = Column(Integer, nullable=False, default=0)
    task = relationship(
        "Task",
        uselist=False,
        info={'colanderalchemy': {'exclude': True}},
    )

    def __json__(self, request):
        return dict(
            id=self.id,
            task_id=self.task_id,
            description=self.description,
            amount=integer_to_amount(self.amount, 5),
            tva=integer_to_amount(self.tva, 2),
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

    task = relationship("Task")
    status_person = relationship(
        "User",
        backref=backref(
            "task_statuses",
            info={
                'colanderalchemy': {'exclude': True},
                'export': {'exclude': True},
            },
        )
    )

    def __json__(self, request):
        result = {
            "date": self.status_date,
            'code': self.status_code,
            "label": format_status_string(self.status_code),
            "comment": self.status_comment,
        }
        if self.status_person is not None:
            result['account'] = self.status_person.label
        return result


class TaskLineGroup(DBBASE, GroupCompute):
    """
    Group of lines
    """
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    task_id = Column(
        Integer,
        ForeignKey('task.id', ondelete="cascade"),
        info={
            'colanderalchemy': {
                'title': u"Identifiant du document",
            }
        }
    )
    description = Column(Text(), default="")
    title = Column(String(255), default="")
    order = Column(Integer, default=1)

    task = relationship(
        "Task",
        primaryjoin="TaskLineGroup.task_id==Task.id",
        info={'colanderalchemy': {'exclude': True}}
    )
    lines = relationship(
        "TaskLine",
        order_by='TaskLine.order',
        cascade="all, delete-orphan",
        back_populates='group',
        collection_class=ordering_list('order'),
        info={
            'colanderalchemy': {
                'title': u"Prestations",
            }
        }
    )

    def __json__(self, request):
        return dict(
            id=self.id,
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

    @classmethod
    def from_sale_product_group(cls, sale_product_group):
        """
        Build an instance based on the given sale_product_group

        :param obj sale_product_group: A SaleProductGroup instance
        :returns: A TaskLineGroup instance
        """
        result = cls()
        result.title = sale_product_group.title
        result.description = sale_product_group.label
        for product in sale_product_group.products:
            result.lines.append(TaskLine.from_sale_product(product))
        return result


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
        info={'colanderalchemy': {'exclude': True}}
    )
    order = Column(Integer, default=1,)
    description = Column(Text)
    cost = Column(
        BigInteger(),
        info={
            'colanderalchemy': {
                'title': 'Montant',
            }
        },
        default=0,
    )
    quantity = Column(
        Float(),
        info={
            'colanderalchemy': {"title": u"Quantité"}
        },
        default=1
    )
    unity = Column(
        String(100),
        info={
            'colanderalchemy': {'title': u"Unité"}
        },
    )
    tva = Column(
        Integer,
        info={'colanderalchemy': {'title': 'Tva (en %)'}},
        nullable=False,
        default=2000
    )
    product_id = Column(Integer)
    group = relationship(
        TaskLineGroup,
        primaryjoin="TaskLine.group_id==TaskLineGroup.id",
        info={'colanderalchemy': {'exclude': True}}
    )
    product = relationship(
        "Product",
        primaryjoin="Product.id==TaskLine.product_id",
        uselist=False,
        foreign_keys=product_id,
        info={'colanderalchemy': {'exclude': True}}
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
            cost=integer_to_amount(self.cost, 5),
            tva=integer_to_amount(self.tva, 2),
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

    @classmethod
    def from_sale_product(cls, sale_product):
        """
        Build an instance based on the given sale_product

        :param obj sale_product: A SaleProduct instance
        :returns: A TaskLine instance
        """
        result = cls()
        result.description = sale_product.description
        result.cost = amount(sale_product.value, 5)
        result.tva = sale_product.tva
        result.unity = sale_product.unity
        result.quantity = 1
        return result


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
    if hasattr(target, 'task'):
        task = target.task
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
