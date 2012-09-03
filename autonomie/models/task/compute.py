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
    # Computing functions
    def lines_total(self):
        """
            compute the sum of the task lines total
        """
        return sum(line.total() for line in self.lines)

    def total_ht(self):
        """
            compute the HT amount
        """
        return self.lines_total() - self.discount_amount()

    def discount_amount(self):
        """
            Compute the amount of the discount
        """
        if hasattr(self, "discountHT"):
            return int(self.discountHT)
        else:
            return 0

    def tva_amount(self, totalht=None):
        """
            Compute the amount of TVA
        """
        if not totalht:
            totalht = self.total_ht()
        result = int(float(totalht) * (max(int(self.tva), 0) / 10000.0))
        return result

    def total_ttc(self):
        """
            Compute the TTC total
        """
        totalht = self.total_ht()
        tva_amount = self.tva_amount(totalht)
        return int(totalht + tva_amount)

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
        if hasattr(self, "payments"):
            return sum([payment.get_amount() for payment in self.payments])
        else:
            return 0

    def topay(self):
        """
            return the amount to pay
        """
        return self.total() - self.paid()

