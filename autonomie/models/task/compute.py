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
    # HT TOTAL total of lines ht
    # TVA TOTAL BY TVA
    #
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
        print "Total HT : %s" % int(self.lines_total_ht() - self.discount_total_ht())
        return int(self.lines_total_ht() - self.discount_total_ht())

    def get_tvas(self):
        """
            return a dict with the tvas amounts stored by tva
            {1960:450.56, 700:45}
        """
        ret_dict = {}
        for line in self.lines:
            print "line: %s, %s " % (line.total_ht(), line.tva_amount())
            val = ret_dict.get(line.tva, 0)
            val += line.tva_amount()
            print "Val : %s" % val
            ret_dict[line.tva] = val
        for discount in self.discounts:
            print "discount: %s %s" %(discount.amount, discount.tva_amount())
            val = ret_dict.get(line.tva, 0)
            val -= discount.tva_amount()
            print "Val : %s" % val
            ret_dict[line.tva] = val
        print "TVA dict : %s" % ret_dict
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
        if hasattr(self, "payments"):
            return sum([payment.get_amount() for payment in self.payments])
        else:
            return 0

    def topay(self):
        """
            return the amount to pay
        """
        return self.total() - self.paid()
