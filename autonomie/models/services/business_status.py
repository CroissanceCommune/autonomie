# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
from autonomie_base.models.base import DBSESSION


logger = logging.getLogger(__name__)


class BusinessStatusService:
    """
    Service class providing Business status management tools
    """

    @classmethod
    def populate_indicators(cls, business):
        """
        Generate base indicators for a given business

        :param obj business: The Business instance
        :returns: The Business instance
        :rtype: obj
        """
        cls.get_or_create_invoice_indicator(business)
        return business

    @classmethod
    def get_or_create_invoice_indicator(cls, business):
        from autonomie.models.indicators import CustomBusinessIndicator
        indicator = CustomBusinessIndicator.query().filter_by(
            business_id=business.id
        ).filter_by(
            name="invoiced"
        ).first()

        if indicator is None:
            indicator = CustomBusinessIndicator(
                name="invoiced",
                label=u"Facturation",
            )
            DBSESSION().add(indicator)
            DBSESSION().flush()
            business.indicators.append(indicator)
            DBSESSION().merge(business)
        return indicator

    @classmethod
    def update_invoicing_indicator(cls, business):
        """
        Update the invoicing status indicator of the given business

        :param obj business: The Business instance
        :returns: The Business instance
        :rtype: obj
        """
        invoicing_status = True
        for deadline in business.payment_deadlines:
            if not deadline.invoiced:
                invoicing_status = False
                break

        indicator = None
        if invoicing_status is True:
            indicator = cls.get_or_create_invoice_indicator(business)
            indicator.status = indicator.SUCCESS_STATUS
            DBSESSION().merge(indicator)

        return indicator

    @classmethod
    def update_invoicing_status(cls, business, invoice=None):
        """
        Update the invoicing status of the deadline associated to this invoice

        :param obj business: The Business instance
        :param obj invoice: The validated Invoice instance
        :returns: The Business instance
        :rtype: obj
        """
        if invoice:
            deadline = business.find_deadline_from_invoice(invoice)
            if deadline is not None:
                deadline.invoiced = True
                DBSESSION().merge(deadline)
        cls.update_invoicing_indicator(business)

    @classmethod
    def _compute_status(cls, business):
        """
        Get the actual status of a business collecting datas from its indicators

        :param obj business: The Business instance
        :returns: The new status
        :rtype: str
        """
        result = 'success'
        for requirement in business.file_requirements:
            result = requirement.cmp_status(result)

        for indicator in business.indicators:
            result = indicator.cmp_status(result)

        return result

    @classmethod
    def update_status(cls, business):
        """
        Update the business status if needed

        :param obj business: The Business instance
        :returns: The Business instance
        :rtype: obj
        """
        status = cls._compute_status(business)
        if status != business.status:
            business.status = status
            DBSESSION().merge(business)
        return business
