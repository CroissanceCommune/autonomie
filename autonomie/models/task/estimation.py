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
    The estimation model
"""
import datetime
import logging

from zope.interface import implementer

from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    ForeignKey,
    Text,
    Boolean,
    Date,
)
from sqlalchemy.orm import (
    relationship,
    deferred,
)
from sqlalchemy.ext.orderinglist import ordering_list
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
    DBSESSION,
)
from autonomie.compute.task import (
    EstimationCompute,
)
from autonomie.compute.math_utils import integer_to_amount
from autonomie.models.tva import Product
from autonomie.interfaces import (
    IMoneyTask,
)
from autonomie.models.services.estimation import EstimationInvoicingService
from .invoice import (
    Invoice,
)
from .task import (
    Task,
    TaskLine,
    TaskLineGroup,
    TaskStatus,
)
from .actions import (
    DEFAULT_ACTION_MANAGER,
    SIGNED_ACTION_MANAGER,
)

logger = logging.getLogger(__name__)


PAYMENTDISPLAYCHOICES = (
    ('NONE', u"Les paiments ne sont pas affichés dans le PDF",),
    ('SUMMARY', u"Le résumé des paiements apparaît dans le PDF",),
    (
        'ALL',
        u"Le détail des paiements apparaît dans le PDF",
    ),
    (
        'ALL_NO_DATE',
        u"Le détail des paiements, sans les dates, apparaît dans le PDF",
    ),
)

ESTIMATION_STATES = (
    ('waiting', u"En attente"),
    ('send', u"Envoyé au client"),
    ('aborted', u'Annulé'),
    ('signed', u'Signé'),
)


@implementer(IMoneyTask)
class Estimation(Task, EstimationCompute):
    """
        Estimation Model
    """
    __tablename__ = 'estimation'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'estimation', }
    _invoicing_service = EstimationInvoicingService

    id = Column(
        ForeignKey('task.id'),
        primary_key=True,
    )
    signed_status = Column(
        String(10),
        default='waiting',
        info={
            'colanderalchemy': {
                'title': u'Statut du devis',
            }
        }
    )
    geninv = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {"title": u"Factures générées ?"},
        }
    )

    # common with only invoices
    deposit = Column(
        Integer,
        info={
            'colanderalchemy': {'title': u'Accompte (en %)'},
        },
        default=0
    )

    # Specific to estimations
    exclusions = deferred(
        Column(
            Text,
            info={'colanderalchemy': {'title': u"Notes"}}
        ),
        group='edit'
    )
    manualDeliverables = deferred(
        Column(
            Integer,
            info={
                'colanderalchemy': {
                    'title': u"Configuration manuelle des paiements"
                }
            },
            default=0,
        ),
        group='edit',
    )
    paymentDisplay = deferred(
        Column(
            String(20),
            info={
                'colanderalchemy': {'title': u"Affichage des paiements"},
            },
            default=PAYMENTDISPLAYCHOICES[0][0]
        ),
        group='edit'
    )
    payment_lines = relationship(
        "PaymentLine",
        order_by='PaymentLine.order',
        cascade="all, delete-orphan",
        back_populates='task',
        collection_class=ordering_list('order'),
        info={
            'colanderalchemy': {'title': u"Échéances de paiement"},
        }
    )
    invoices = relationship(
        "Invoice",
        primaryjoin="Estimation.id==Invoice.estimation_id",
        order_by="Invoice.date",
        back_populates="estimation",
        info={
            'colanderalchemy': {'exclude': True},
        }
    )
    state_manager = DEFAULT_ACTION_MANAGER['estimation']
    signed_state_manager = SIGNED_ACTION_MANAGER
    _number_tmpl = u"{s.company.name} {s.date:%Y-%m} D{s.company_index}"

    _name_tmpl = u"Devis {0}"

    def _get_project_index(self, project):
        """
        Return the index of the current object in the associated project
        :param obj project: A Project instance in which we will look to get the
        current doc index
        :returns: The next number
        :rtype: int
        """
        return project.get_next_estimation_index()

    def _get_company_index(self, company):
        """
        Return the index of the current object in the associated company
        :param obj company: A Company instance in which we will look to get the
        current doc index
        :returns: The next number
        :rtype: int
        """
        return company.get_next_estimation_index()

    def set_signed_status(self, status, request, **kw):
        """
        set the signed status of a task through the state machine
        """
        if request.user.id is not None:
            status_record = TaskStatus(
                status_code=status,
                status_person_id=request.user.id,
                status_comment="",
            )
            self.statuses.append(status_record)

        return self.signed_state_manager.process(
            status,
            self,
            request,
            **kw
        )

    def check_signed_status_allowed(self, status, request, **kw):
        return self.signed_state_manager.check_allowed(status, self, request)

    def gen_business(self):
        """
        Generate a business based on this Task

        :returns: A new business instance
        :rtype: :class:`autonomie.models.project.business.Business`
        """
        business = Task.gen_business(self)
        business.populate_deadlines(self)
        return business

    def duplicate(self, user, **kw):
        """
        DUplicate the current Estimation object

        Mandatory args :

            user

                The user duplicating this estimation

            customer

            project
        """
        estimation = Estimation(
            user=user,
            company=self.company,
            **kw
        )

        if estimation.customer.id == self.customer_id:
            estimation.address = self.address

        estimation.workplace = self.workplace

        estimation.description = self.description

        estimation.deposit = self.deposit
        estimation.payment_conditions = self.payment_conditions
        estimation.exclusions = self.exclusions
        estimation.manualDeliverables = self.manualDeliverables
        estimation.display_units = self.display_units
        estimation.expenses_ht = self.expenses_ht
        estimation.paymentDisplay = self.paymentDisplay
        estimation.line_groups = []
        for group in self.line_groups:
            estimation.line_groups.append(group.duplicate())
        for line in self.payment_lines:
            estimation.payment_lines.append(line.duplicate())
        for line in self.discounts:
            estimation.discounts.append(line.duplicate())
        estimation.mentions = self.mentions
        return estimation

    def __repr__(self):
        return u"<Estimation id:{s.id} ({s.status}>".format(s=self)

    def __json__(self, request):
        if self.manualDeliverables == 1:
            payment_times = -1
        else:
            payment_times = len(self.payment_lines)

        result = Task.__json__(self, request)
        result.update(
            dict(
                deposit=self.deposit,
                exclusions=self.exclusions,
                manual_deliverables=self.manualDeliverables,
                manualDeliverables=self.manualDeliverables,
                paymentDisplay=self.paymentDisplay,
                payment_times=payment_times,
                payment_lines=[
                    line.__json__(request)
                    for line in self.payment_lines
                ]
            )
        )
        return result

    def gen_deposit_invoice(self, user):
        """
        Generate a deposit invoice based on the current estimation

        :param obj user: User instance, the user generating the document
        :rtype: `class:Invoice`
        """
        return self._invoicing_service.gen_deposit_invoice(self, user)

    def gen_invoice(self, payment_line, user):
        """
        Generate an invoice based on a payment line

        :param obj payment_line: The payment line we ask an Invoice for
        :param obj user: User instance, the user generating the document
        :rtype: `class:Invoice`
        """
        if payment_line == self.payment_lines[-1]:
            self.geninv = True
            DBSESSION().merge(self)
            return self._invoicing_service.gen_sold_invoice(self, user)
        else:
            return self._invoicing_service.gen_intermediate_invoice(
                self, payment_line, user
            )


class PaymentLine(DBBASE):
    """
        payments lines
    """
    __tablename__ = 'estimation_payment'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
    )
    task_id = Column(
        Integer,
        ForeignKey('estimation.id', ondelete="cascade"),
        info={
            'colanderalchemy': {
                'title': u"Identifiant du document",
            }
        },
    )
    order = Column(
        Integer,
        info={'colanderalchemy': {'title': u"Ordre"}},
        default=1
    )
    description = Column(
        Text,
        info={'colanderalchemy': {'title': u"Description"}},
    )
    amount = Column(
        BigInteger(),
        info={'colanderalchemy': {'title': u"Montant"}},
    )
    date = Column(
        Date(),
        info={'colanderalchemy': {"title": u"Date"}},
        default=datetime.date.today
    )
    task = relationship(
        "Estimation",
        info={'colanderalchemy': {'exclude': True}},
    )

    def duplicate(self):
        """
            duplicate a paymentline
        """
        return PaymentLine(
            order=self.order,
            amount=self.amount,
            description=self.description,
            date=datetime.date.today(),
        )

    def __repr__(self):
        return u"<PaymentLine id:{s.id} task_id:{s.task_id} amount:{s.amount}\
 date:{s.date}".format(s=self)

    def __json__(self, request):
        return dict(
            id=self.id,
            order=self.order,
            index=self.order,
            description=self.description,
            cost=integer_to_amount(self.amount, 5),
            amount=integer_to_amount(self.amount, 5),
            date=self.date.isoformat(),
            task_id=self.task_id,
        )
