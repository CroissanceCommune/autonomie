# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Boolean,
    String,
)
from sqlalchemy.orm import (
    relationship,
)
from autonomie_base.models.base import (
    default_table_args,
    DBBASE,
)
from autonomie.models.node import Node
from autonomie.models.services.sale_file_requirements import (
    BusinessFileRequirementService,
)
from autonomie.models.services.business import BusinessService
from autonomie.models.services.business_status import (
    BusinessStatusService,
)


class BusinessPaymentDeadline(DBBASE):
    __tablename__ = 'business_payment_deadline'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True)
    deposit = Column(Boolean(), default=False)
    business_id = Column(Integer, ForeignKey('business.id'))
    estimation_payment_id = Column(Integer, ForeignKey('estimation_payment.id'))
    estimation_id = Column(Integer, ForeignKey('estimation.id'))
    invoiced = Column(Boolean(), default=False)
    invoice_id = Column(Integer, ForeignKey('invoice.id'))
    payment_line = relationship("PaymentLine")
    estimation = relationship("Estimation")
    invoice = relationship('Invoice')


class Business(Node):
    """
    Permet de :

        * Collecter les fichiers

        * Regrouper devis/factures/avoirs

        * Calculer le CA d'une affaire

        * Générer les factures

        * Récupérer le HT à dépenser

        * Des choses plus complexes en fonction du type de business

    Business.estimations
    Business.invoices
    Business.invoices[0].cancelinvoices
    """
    __tablename__ = "business"
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': "business"}
    file_requirement_service = BusinessFileRequirementService
    status_service = BusinessStatusService
    _autonomie_service = BusinessService

    id = Column(
        Integer,
        ForeignKey('node.id'),
        primary_key=True,
        info={'colanderalchemy': {'exclude': True}},
    )
    closed = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': u"Cette affaire est-elle terminée ?"
            }
        },
    )
    status = Column(
        String(8),
        default="danger",
        info={
            'colanderalchemy': {"title": u"Statut de cette affaire"}
        }
    )

    business_type_id = Column(
        ForeignKey('business_type.id'),
        info={'colanderalchemy': {'title': u"Type d'affaires"}}
    )
    project_id = Column(
        ForeignKey('project.id'),
        info={'colanderalchemy': {'exclude': True}},
    )

    # Relations
    business_type = relationship(
        "BusinessType",
    )
    project = relationship(
        "Project",
        primaryjoin="Project.id == Business.project_id",
    )
    tasks = relationship(
        "Task",
        primaryjoin="Task.business_id==Business.id",
        back_populates="business"
    )
    estimations = relationship(
        "Task",
        back_populates="business",
        primaryjoin="and_(Task.business_id==Business.id, "
        "Task.type_=='estimation')",
    )
    invoices = relationship(
        "Task",
        back_populates="business",
        primaryjoin="and_(Task.business_id==Business.id, "
        "Task.type_.in_(('invoice', 'cancelinvoice')))"
    )
    payment_deadlines = relationship(
        "BusinessPaymentDeadline",
        primaryjoin="BusinessPaymentDeadline.business_id==Business.id",
        cascade="all, delete-orphan",
    )
    indicators = relationship(
        "CustomBusinessIndicator",
        primaryjoin="CustomBusinessIndicator.business_id==Business.id",
    )

    @property
    def payment_lines(self):
        """
        Collect payment lines that are referenced by a deadline
        """
        return [deadline.payment_line
                for deadline in self.payment_deadlines
                if deadline.payment_line is not None]

    @property
    def invoiced(self):
        indicator = self.status_service.get_or_create_invoice_indicator(self)
        return indicator.status == indicator.SUCCESS_STATUS

    def get_company_id(self):
        return self.project.company_id

    def amount_to_invoice(self):
        """
        Compute the amount to invoice in this business
        :returns: The amount in the *10^5 precision
        :rtype: int
        """
        return self._autonomie_service.to_invoice(self)

    def populate_indicators(self):
        """
        Populate custom business indicators

        :returns: The business we manage
        """
        return self.status_service.populate_indicators(self)

    def populate_deadlines(self, estimation=None):
        """
        Populate the current business with its associated payment deadlines
        regarding the estimations belonging to this business

        :param obj estimation: An optionnal Estimation instance
        :returns: This instance
        """
        return self._autonomie_service.populate_deadlines(
            self, estimation
        )

    def find_deadline(self, deadline_id):
        """
        Find the deadline matching this id

        :param int deadline_id: The deadline id
        :returns: A Payment instance
        """
        return self._autonomie_service.find_deadline(self, deadline_id)

    def gen_invoices(self, user, payment_deadlines=None):
        """
        Generate invoices for the given list of payment_deadlines (or all if not
        provided)

        :param obj business: The Business in which we work
        :param obj user: The current connected user
        :param list payment_deadlines: Optionnal the deadlines for which we
        generate invoices else all deadlines
        :returns: A list of invoices
        """
        return self._autonomie_service.gen_invoices(
            self, user, payment_deadlines
        )

    def find_deadline_from_invoice(self, invoice):
        """
        Find the deadline associated to the current business and the given
        invoice

        :param obj invoice: The Invoice we're working on
        :returns: A BusinessPaymentDeadline instance
        """
        return self._autonomie_service.find_deadline_from_invoice(
            self, invoice
        )
