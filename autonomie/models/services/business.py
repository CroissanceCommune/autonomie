# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
from autonomie_base.models.base import DBSESSION


logger = logging.getLogger(__name__)


class BusinessService:
    """
    Service class provding common Business related tools
    """
    @classmethod
    def to_invoice(cls, business):
        """
        Compute the amount that is supposed to be invoiced regarding the
        estimation and the existing invoices

        :param obj business: The business instance
        :returns: The amount to be invoiced (in *10^5 format)
        ;rtype: int
        """
        to_invoice = sum([estimation.ht for estimation in business.estimations])
        invoiced = sum([invoice.ht for invoice in business.invoices])
        return max(to_invoice - invoiced, 0)

    @classmethod
    def _add_payment_deadline(cls, business, payment_line, estimation):
        """
        Add a payment deadline for the given payment line to the business
        deadlines
        """
        from autonomie.models.project.business import BusinessPaymentDeadline
        if payment_line not in business.payment_lines:
            business.payment_deadlines.append(
                BusinessPaymentDeadline(
                    payment_line=payment_line, estimation=estimation
                )
            )

    @classmethod
    def _add_deposit_deadline(cls, business, estimation):
        """
        Add a deposit deadline to a business
        """
        deposit = estimation.deposit
        if not deposit:
            return business
        from autonomie.models.project.business import BusinessPaymentDeadline
        query = BusinessPaymentDeadline.query()
        query = query.filter_by(business_id=business.id)
        query = query.filter_by(estimation_id=estimation.id)
        query = query.filter_by(deposit=True)
        if query.count() == 0:
            business.payment_deadlines.append(
                BusinessPaymentDeadline(
                    business_id=business.id,
                    estimation_id=estimation.id,
                    deposit=True,
                )
            )
            DBSESSION().merge(business)
        return business

    @classmethod
    def populate_deadlines(cls, business, estimation=None):
        """
        Populate the business deadlines with those described in the associated
        estimation(s)

        :param obj business: The Business instance
        :param obj estimation: Optionnal Estimation instance
        :returns: The Business instance
        :rtype: obj
        """
        logger.debug(
            u"Populating deadlines for the business {}".format(business.id)
        )
        if estimation is not None:
            estimations = [estimation]
        else:
            estimations = business.estimations
        for estimation in estimations:
            cls._add_deposit_deadline(business, estimation)
            for payment_line in estimation.payment_lines:
                cls._add_payment_deadline(business, payment_line, estimation)

        return DBSESSION().merge(business)

    @classmethod
    def find_deadline(cls, business, deadline_id):
        """
        Find the deadline matching this id

        :param obj business: The parent Business
        :param int deadline_id: The associated deadline_id
        """
        from autonomie.models.project.business import BusinessPaymentDeadline
        result = BusinessPaymentDeadline.get(deadline_id)
        if result.business_id != business.id:
            result = None
        return result

    @classmethod
    def find_deadline_from_invoice(cls, business, invoice):
        """
        Find the deadline having this invoice attached to it

        :param obj business: The parent Business
        :param obj invoice: The associated Invoice
        """
        from autonomie.models.project.business import BusinessPaymentDeadline
        result = BusinessPaymentDeadline.query().filter_by(
            invoice_id=invoice.id
        ).filter_by(
            business_id=business.id
        ).first()
        return result

    @classmethod
    def gen_invoices(cls, business, user, payment_deadlines=None):
        """
        Generate the invoices associated to the given payment deadlines

        :param obj business: The Business in which we work
        :param obj user: The current connected user
        :param list payment_deadlines: Optionnal the deadlines for which we
        generate invoices else all deadlines
        :returns: A list of invoices
        """
        if not payment_deadlines:
            payment_deadlines = business.payment_deadlines
        elif not hasattr(payment_deadlines, '__iter__'):
            payment_deadlines = [payment_deadlines]

        invoices = []
        for deadline in payment_deadlines:
            estimation = deadline.estimation
            if deadline.deposit:
                invoice = estimation.gen_deposit_invoice(
                    user,
                )
            else:
                invoice = estimation.gen_invoice(
                    deadline.payment_line,
                    user,
                )
            invoice.initialize_business_datas(business)
            DBSESSION().add(invoice)
            DBSESSION().flush()
            deadline.invoice_id = invoice.id
            DBSESSION().merge(deadline)
            invoices.append(invoice)
        return invoices
