# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 03-09-2012
# * Last Modified :
#
# * Project :
#
"""
    Task computing tool
    Used to compute invoice, estimation or cancelinvoice totals
"""


class TaskCompute(object):
    """
        class A(TaskCompute):
            pass

        A.total()
        expects some attributes to be filled
        lines
        payments
        discountHT
        expenses
        tva
    """
    # Should have a total_ht and a tva method
    lines = []
    # Should have a total_ht and a tva method
    discounts = []
    # Should have an amount attribute
    payments = []
    expenses = None

    def lines_total_ht(self):
        """
            compute the sum of the task lines total
        """
        return sum(line.total_ht() for line in self.lines)

    def discount_total_ht(self):
        """
            compute the discount total
        """
        return sum(line.total_ht() for line in self.discounts)

    def total_ht(self):
        """
            compute the HT amount
        """
        return int(self.lines_total_ht() - self.discount_total_ht())

    def get_tvas(self):
        """
            return a dict with the tvas amounts stored by tva
            {1960:450.56, 700:45}
        """
        ret_dict = {}
        for line in self.lines:
            val = ret_dict.get(line.tva, 0)
            val += line.tva_amount()
            ret_dict[line.tva] = val
        for discount in self.discounts:
            val = ret_dict.get(discount.tva, 0)
            val -= discount.tva_amount()
            ret_dict[discount.tva] = val
        return ret_dict

    def tva_amount(self):
        """
            Compute the sum of the TVAs amount of TVA
        """
        return int(sum(tva for tva in self.get_tvas().values()))

    def total_ttc(self):
        """
            Compute the TTC total
        """
        return self.total_ht() + self.tva_amount()

    def total(self):
        """
            Compute TTC after tax removing
        """
        return self.total_ttc() + self.expenses_amount()

    def expenses_amount(self):
        """
            return the amount of the expenses
        """
        result = int(self.expenses)
        return result

    def paid(self):
        """
            return the amount that has already been paid
        """
        if self.payments:
            return sum([payment.amount for payment in self.payments])
        else:
            return 0

    def topay(self):
        """
            return the amount to pay
        """
        return self.total() - self.paid()

    def no_tva(self):
        """
            return True if all the tvas are below 0
        """
        ret = True
        for key in self.get_tvas():
            if key >= 0:
                ret = False
        return ret

class EstimationCompute(TaskCompute):
    """
        Computing class for estimations
        Adds the ability to compute deposit amounts ...
    """
    deposit = None
    manualDeliverables = None
    payment_lines = None


    # Computing
    def deposit_amount(self):
        """
            Compute the amount of the deposit
        """
        if self.deposit > 0:
            total = self.total_ht()
            return int(total * int(self.deposit) / 100.0)
        return 0

    def get_nb_payment_lines(self):
        """
            Returns the number of payment lines configured
        """
        return len(self.payment_lines)

    def paymentline_amount(self):
        """
            Compute payment lines amounts in case of equal payment repartition
            (when manualDeliverables is 0)
            (when the user has selected 3 time-payment)
        """
        total = self.total_ht()
        deposit = self.deposit_amount()
        rest = total - deposit
        return int(rest / self.get_nb_payment_lines())

    # Computations for estimation display
    def deposit_amount_ttc(self):
        """
            Return the ttc amount of the deposit (for estimation display)
        """
        if self.deposit > 0:
            total_ttc = self.total_ttc()
            return int(total_ttc * int(self.deposit) / 100.0)
        return 0

    def sold(self):
        """
            Compute the sold amount to finish on an exact value
            if we divide 10 in 3, we'd like to have something like :
                3.33 3.33 3.34
            (for estimation display)
        """
        result = 0
        total_ttc = self.total()
        deposit_ttc = self.deposit_amount_ttc()
        rest = total_ttc - deposit_ttc

        payment_lines_num = self.get_nb_payment_lines()
        if payment_lines_num == 1 or not self.get_nb_payment_lines():
            # No other payment line
            result = rest
        else:
            if self.manualDeliverables == 0:
                # Amounts has to be divided
                line_amount = self.paymentline_amount()
                result = rest - ((payment_lines_num - 1) * line_amount)
            else:
                # Ici la donnée est fausse (on va rajouter de la tva sur les
                # montants des lignes de paiement configurées manuellement
                # Donc le solde caluclé ici est faux
                result = rest - sum(line.amount
                                    for line in self.payment_lines[:-1])
        return result

class LineCompute(object):
    """
        Computing tool for line objects
    """
    cost = None
    tva = None
    quantity = 1

    def total_ht(self):
        """
            Compute the line's total
        """
        return float(self.cost) * float(self.quantity)

    def tva_amount(self):
        """
            compute the tva amount of a line
        """
        totalht = self.total_ht()
        result = float(totalht) * (max(int(self.tva), 0) / 10000.0)
        return result

    def total(self):
        """
            Compute the ttc amount of the line
        """
        return self.tva_amount() + self.total_ht()
