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

import datetime
import pytest

from autonomie.models.task.states import record_payment
from autonomie.models.task import Payment
from autonomie.models.task import Invoice, InvoiceLine

INVOICE = dict( name=u"Facture 2",
                sequence_number=2,
                taskDate=datetime.date(2012, 12, 10), #u"10-12-2012",
                description=u"Description de la facture",
                _number=u"invoicenumber",
                expenses=0,
                expenses_ht=0)

LINE = {'description':u'text1', 'cost':10000, 'tva':1960,
              'unity':'DAY', 'quantity':1, 'rowIndex':1}

PAYMENTS = [
            {'amount':1500, 'mode':'CHEQUE'},
            {'amount':1895, 'mode':'CHEQUE'},
            ]

@pytest.fixture
def invoice():
    inv = Invoice(**INVOICE)
    inv.lines = [InvoiceLine(**LINE)]
    for i in PAYMENTS:
        inv.payments.append(Payment(**i))
    return inv


def test_record_payment(invoice):
    request_params = {'amount':1500, 'mode':'cheque'}
    record_payment(invoice, **request_params)
    assert len(invoice.payments) == 3
    assert invoice.payments[2].amount == 1500


def test_payment_get_amount():
    payment = Payment(**PAYMENTS[1])
    assert payment.get_amount() == 1895


def test_invoice_topay(invoice):
    assert invoice.paid() == 3395
    assert invoice.topay() == 11960 - 3395


def test_resulted_manual(invoice):
    invoice.CAEStatus = 'wait'
    invoice.CAEStatus = 'valid'
    invoice.CAEStatus = 'paid'
    request_params = {'amount':0, 'mode':'cheque', 'resulted':True}
    record_payment(invoice, **request_params)
    assert invoice.CAEStatus == 'resulted'


def test_resulted_auto(invoice):
    invoice.CAEStatus = 'wait'
    invoice.CAEStatus = 'valid'
    invoice.CAEStatus = 'paid'
    request_params = {'amount':int(invoice.topay()), 'mode':'cheque'}
    record_payment(invoice, **request_params)
    assert invoice.CAEStatus == 'resulted'
