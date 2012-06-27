# -*- coding: utf-8 -*-
# * File Name : task.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 27-06-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    computers for task handling
"""

class TaskComputing:
    """
        The task computing model is a handly class
        overlaying the database model for estimation or invoices
        it provides access to the model and computation of the main amounts
        we'd like to be computed

        NOTE ON COMPUTING

        Since the datas stored in the database are stored in *100 format
        We are now working with integers only
        TVA is stored as an integer too (needs to be divided by 100*100
        Database returns Decimal, so we convert all database retrieved amounts
        in integers (except the quantity one which is not stored in *100 format)

        Payment lines:
            the payment lines are:
                manually configured
                or
                splitted in equal parts
            in each case, the sold should be computed aside to ensure the total
            amount is reached (if not,we may make mistakes by rounding)

    """

    def __init__(self, model):
        self.model = model

    @staticmethod
    def compute_line_total(line):
        """
            compute estimation/invoice line total
        """
        cost = line.cost
        quantity = line.quantity
        return float(cost) * float(quantity)

    def compute_lines_total(self):
        """
            compute the estimation/invoices line total
        """
        return sum(self.compute_line_total(line) for line in self.model.lines)

    def compute_totalht(self):
        """
            compute the ht total
        """
        return self.compute_lines_total() - int(self.model.discountHT)

    def compute_tva(self, totalht=None):
        """
            compute the tva amount
        """
        if not totalht:
            totalht = self.compute_totalht()
        return int(float(totalht) * (max(int(self.model.tva), 0) / 10000.0))

    def compute_ttc(self):
        """
            compute the ttc value before expenses
        """
        totalht = self.compute_totalht()
        tva_amount = self.compute_tva(totalht)
        return totalht + tva_amount

    def compute_total(self):
        """
            compute the total amount
        """
        return self.compute_ttc() - int(self.model.expenses)

    def compute_deposit(self):
        """
            Compute the amount of the deposit
        """
        if self.model.deposit > 0:
            total = self.compute_total()
            return int(total * int(self.model.deposit) / 100.0)
        return 0

    def get_nb_payment_lines(self):
        """
            Returns the number of payment lines configured
        """
        return len(self.model.payment_lines)

    def compute_line_amount(self):
        """
            Compute payment lines amounts in case of equal division
            (when manualDeliverables is 0)
            (when the user has checked 3 times)
        """
        total = self.compute_total()
        deposit = self.compute_deposit()
        rest = total - deposit
        return int(rest / self.get_nb_payment_lines())

    def compute_sold(self):
        """
            Compute the sold amount to finish on an exact value
            if we divide 10 in 3, we'd like to have something like :
                3.33 3.33 3.34
        """
        total = self.compute_total()
        deposit = self.compute_deposit()
        rest = total - deposit
        payment_lines_num = self.get_nb_payment_lines()
        if payment_lines_num == 1:
            return rest
        else:
            if self.model.manualDeliverables == 0:
                line_amount = self.compute_line_amount()
                return rest - ((payment_lines_num-1) * line_amount)
            else:
                return rest - sum(line.amount \
                        for line in self.model.payment_lines[:-1])

    def get_client(self):
        """
            Returns the client associated to the given task
        """
        return self.model.project.client

class ManualInvoiceComputing:
    """
        wrap manual invoices to allow computing
    """
    def __init__(self, model):
        self.model = model

    def compute_totalht(self):
        """
            Compute ht total
        """
        return int(self.model.montant_ht * 100)

    def compute_tva(self):
        """
            compute_tva
        """
        if self.model.tva:
            totalht = self.compute_totalht()
            if self.model.tva < 0 :
                return int(float(self.model.tva) * 100)
            else:
                tva = max(int(self.model.tva), 0)
                return int(float(totalht) * (tva / 10000.0))
        else:
            return 0

    def get_client(self):
        """
            returns the associated client
        """
        return self.model.client

