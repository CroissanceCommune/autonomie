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
    Task computing tool
    Used to compute invoice, estimation or cancelinvoice totals
"""
import operator
import math
from autonomie.models.tva import Tva
from autonomie.compute import math_utils


def get_default_tva():
    """
        Return the default tva
    """
    try:
        default_tva = Tva.get_default()
    except:
        default_tva = None

    if default_tva:
        return default_tva.value
    else:
        return 1960


def reverse_tva(total_ttc, tva):
    """
        Compute total_ht from total_ttc
    """
    return math.ceil(float(total_ttc) * 10000.0 / (max(int(tva), 0) + 10000.0))


def compute_tva(total_ht, tva):
    """
        Compute the tva for the given ht total
    """
    return float(total_ht) * (max(int(tva), 0) / 10000.0)


class TaskCompute(object):
    """
        class A(TaskCompute):
            pass

        A.total()
    """
    # Should have a total_ht and a tva method
    lines = []
    # Should have a total_ht and a tva method
    discounts = []
    expenses = 0
    expenses_ht = 0
    expenses_tva = -1
    round_floor = False

    def floor(self, amount):
        return math_utils.floor(amount, self.round_floor)

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
        expenses_ht = self.expenses_ht or 0
        total_ht = self.lines_total_ht() - \
                self.discount_total_ht() + \
                expenses_ht
        return self.floor(total_ht)

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
        expense = self.get_expense_ht()
        tva_amount = expense.tva_amount()
        if tva_amount > 0:
            val = ret_dict.get(expense.tva, 0)
            val += expense.tva_amount()
            ret_dict[expense.tva] = val
        return ret_dict

    def tva_amount(self):
        """
            Compute the sum of the TVAs amount of TVA
        """
        return self.floor(
            sum(tva for tva in self.get_tvas().values())
        )

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
        expenses = self.expenses or 0
        result = int(expenses)
        return result

    def get_expenses_tva(self):
        """
            Return the tva for the HT expenses
        """
        if self.expenses_tva == -1:
            self.expenses_tva = get_default_tva()
        return self.expenses_tva

    def get_expense_ht(self):
        """
            Return a line object for the HT expense handling
        """
        return LineCompute(tva=self.get_expenses_tva(), cost=self.expenses_ht)

    def no_tva(self):
        """
            return True if all the tvas are below 0
        """
        ret = True
        for key in self.get_tvas():
            if key >= 0:
                ret = False
                break
        return ret


class InvoiceCompute(TaskCompute):
    """
        Invoice computing object
        Handles payments
    """
    # Should have an amount attribute
    payments = []
    cancelinvoice = None

    def payments_sum(self):
        """
        Return the amount covered by the recorded payments
        """
        return sum([payment.amount for payment in self.payments])

    def cancelinvoice_amount(self):
        """
        Return the amount covered by th associated cancelinvoice
        """
        result = 0
        if self.cancelinvoice is not None and self.cancelinvoice.is_valid():
            # cancelinvoice total is negative
            result = -1 * self.cancelinvoice.total()
        return result

    def paid(self):
        """
            return the amount that has already been paid
        """
        return self.payments_sum() + self.cancelinvoice_amount()

    def topay(self):
        """
        Return the amount that still need to be paid

        Compute the sum of the payments and what's part of a valid cancelinvoice
        """
        result = self.total() - self.paid()
        return result


class EstimationCompute(TaskCompute):
    """
        Computing class for estimations
        Adds the ability to compute deposit amounts ...
    """
    deposit = None
    manualDeliverables = None
    payment_lines = None

    def get_default_tva(self):
        """
            Silly hack to get a default tva for deposit and intermediary
            payments (configured ttc)
        """
        tvas = self.get_tvas().keys()
        return tvas[0]

    @staticmethod
    def add_ht_by_tva(ret_dict, lines, operation=operator.add):
        """
            Add ht sums by tva to ret_dict for the given lines
        """
        for line in lines:
            val = ret_dict.get(line.tva, 0)
            ht_amount = operation(val, line.total_ht())
            ret_dict[line.tva] = ht_amount
        return ret_dict

    def tva_parts(self):
        """
            Return a list of tuples
                dict(tva=(ht, tva_part,))
            for each tva value
        """
        ret_dict = {}
        ret_dict = self.add_ht_by_tva(ret_dict, self.lines)
        ret_dict = self.add_ht_by_tva(ret_dict, self.discounts, operator.sub)
        expense = self.get_expense_ht()
        ret_dict = self.add_ht_by_tva(ret_dict, [expense])
        return ret_dict

    def deposit_amounts(self):
        """
            Return the lines of the deposit for the different amount of tvas
        """
        ret_dict = {}
        for tva, total_ht in self.tva_parts().items():
            ret_dict[tva] = self.floor(total_ht * int(self.deposit) / 100.0)
        return ret_dict

    def deposit_amount(self):
        """
            Compute the amount of the deposit
        """
        import warnings
        warnings.warn("deprecated", DeprecationWarning)
        if self.deposit > 0:
            total = self.total_ht()
            return self.floor(total * int(self.deposit) / 100.0)
        return 0

    def get_nb_payment_lines(self):
        """
            Returns the number of payment lines configured
        """
        return len(self.payment_lines)

    def paymentline_amounts(self):
        """
            Compute payment lines amounts in case of equal payment repartition
            (when manualDeliverables is 0)
            (when the user has selected 3 time-payment)
        """
        ret_dict = {}
        totals = self.tva_parts()
        deposits = self.deposit_amounts()
        # num_parts set the number of equal parts
        num_parts = self.get_nb_payment_lines()
        for tva, total_ht in totals.items():
            rest = total_ht - deposits[tva]
            line_ht = rest / num_parts
            ret_dict[tva] = line_ht
        return ret_dict

    def manual_payment_line_amounts(self):
        """
            Computes the ht and tva needed to reach each payment line total

            self.payment_lines are configured with TTC amounts


            return a list of dict:
                [{tva1:ht_amount, tva2:ht_amount}]
            each dict represents a configured payment line
        """
        # Cette méthode recompose un paiement qui a été configuré TTC, sous
        # forme de part HT + TVA au regard des différentes tva configurées dans
        # le devis
        ret_data = []
        parts = self.tva_parts()
        # On enlève déjà ce qui est inclu dans l'accompte
        for tva, ht_amount in self.deposit_amounts().items():
            parts[tva] -= ht_amount

        for payment in self.payment_lines[:-1]:
            payment_ttc = payment.amount
            payment_lines = {}

            for tva, total_ht in parts.items():
                payment_ht = reverse_tva(payment_ttc, tva)
                if total_ht >= payment_ht:
                    # Le total ht de cette tranche de tva est suffisant pour
                    # recouvrir notre paiement
                    # on la récupère
                    payment_lines[tva] = payment_ht
                    # On enlève ce qu'on vient de prendre de la tranche de tva
                    # pour le calcul des autres paiements
                    parts[tva] = total_ht - payment_ht
                    ret_data.append(payment_lines)
                    break
                else:
                    # On a besoin d'une autre tranche de tva pour atteindre
                    # notre paiement, on prend déjà ce qu'il y a
                    payment_lines[tva] = parts.pop(tva)
                    # On enlève la part qu'on a récupéré dans cette tranche de
                    # tva du total de notre paiement
                    payment_ttc -= total_ht + compute_tva(total_ht, tva)

        # Ce qui reste c'est donc pour notre facture de solde
        sold = parts
        ret_data.append(sold)
        return ret_data

    # Computations for estimation display
    def deposit_amount_ttc(self):
        """
            Return the ttc amount of the deposit (for estimation display)
        """
        if self.deposit > 0:
            total_ttc = 0
            for tva, total_ht in self.deposit_amounts().items():
                line = LineCompute(cost=total_ht, tva=tva)
                total_ttc += line.total()
            return self.floor(total_ttc)
        return 0

    def paymentline_amount_ttc(self):
        """
            Return the ttc amount of payment (in equal repartition)
        """
        total_ttc = 0
        for tva, total_ht in self.paymentline_amounts().items():
            line = LineCompute(cost=total_ht, tva=tva)
            total_ttc += self.floor(line.total())
        return total_ttc

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
                line_ttc = self.paymentline_amount_ttc()
                result = rest - ((payment_lines_num - 1) * line_ttc)
            else:
                sold_lines = self.manual_payment_line_amounts()[-1]
                result = 0
                for tva, total_ht in sold_lines.items():
                    line = LineCompute(tva=tva, cost=total_ht)
                    result += line.total()
        return result

class LineCompute(object):
    """
        Computing tool for line objects
    """
    cost = None
    tva = None
    quantity = 1

    def __init__(self, cost, tva, quantity=1):
        self.cost = cost
        self.tva = tva
        self.quantity = quantity

    def total_ht(self):
        """
            Compute the line's total
        """
        # Discount have amount attr not cost
        cost = getattr(self, "amount", self.cost) or 0
        quantity = self.quantity or 0
        return float(cost) * float(quantity)

    def tva_amount(self):
        """
            compute the tva amount of a line
        """
        totalht = self.total_ht()
        return compute_tva(totalht, self.tva)

    def total(self):
        """
            Compute the ttc amount of the line
        """
        return self.tva_amount() + self.total_ht()
