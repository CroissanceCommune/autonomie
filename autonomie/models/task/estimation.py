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
    Table,
)
from sqlalchemy.orm import (
    relationship,
    deferred,
)
from sqlalchemy.ext.orderinglist import ordering_list
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie.compute.task import (
    EstimationCompute,
)
from autonomie.compute.math_utils import integer_to_amount
from autonomie.models.tva import Product
from .interfaces import (
    IMoneyTask,
)
from autonomie.models.config import Config
from .invoice import (
    Invoice,
)
from autonomie.models.project.business import Business
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

logger = log = logging.getLogger(__name__)


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


EstimationBusiness = Table(
    "estimation_business",
    DBBASE.metadata,
    Column("estimation.id", Integer, ForeignKey('estimation.id')),
    Column("business.id", Integer, ForeignKey('business.id')),
    mysql_charset=default_table_args['mysql_charset'],
    mysql_engine=default_table_args['mysql_engine']
)


@implementer(IMoneyTask)
class Estimation(Task, EstimationCompute):
    """
        Estimation Model
    """
    __tablename__ = 'estimation'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'estimation', }
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
    course = deferred(
        Column(
            Integer,
            nullable=False,
            info={
                'colanderalchemy': {'title': u"Concerne une formation ?"}
            },
            default=0
        ),
        group='edit'
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
    businesses = relationship(
        "Business",
        secondary=EstimationBusiness,
        order_by="Business.created_at",
        back_populates="estimations",
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
        estimation.course = self.course
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

    def _account_invoiceline(self, amount, description, tva=1960):
        """
            Return an account invoiceline
        """
        line = TaskLine(cost=amount, description=description, tva=tva)
        line.product_id = Product.first_by_tva_value(tva)
        return line

    def _make_deposit(self, invoice):
        """
            Return a deposit invoice
        """
        invoice.financial_year = invoice.date.year
        invoice.display_units = 0

        for tva, amount in self.deposit_amounts().items():
            description = u"Facture d'acompte"
            line = self._account_invoiceline(amount, description, tva)
            invoice.default_line_group.lines.append(line)
        return invoice, [l.duplicate()
                         for l in invoice.default_line_group.lines]

    def _make_intermediary(self, invoice, paymentline, amounts):
        """
            return an intermediary invoice described by "paymentline"
        """
        invoice.date = paymentline.date
        invoice.financial_year = paymentline.date.year
        invoice.display_units = 0
        for tva, amount in amounts.items():
            description = paymentline.description
            line = self._account_invoiceline(amount, description, tva)
            invoice.default_line_group.lines.append(line)
        return invoice, [l.duplicate()
                         for l in invoice.default_line_group.lines]

    def _sold_invoice_lines(self, account_lines):
        """
            return the lines that will appear in the sold invoice
        """
        sold_groups = []
        for group in self.line_groups:
            sold_groups.append(group.duplicate())

        if len(self.line_groups) > 1:
            current_group = TaskLineGroup()
            sold_groups.append(current_group)
        else:
            current_group = sold_groups[0]

        account_lines.reverse()

        order = len(current_group.lines)
        for line in account_lines:
            order = order + 1
            line.cost = -1 * line.cost
            line.order = order
            # On ajoute les lignes au groupe créé par défaut
            current_group.lines.append(line)

        return sold_groups

    def _make_sold(self, invoice, paymentline, paid_lines):
        """
            Return the sold invoice
        """
        invoice.date = paymentline.date
        invoice.financial_year = paymentline.date.year

        invoice.display_units = self.display_units
        invoice.expenses_ht = self.expenses_ht
        # On supprimer le default_task_line group car insère ceux du devis
        invoice.line_groups = []
        for group in self._sold_invoice_lines(paid_lines):
            invoice.line_groups.append(group)
        for line in self.discounts:
            invoice.discounts.append(line.duplicate())
        return invoice

    def _get_common_invoice(self, user):
        """
            Return an invoice object with common args for
            all the generated invoices
        """
        inv = Invoice(
            company=self.company,
            customer=self.customer,
            project=self.project,
            user=user,
            phase_id=self.phase_id,
            estimation=self,
            payment_conditions=self.payment_conditions,
            description=self.description,
            course=self.course,
            address=self.address,
            workplace=self.workplace,
            mentions=self.mentions,
            prefix=Config.get_value('invoice_prefix', ''),
            business_type_id=self.business_type_id,
        )
        return inv

    def gen_invoices(self, user):
        """
        Generate invoices based on the current estimation and its payments
        configuration

        :returns: The list of Invoice instances
        :rtype: list
        """
        invoices = []
        # Used to store the amount of the intermediary invoices
        paid_lines = []

        current_project_index = None
        current_company_index = None

        # Sequence number that will be incremented by hand
        if self.deposit > 0:
            invoice = self._get_common_invoice(user)
            deposit, lines = self._make_deposit(invoice)
            invoices.append(deposit)
            # We remember the lines to display them in the last invoice
            paid_lines.extend(lines)

            current_project_index = invoice.project_index
            current_company_index = invoice.company_index

            # We need to update the invoice name
            invoice.set_deposit_label()

        if self.manualDeliverables == 1:
            payments = self.manual_payment_line_amounts()

            # all payment lines specified (less the last one)
            for index, amounts in enumerate(payments[:-1]):
                invoice = self._get_common_invoice(user)
                line = self.payment_lines[index]
                invoice, lines = self._make_intermediary(
                    invoice,
                    line,
                    amounts,
                )
                if current_project_index is None:
                    # Label and numbers remains unchanged, no need to update
                    # numbers
                    current_project_index = invoice.project_index
                    current_company_index = invoice.company_index
                else:
                    current_project_index += 1
                    current_company_index += 1
                    invoice.set_numbers(
                        current_company_index,
                        current_project_index,
                    )

                paid_lines.extend(lines)
                invoices.append(invoice)
        else:
            amounts = self.paymentline_amounts()

            # All amounts are equal
            for line in self.payment_lines[:-1]:
                invoice = self._get_common_invoice(user)

                invoice, lines = self._make_intermediary(
                    invoice,
                    line,
                    amounts,
                )
                if current_project_index is None:
                    # Label and numbers remains unchanged, no need to update
                    # numbers
                    current_project_index = invoice.project_index
                    current_company_index = invoice.company_index
                else:
                    current_project_index += 1
                    current_company_index += 1
                    invoice.set_numbers(
                        current_company_index,
                        current_project_index,
                    )
                paid_lines.extend(lines)
                invoices.append(invoice)

        invoice = self._get_common_invoice(user)
        pline = self.payment_lines[-1]
        invoice = self._make_sold(
            invoice,
            pline,
            paid_lines,
        )

        if current_project_index is not None:
            # here we already have some invoices set
            current_project_index += 1
            current_company_index += 1
            invoice.set_numbers(current_company_index, current_project_index)
            invoice.set_sold_label()

        invoices.append(invoice)
        return invoices

    def gen_business(self):
        """
        Generate a business based on this estimation

        :returns: A new business instance
        :rtype: :class:`autonomie.models.poroject.business.Business`
        """
        business = Business(
            name=self.name,
            project_id=self.project_id,
            business_type_id=self.business_type_id,
        )
        return business

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
                course=self.course,
                paymentDisplay=self.paymentDisplay,
                payment_times=payment_times,
                payment_lines=[
                    line.__json__(request)
                    for line in self.payment_lines
                ]
            )
        )
        return result


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
