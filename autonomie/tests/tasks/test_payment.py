# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 17-12-2012
# * Last Modified :
#
# * Project :
#
import datetime

from autonomie.tests.base import BaseTestCase
from autonomie.models.task.states import record_payment
from autonomie.models.task import Payment
from autonomie.models.task import Invoice, InvoiceLine

INVOICE = dict( name=u"Facture 2",
                sequenceNumber=2,
                taskDate=datetime.date(2012, 12, 10), #u"10-12-2012",
                description=u"Description de la facture",
                number=u"invoicenumber",
                expenses=0)

LINE = {'description':u'text1', 'cost':10000, 'tva':1960,
              'unity':'DAY', 'quantity':1, 'rowIndex':1}

PAYMENTS = [
            {'amount':1500, 'mode':'CHEQUE'},
            {'amount':1895, 'mode':'CHEQUE'},
            ]

class TestPayment(BaseTestCase):

    def get_task(self):
        inv = Invoice(**INVOICE)
        inv.lines = [InvoiceLine(**LINE)]
        for i in PAYMENTS:
            inv.payments.append(Payment(**i))
        return inv

    def test_record_payment(self):
        task = self.get_task()
        request_params = {'amount':1500, 'mode':'cheque'}
        record_payment(task, **request_params)
        self.assertEqual(len(task.payments), 3)
        self.assertEqual(task.payments[2].amount, 1500)
        self.session.add(task)
        self.session.flush()

    def test_payment_get_amount(self):
        payment = Payment(**PAYMENTS[1])
        self.assertEqual(payment.get_amount(), 1895)

    def test_invoice_topay(self):
        task = self.get_task()
        self.assertEqual(task.paid(), 3395)
        self.assertEqual(task.topay(), 11960 - 3395)

    def test_resulted_manual(self):
        task = self.get_task()
        task.CAEStatus = 'wait'
        task.CAEStatus = 'valid'
        task.CAEStatus = 'paid'
        request_params = {'amount':0, 'mode':'cheque', 'resulted':True}
        record_payment(task, **request_params)
        self.assertEqual(task.CAEStatus, 'resulted')

    def test_resulted_auto(self):
        task = self.get_task()
        task.CAEStatus = 'wait'
        task.CAEStatus = 'valid'
        task.CAEStatus = 'paid'
        request_params = {'amount':int(task.topay()), 'mode':'cheque'}
        record_payment(task, **request_params)
        self.assertEqual(task.CAEStatus, 'resulted')
