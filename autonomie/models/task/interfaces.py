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
    def lines_total():
        """
            Return the sum of the document lines
        """

    def total_ht():
        """
            return the HT total of the document
        """

    def discount_amount():
        """
            Return the discount
        """

    def tva_amount(totalht):
        """
            compute the tva
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
    def is_tolate():
        """
            Is the payment of the current task to late ?
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
    statusComment = Attribute("""statusComment to allow discussion""")
    statusDate = Attribute("""The date the status has last been changed""")
    officialNumber = Attribute("""official number used in sage""")
    taskDate = Attribute("""Date of the task""")
    id = Attribute("""the document sql id""")
    number = Attribute("""the document's non official number""")
    description = Attribute("""the document description string""")

    def get_company():
        """
            Return the company this task is related to
        """

    def get_client():
        """
            Return the client this document is related to
        """

    def is_paid():
        """
            Has the current task been paid
        """

    def is_cancelled():
        """
            Has the current document been cancelled
        """

    def is_tolate():
        """
            Is it too late
        """

    def is_invoice():
        """
            is the current task an invoice ?
        """

    def is_cancelinvoice():
        """
            Is the current task a cancelled invoice ?
        """

    def is_resulted():
        """
            Return True if the task is resulted (definitively paid)
        """

