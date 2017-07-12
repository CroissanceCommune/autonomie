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
import deform
import colander

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
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie import forms
from autonomie.forms.custom_types import AmountType
from autonomie.compute.task import (
    EstimationCompute,
)
from autonomie.compute.math_utils import integer_to_amount
from .interfaces import (
    IMoneyTask,
)
from .invoice import (
    Invoice,
)
from .task import (
    Task,
    DiscountLine,
    TaskLine,
    TaskStatus,
)
from .actions import (
    DEFAULT_ACTION_MANAGER,
    SIGNED_ACTION_MANAGER,
)

log = logging.getLogger(__name__)


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
    id = Column(
        ForeignKey('task.id'),
        primary_key=True,
        info={
            'colanderalchemy': {
                "exclude": True,
                'widget': deform.widget.HiddenWidget(),
                "missing": colander.drop,
            }
        },
    )
    signed_status = Column(
        String(10),
        default='waiting',
        info={
            'colanderalchemy': {
                'widget': deform.widget.SelectWidget(values=ESTIMATION_STATES),
                'title': u'Statut du devis',
                "validator": colander.OneOf([i[0] for i in ESTIMATION_STATES])
            }
        }
    )
    geninv = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                "title": u"Factures générées ?",
            }
        }
    )

    # common with only invoices
    deposit = Column(
        Integer,
        info={
            'colanderalchemy': {
                'title': u'Accompte (en %)',
                "validator": colander.Range(
                    0,
                    100,
                    min_err=u"Ce nombre n'est pas compris en 0 et 100",
                    max_err=u"Ce nombre n'est pas compris en 0 et 100",
                )
            }
        },
        default=0
    )
    course = deferred(
        Column(
            Integer,
            nullable=False,
            info={
                'colanderalchemy': {
                    'title': u"Concerne une formation ?"
                }
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
            info={'colanderalchemy': {'exclude': True}}
        ),
        group='edit'
    )
    paymentDisplay = deferred(
        Column(
            String(20),
            info={
                'colanderalchemy': {
                    'title': u"Affichage des paiements",
                    'widget': deform.widget.SelectWidget(
                        values=PAYMENTDISPLAYCHOICES),
                    'validator': colander.OneOf(
                        [i[0] for i in PAYMENTDISPLAYCHOICES]
                    )
                }
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
        info={
            'colanderalchemy': {
                'title': u"Échéances de paiement",
                "validator": colander.Length(
                    min=1,
                    min_err="Au moins un paiement est requis"
                ),
                "missing": colander.required,
            },
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

    def duplicate(self, user, project, phase, customer):
        """
            returns a duplicate estimation object
        """
        estimation = Estimation(
            self.company,
            customer,
            project,
            phase,
            user,
        )

        if customer.id == self.customer_id:
            estimation.address = self.address
        else:
            estimation.address = customer.full_address

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
        return TaskLine(cost=amount, description=description, tva=tva)

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
        order = len(self.line_groups)
        for line in account_lines:
            order = order + 1
            line.cost = -1 * line.cost
            line.order = order
            # On ajoute les lignes au groupe créé par défaut
            sold_groups[0].lines.append(line)
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
            self.company,
            self.customer,
            self.project,
            self.phase,
            user
        )
        inv.estimation = self

        # Common args
        inv.payment_conditions = self.payment_conditions
        inv.description = self.description
        inv.course = self.course
        inv.address = self.address
        inv.workplace = self.workplace
        inv.mentions = self.mentions
        return inv

    def gen_invoices(self, user):
        """
            Return the invoices based on the current estimation
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

    def add_line(self, line=None, **kwargs):
        """
            Add a line to the current task
        """
        if line is None:
            line = TaskLine(**kwargs)
        self.default_line_group.lines.append(line)

    def add_discount(self, line=None, **kwargs):
        """
            Add a discount line to the current task
        """
        if line is None:
            line = DiscountLine(**kwargs)
        self.discounts.append(line)

    def add_payment(self, line=None, **kwargs):
        """
            Add a payment line to the current task
        """
        if line is None:
            line = PaymentLine(**kwargs)
        self.payments.append(line)

    def set_lines(self, lines):
        """
            Set the lines
        """
        self.default_line_group.lines = lines

    def set_discounts(self, lines):
        """
            Set the discounts
        """
        self.discounts = lines

    def set_payments(self, lines):
        """
            set the payment lines
        """
        self.payments = lines

    def __repr__(self):
        return u"<Estimation id:{s.id} ({s.status}>".format(s=self)

    def __json__(self, request):
        result = Task.__json__(self, request)
        result.update(
            dict(
                deposit=self.deposit,
                exclusions=self.exclusions,
                manual_deliverables=self.manualDeliverables,
                manualDeliverables=self.manualDeliverables,
                course=self.course,
                paymentDisplay=self.paymentDisplay,
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
        info={'colanderalchemy': {'widget': deform.widget.HiddenWidget()}}
    )
    task_id = Column(
        Integer,
        ForeignKey('estimation.id', ondelete="cascade"),
        info={
            'colanderalchemy': {
                'title': u"Identifiant du document",
                'missing': colander.required,
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
        info={
            'colanderalchemy': {
                'title': u"Description",
                'validator': forms.textarea_node_validator,
            }
        },
    )
    amount = Column(
        BigInteger(),
        info={
            'colanderalchemy': {
                'title': u"Montant",
                'typ': AmountType(5),
                'missing': colander.required,
            }
        },
    )
    date = Column(
        Date(),
        info={
            'colanderalchemy': {
                "title": u"Date",
            }
        },
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
            order=self.order,
            index=self.order,
            description=self.description,
            cost=integer_to_amount(self.amount, 5),
            amount=integer_to_amount(self.amount, 5),
            date=self.date.isoformat(),
            task_id=self.task_id,
        )
