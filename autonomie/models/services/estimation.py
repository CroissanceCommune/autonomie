# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


class EstimationInvoicingService:
    """
    Service managing invoice generation for estimations
    """
    @classmethod
    def _get_common_invoice(cls, estimation, user):
        """
        Prepare a new Invoice related to the given estimation

        :param obj estimation: The estimation we're starting from
        :param obj user: The user generating the new document
        :returns: A new Invoice
        :rtype: `class:Invoice`
        """
        from autonomie.models.task.invoice import Invoice
        invoice = Invoice(
            user=user,
            company=estimation.company,
            customer=estimation.customer,
            project=estimation.project,
            phase_id=estimation.phase_id,
            estimation=estimation,
            payment_conditions=estimation.payment_conditions,
            description=estimation.description,
            address=estimation.address,
            workplace=estimation.workplace,
            mentions=estimation.mentions,
            business_type_id=estimation.business_type_id,
            notes=estimation.notes,
        )
        return invoice

    @classmethod
    def _get_task_line(cls, cost, description, tva):
        from autonomie.models.task.task import TaskLine
        from autonomie.models.tva import Product
        line = TaskLine(cost=cost, description=description, tva=tva, quantity=1)
        line.product_id = Product.first_by_tva_value(tva)
        return line

    @classmethod
    def _get_deposit_task_line(cls, cost, tva):
        """
            Return an deposit invoiceline
        """
        description = u"Facture d'acompte"
        return cls._get_task_line(cost, description, tva)

    @classmethod
    def _get_deposit_task_lines(cls, estimation):
        """
        Return all deposit invoiceline
        """
        lines = []
        for tva, cost in estimation.deposit_amounts().items():
            line = cls._get_deposit_task_line(cost, tva)
            lines.append(line)
        return lines

    @classmethod
    def gen_deposit_invoice(cls, estimation, user):
        """
        Generate a deposit invoice based on the given estimation

        :param obj estimation: The estimation we're starting from
        :param obj user: The user generating the new document
        :returns: A new Invoice
        :rtype: `class:Invoice`
        """
        invoice = cls._get_common_invoice(estimation, user)
        invoice.financial_year = invoice.date.year
        invoice.display_units = 0
        invoice.default_line_group.lines.extend(
            cls._get_deposit_task_lines(estimation)
        )
        return invoice

    @classmethod
    def _get_intermediate_invoiceable_amounts(cls, estimation):
        """
        Collect the amounts that should be invoiced in each intermediate payment
        deadline

        :param obj estimation: The estimation we're working on
        :returns: The amounts to be invoiced in form of a list of dict
        [{tva1: 10, tva2: 15}]
        :rtype: list
        """
        if estimation.manualDeliverables == 1:
            # On fait le calcul globale de tous les paiements et on récupère
            # celui que l'on veut
            payments = estimation.manual_payment_line_amounts()[:-1]
        else:
            divided_amount = estimation.paymentline_amounts()
            # All but not the last one (sold)
            num_payments = len(estimation.payment_lines) - 1
            payments = [divided_amount for i in range(num_payments)]
        return payments

    @classmethod
    def _get_intermediate_task_lines(cls, payment_line, payment_description):
        lines = []
        for tva, cost in payment_description.items():
            line = cls._get_task_line(cost, payment_line.description, tva)
            lines.append(line)
        return lines

    @classmethod
    def gen_intermediate_invoice(cls, estimation, payment_line, user):
        """
        Generate an intermediate invoice based on the given payment_line
        definition

        :param obj estimation: The estimation we're starting from
        :param obj payment_line: The PaymentLine describing the invoice
        :param obj user: The user generating the new document
        :returns: A new Invoice object
        :rtype: `class:Invoice`
        """
        line_index = estimation.payment_lines[:-1].index(payment_line)

        invoice = cls._get_common_invoice(estimation, user)
        if invoice.date < payment_line.date:
            invoice.date = payment_line.date
        invoice.financial_year = invoice.date.year
        invoice.display_units = 0

        payments = cls._get_intermediate_invoiceable_amounts(estimation)
        payment_description = payments[line_index]

        invoice.default_line_group.lines.extend(
            cls._get_intermediate_task_lines(
                payment_line,
                payment_description,
            )
        )
        return invoice

    @classmethod
    def _get_all_intermediate_invoiceable_task_lines(cls, estimation):
        """
        Build all intermediate invoiceable task lines including the deposit

        :param obj estimation: The estimation we're working on
        :returns: A list with all task lines
        :rtype: list of `class:TaskLine` instances
        """
        payment_descriptions = cls._get_intermediate_invoiceable_amounts(
            estimation
        )
        payments = estimation.payment_lines[:-1]

        result = []
        if estimation.deposit:
            result.extend(cls._get_deposit_task_lines(estimation))

        for payment, description in zip(payments, payment_descriptions):
            result.extend(
                cls._get_intermediate_task_lines(payment, description)
            )
        return result

    @classmethod
    def gen_sold_invoice(cls, estimation, user):
        """
        Generate a sold invoice based on the given estimation definition

        :param obj estimation: The estimation we're starting from
        :param obj user: The user generating the new document
        :returns: A new Invoice object
        :rtype: `class:Invoice`
        """
        payment_line = estimation.payment_lines[-1]
        invoice = cls._get_common_invoice(estimation, user)

        if invoice.date < payment_line.date:
            invoice.date = payment_line.date
        invoice.financial_year = invoice.date.year
        invoice.display_units = 0
        invoice.expenses_ht = estimation.expenses_ht
        line_groups = []

        for group in estimation.line_groups:
            line_groups.append(group.duplicate())

        if len(line_groups) > 1:
            from autonomie.models.task.task import TaskLineGroup
            already_invoiced_group = TaskLineGroup()
            line_groups.append(already_invoiced_group)
        else:
            already_invoiced_group = line_groups[0]

        task_lines = cls._get_all_intermediate_invoiceable_task_lines(
            estimation
        )
        task_lines.reverse()
        current_order = len(already_invoiced_group.lines)
        for line in task_lines:
            current_order += 1
            line.cost = -1 * line.cost
            line.order = current_order
            already_invoiced_group.lines.append(line)

        for discount in estimation.discounts:
            invoice.discounts.append(discount.duplicate())

        invoice.line_groups = line_groups
        return invoice
