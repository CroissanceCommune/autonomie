# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2016 Croissance Commune
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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

from zope.interface import Interface
from zope.interface import Attribute


class ITreasuryInvoiceProducer(Interface):
    """
    Interface for the class that will produce treasury invoice export lines
    """
    def get_book_entries(self, invoicelist):
        pass


class ITreasuryInvoiceWriter(Interface):
    """
    Interface for the module handling the generation of the tabular export file
    """
    def set_datas(self, lines):
        """
        Set the tabular datas that will be written in the output file
        """
        pass


class ITreasuryExpenseProducer(Interface):
    """
    Interface for the class that will produce treasury expense export lines
    """
    def get_book_entries(self, expenselist):
        pass


class ITreasuryExpenseWriter(Interface):
    """
    Interface for the module handling the generation of the tabular export file
    """
    def set_datas(self, lines):
        """
        Set the tabular datas that will be written in the output file
        """
        pass


class ITreasuryPaymentProducer(Interface):
    """
    Interface for the class that will produce treasury payment export lines
    """
    def get_book_entries(self, paymentlist):
        pass


class ITreasuryPaymentWriter(Interface):
    """
    Interface for the module handling the generation of the tabular export file
    """
    def set_datas(self, lines):
        """
        Set the tabular datas that will be written in the output file
        """
        pass


class IFileRequirementService(Interface):
    """
    Describe the way a File Requirement service should work
    """
    def populate(parent_object):
        """
        Populate the parent_object with File Requirements
        """
        pass

    def register(sale_node, file_object):
        """
        Register the file_object against the associated indicators
        """
        pass


class IMoneyTask(Interface):
    """
        Interface for task handling money
    """
    def lines_total_ht():
        """
            Return the sum of the document lines
        """

    def total_ht():
        """
            return the HT total of the document
        """

    def discount_total_ht():
        """
            Return the HT discount
        """

    def get_tvas():
        """
            Return a dict with the tva amounts stored by tva reference
        """

    def tva_amount():
        """
            Return the amount of Tva to be paid
        """

    def total_ttc():
        """
            compute the ttc value before expenses
        """

    def total():
        """
            compute the total to be paid
        """

    def expenses_amount():
        """
            return the TTC expenses
        """


class IInvoice(Interface):
    """
        Invoice interface (used to get an uniform invoice list display
        See templates/invoices.mako (under invoice.model) to see the expected
        common informations
    """
    official_number = Attribute("""official number used in sage""")

    def total_ht():
        """
            Return the HT total of the current document
        """

    def tva_amount():
        """
            Return the sum of the tvas
        """

    def total():
        """
            Return the TTC total
        """

    def get_company():
        """
            Return the company this task is related to
        """

    def get_customer():
        """
            Return the customer this document is related to
        """
