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
    interfaces for task handling
"""
from zope.interface import Attribute
from zope.interface import Interface


class ITask(Interface):
    """
        Task interface, need to be implemented by all documents
    """
    def is_invoice():
        """
            is the current task an invoice ?
        """

    def is_estimation():
        """
            Is the current task an estimation ?
        """

    def is_cancelinvoice():
        """
            Is the current task a cancelled invoice ?
        """


class IValidatedTask(ITask):
    """
        Interface for task needing to be validated by the office
    """
    def is_draft():
        """
            Return the draft status of a document
        """

    def is_editable(manage):
        """
            Is the current task editable ?
        """

    def is_valid():
        """
            Is the current task valid
        """

    def has_been_validated():
        """
            Has the current task been validated ?
        """

    def is_waiting():
        """
            Is the current task waiting for approval
        """

    def is_cancelled():
        """
            Has the current document been cancelled
        """


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


class IPaidTask(Interface):
    """
        Task interface for task needing to be paid
    """
    def is_paid():
        """
            Has the current task been paid
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

    def is_cancelled():
        """
            Has the current document been cancelled
        """

    def is_paid():
        """
            Has the current task been paid
        """

    def is_resulted():
        """
            Return True if the task is resulted (definitively paid)
        """

    def get_company():
        """
            Return the company this task is related to
        """

    def get_customer():
        """
            Return the customer this document is related to
        """
