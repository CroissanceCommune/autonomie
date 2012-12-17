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
from mock import MagicMock
from autonomie.tests.base import BaseTestCase, printstatus
from autonomie.models.task import (CancelInvoice, ManualInvoice,
                                    Invoice, InvoiceLine, DiscountLine)
from autonomie.models.user import User
from autonomie.models.project import Phase, Project

LINES = [{'description':u'text1',
          'cost':10025,
           'tva':1960,
          'unity':'DAY',
          'quantity':1.25,
          'rowIndex':1},
         {'description':u'text2',
          'cost':7500,
           'tva':1960,
          'unity':'month',
          'quantity':3,
          'rowIndex':2}]

DISCOUNTS = [{'description':u"Remise à 19.6", 'amount':2000, 'tva':1960}]

INVOICE = dict( name=u"Facture 2",
                sequenceNumber=2,
                taskDate=datetime.date(2012, 12, 10), #u"10-12-2012",
                description=u"Description de la facture",
                number=u"invoicenumber",
                expenses=0)

class TestCancelInvoice(BaseTestCase):
    def test_get_name(self):
        self.assertEqual(CancelInvoice.get_name(5), u"Avoir 5")

    def test_get_number(self):
        project = MagicMock(code="PRO1", client=MagicMock(code="CLI1"))
        seq_number = 15
        date = datetime.date(1969, 07, 31)
        self.assertEqual(CancelInvoice.get_number(project, seq_number, date),
                        u"PRO1_CLI1_A15_0769")

class TestManualInvoice(BaseTestCase):
    def test_tva_amount(self):
        m = ManualInvoice(montant_ht=1950)
        self.assertEqual(m.tva_amount(), 0)

class TestInvoice(BaseTestCase):

    def getOne(self):
        inv = Invoice(**INVOICE)
        for line in LINES:
            inv.lines.append(InvoiceLine(**line))
        for discount in DISCOUNTS:
            inv.discounts.append(DiscountLine(**discount))
        return inv

    def test_get_name(self):
        self.assertEqual(Invoice.get_name(5), u"Facture 5")
        self.assertEqual(Invoice.get_name(5, sold=True), u"Facture de solde")
        self.assertEqual(Invoice.get_name(5, account=True),
                                                      u"Facture d'acompte 5")

    def test_get_number(self):
        project = MagicMock(code="PRO1", client=MagicMock(code="CLI1"))
        seq_number = 15
        date = datetime.date(1969, 07, 31)
        self.assertEqual(Invoice.get_number(project, seq_number, date),
                        u"PRO1_CLI1_F15_0769")
        self.assertEqual(Invoice.get_number(project, seq_number, date,
                        deposit=True), u"PRO1_CLI1_FA15_0769")

    def test_gen_cancelinvoice(self):
        user = User.query().first()
        project = Project.query().first()
        inv = self.getOne()
        inv.project = project
        inv.owner = user
        inv.statusPersonAccount = user

        self.session.add(inv)
        self.session.flush()
        cinv = inv.gen_cancelinvoice(user.id)
        self.session.add(cinv)
        self.session.flush()

        self.assertEqual(cinv.name, "Avoir 1")
        self.assertEqual(cinv.total_ht(), -1 * inv.total_ht())
        today = datetime.date.today()
        self.assertEqual(cinv.taskDate, today)

    def test_gen_cancelinvoice_payment(self):
        user = User.query().first()
        project = Project.query().first()
        inv = self.getOne()
        inv.project = project
        inv.owner = user
        inv.statusPersonAccount = user
        inv.record_payment(mode="c", amount=1500)
        cinv = inv.gen_cancelinvoice(user.id)
        self.assertEqual(len(cinv.lines),
                          len(inv.lines) + len(inv.discounts) + 1)
        self.assertEqual(cinv.lines[-1].cost, 1500)

    def test_duplicate_invoice(self):
        user = self.session.query(User).first()
        project = self.session.query(Project).first()
        phase = self.session.query(Phase).first()
        inv = self.getOne()
        inv.owner = user
        inv.statusPersonAccount = user
        inv.project = project
        inv.phase = phase

        newinv = inv.duplicate(user, project, phase)
        self.assertEqual(len(inv.lines), len(newinv.lines))
        self.assertEqual(len(inv.discounts), len(newinv.discounts))
        self.assertEqual(inv.project, newinv.project)
        self.assertEqual(newinv.statusPersonAccount, user)
        self.assertEqual(newinv.phase, phase)

    def test_duplicate_invoice_integration(self):
        user = self.session.query(User).first()
        printstatus(user)
        project = self.session.query(Project).first()
        phase = self.session.query(Phase).first()
        inv = self.getOne()
        inv.phase = phase
        inv.owner = user
        inv.statusPersonAccount = user
        inv.project = project
        self.session.add(inv)
        self.session.flush()
        newest = inv.duplicate(user, project, phase)
        self.session.add(newest)
        self.session.flush()
        self.assertEqual(newest.phase_id, phase.id)
        self.assertEqual(newest.owner_id, user.id)
        self.assertEqual(newest.statusPerson, user.id)
        self.assertEqual(newest.project_id, project.id)

#
#    def test_valid_invoice(self):
#        inv = get_invoice(stripped=True)
#        self.session.add(inv)
#        self.session.flush()
#        self.config.testing_securitypolicy(userid='test', permissive=True)
#        request = testing.DummyRequest()
#        inv.set_status('wait', request, 1)
#        self.session.merge(inv)
#        self.session.flush()
#        inv.set_status('valid', request, 1)
#        today = datetime.date.today()
#        self.assertEqual(inv.taskDate, today)
#        self.assertEqual(inv.officialNumber, 1)
#
#    def test_valid_payment(self):
#        inv = get_invoice(stripped=True)
#        self.session.add(inv)
#        self.session.flush()
#        self.config.testing_securitypolicy(userid='test', permissive=True)
#        request = testing.DummyRequest()
#        inv.set_status('wait', request, 1)
#        self.session.merge(inv)
#        self.session.flush()
#        inv.set_status('valid', request, 1)
#        self.session.merge(inv)
#        self.session.flush()
#        inv.set_status("paid", request, 1, amount=150, mode="CHEQUE")
#        inv = self.session.merge(inv)
#        self.session.flush()
#        invoice = self.session.query(Invoice)\
#                .filter(Invoice.id==inv.id).first()
#        self.assertEqual(invoice.CAEStatus, 'paid')
#        self.assertEqual(len(invoice.payments), 1)
#        self.assertEqual(invoice.payments[0].amount, 150)
