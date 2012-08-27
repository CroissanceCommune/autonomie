# -*- coding: utf-8 -*-
# * File Name : test_models_tasks.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt

#
# * Creation Date : 27-07-2012
# * Last Modified :
#
# * Project :
#
"""
    Test Documents (Tasks):
        Estimations
        Invoices
        CancelInvoices
        ManualInvoices
"""

import datetime
from mock import MagicMock
from .base import BaseTestCase

from autonomie.models.task import Task
from autonomie.models.task import Estimation
from autonomie.models.task import Invoice
from autonomie.models.task import CancelInvoice
from autonomie.models.task import ManualInvoice
from autonomie.models.task import EstimationLine
from autonomie.models.task import InvoiceLine
from autonomie.models.task import PaymentLine
from autonomie.models.task import CancelInvoiceLine
from autonomie.models.task import TaskCompute

from autonomie.models.user import User

from autonomie.exception import Forbidden

TASK = dict(name=u"Test task",
                 CAEStatus="draft",
                 taskDate=datetime.date.today(),
                 statusDate=datetime.date.today(),
                 description=u"Test task description")

USER = dict(id=2,
            login=u"test_user1",
            firstname=u"user1_firstname",
            lastname=u"user1_lastname")

USER2 = dict(id=3, login=u"test_user2")

PROJECT = dict(id=1, name=u'project1', code=u"PRO1", id_company=1,
        code_client=u"CLI1")
CLIENT = dict(name=u"client1", id=u"CLI1", id_company=1)

ESTIMATION = dict(IDPhase=1,
                IDProject=1,
                name=u"Devis 2",
                sequenceNumber=2,
                CAEStatus="draft",
                course="0",
                displayedUnits="1",
                discountHT=2000,
                tva=1960,
                expenses=1500,
                deposit=20,
                exclusions=u"Notes",
                paymentDisplay=u"ALL",
                paymentConditions=u"Conditions de paiement",
                taskDate=datetime.date(2012, 12, 10), #u"10-12-2012",
                description=u"Description du devis",
                manualDeliverables=1,
                statusComment=u"Aucun commentaire",
                number=u"estnumber")
INVOICE = dict(IDPhase=1,
                IDProject=1,
                name=u"Facture 2",
                sequenceNumber=2,
                CAEStatus="draft",
                course="0",
                displayedUnits="1",
                discountHT=2000,
                tva=1960,
                expenses=1500,
                deposit=20,
                paymentConditions=u"Conditions de paiement",
                taskDate=datetime.date(2012, 12, 10), #u"10-12-2012",
                description=u"Description de la facture",
                statusComment=u"Aucun commentaire",
                number=u"invoicenumber")
LINES = [{'description':u'text1',
          'cost':10025,
          'unity':'DAY',
          'quantity':1.25,
          'rowIndex':1},
         {'description':u'text2',
          'cost':7500,
          'unity':'month',
          'quantity':3,
          'rowIndex':2},
         {'description':u'text3',
          'cost':-5200,
          "quantity":1,
          "unity":"DAY",
          "rowIndex":3,}]

PAYMENT_LINES = [{'description':u"Début",
                  "paymentDate":datetime.date(2012, 12, 12),
                  "amount":1000,
                  "rowIndex":1},
                 {'description':u"Milieu",
                  "paymentDate":datetime.date(2012, 12, 13),
                  "amount":1000, "rowIndex":2},
                 {'description':u"Fin",
                  "paymentDate":datetime.date(2012, 12, 14),
                  "amount":150,
                  "rowIndex":3}]

# Values:
#         the money values are represented *100
#
# Rounding rules:
#         TVA, total_ttc and deposit are rounded (total_ht is not)

# Lines total should accept until 4 elements after the '.'(here they are *100)
# so it fits the limit case
#
# Line totals should be floats (here they are *100)
EST_LINES_TOTAL = (12531.25, 22500, -5200)
LINES_TOTAL = sum(EST_LINES_TOTAL)

TVA = int((LINES_TOTAL - ESTIMATION['discountHT']) \
                * float(ESTIMATION['tva']) / 10000)

# EST_TOTAL = lines + tva + expenses rounded
EST_TOTAL = int(LINES_TOTAL - ESTIMATION['discountHT'] \
                        + TVA + ESTIMATION['expenses'])
EST_DEPOSIT = int(EST_TOTAL * ESTIMATION['deposit'] / 100.0)
PAYMENTSSUM = sum([p['amount'] for p in PAYMENT_LINES[:-1]])
EST_SOLD = EST_TOTAL - EST_DEPOSIT - PAYMENTSSUM

def get_client():
    client = MagicMock(**CLIENT)
    return client

def get_project():
    project = MagicMock(**PROJECT)
    project.client = get_client()
    project.get_next_estimation_number = lambda :2
    project.get_next_invoice_number = lambda :2
    project.get_next_cancelinvoice_number = lambda :2
    return project

def get_user(datas=USER):
    user = User(**datas)
    return user

def get_task(factory):
    user = get_user()
    task = factory(**TASK)
    task.statusPersonAccount = user
    task.owner = user
    return task

def get_estimation(user=None, project=None):
    est = Estimation(**ESTIMATION)
    for line in LINES:
        l = EstimationLine(**line)
        est.lines.append(l)
    for line in PAYMENT_LINES:
        l = PaymentLine(**line)
        est.payment_lines.append(l)
    if not user:
        user = get_user()
    if not project:
        project = get_project()
    est.project = project
    est.statusPersonAccount = user
    return est

def get_invoice(user=None, project=None):
    inv = Invoice(**INVOICE)
    for line in LINES:
        l = InvoiceLine(**line)
        inv.lines.append(l)
    if not user:
        user = get_user()
    if not project:
        project = get_project()
    inv.project = project
    inv.statusPersonAccount = user
    return inv

class TestTaskModels(BaseTestCase):
    def test_interfaces(self):
        from autonomie.models.task import ITask
        from autonomie.models.task import IValidatedTask
        from autonomie.models.task import IPaidTask
        from autonomie.models.task import IInvoice
        from zope.interface.verify import verifyObject
        self.assertTrue(verifyObject(ITask, Task()))
        self.assertTrue(verifyObject(IValidatedTask, Estimation()))
        self.assertTrue(verifyObject(IPaidTask, Invoice()))
        self.assertTrue(verifyObject(IPaidTask, CancelInvoice()))
        self.assertTrue(verifyObject(IInvoice, Invoice()))
        self.assertTrue(verifyObject(IInvoice, CancelInvoice()))
        self.assertTrue(verifyObject(IInvoice, ManualInvoice()))

    def test_task_status(self):
        task = get_task(factory=Task)
        self.assertEqual(task.get_status_suffix(),
                u" par user1_firstname user1_lastname le {:%d/%m/%Y}".format(
                                                        datetime.date.today()))
        #Estimations
        task = get_task(factory=Estimation)
        task.CAEStatus = 'draft'
        self.assertTrue(task.is_draft())
        self.assertTrue(task.is_editable())
        self.assertFalse(task.is_valid())
        self.assertFalse(task.has_been_validated())
        self.assertFalse(task.is_waiting())
        self.assertFalse(task.is_sent())
        task.CAEStatus = "wait"
        self.assertTrue(task.is_waiting())
        self.assertFalse(task.is_valid())
        self.assertFalse(task.is_editable())
        self.assertTrue(task.is_editable(manage=True))
        for i in ("valid", "sent", "geninv"):
            task.CAEStatus = i
            self.assertTrue(task.has_been_validated())
            self.assertFalse(task.is_editable())
        # Invoices
        task = get_task(factory=Invoice)
        task.CAEStatus = 'draft'
        self.assertTrue(task.is_draft())
        self.assertTrue(task.is_editable())
        self.assertFalse(task.is_valid())
        self.assertFalse(task.has_been_validated())
        self.assertFalse(task.is_waiting())
        self.assertFalse(task.is_sent())
        task.CAEStatus = "wait"
        self.assertTrue(task.is_waiting())
        self.assertFalse(task.is_valid())
        self.assertFalse(task.is_editable())
        self.assertTrue(task.is_editable(manage=True))
        for i in ("valid", "sent", "recinv"):
            task.CAEStatus = i
            self.assertTrue(task.has_been_validated())
            self.assertFalse(task.is_editable())
        task.CAEStatus = "paid"
        self.assertTrue(task.is_paid())
        # CancelInvoice
        task = get_task(factory=CancelInvoice)
        task.CAEStatus = 'draft'
        self.assertTrue(task.is_draft())
        self.assertTrue(task.is_editable())
        self.assertFalse(task.is_valid())
        self.assertFalse(task.has_been_validated())
        self.assertFalse(task.is_waiting())
        self.assertFalse(task.is_sent())
        task.CAEStatus = "wait"
        self.assertTrue(task.is_waiting())
        self.assertFalse(task.is_valid())
        self.assertFalse(task.is_editable())
        self.assertTrue(task.is_editable(manage=True))
        task.CAEStatus = "valid"
        self.assertTrue(task.is_valid())
        self.assertFalse(task.is_editable())
        for i in ("sent", "recinv"):
            task.CAEStatus = i
            self.assertTrue(task.has_been_validated())
            self.assertFalse(task.is_editable())
        task.CAEStatus = "paid"
        self.assertTrue(task.is_paid())

    def test_status_change(self):
        # Estimation
        task = get_task(factory=Estimation)
        for st in ("valid", "geninv", "sent", "aboest", "invalid"):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
        self.assertEqual(task.validate_status("nutt", "wait"), "wait")
        task.CAEStatus = "wait"
        for st in ("draft", "geninv", "sent",):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
        self.assertEqual(task.validate_status("nutt", "invalid"), "invalid")
        self.assertEqual(task.validate_status("nutt", "valid"), "valid")
        task.CAEStatus = "valid"
        for st in ("draft", "invalid", ):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
        for st in ("geninv", "sent", "aboest"):
            self.assertEqual(task.validate_status("nutt", st), st)
        task.CAEStatus = "sent"
        for st in ("draft", "invalid", "valid"):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
        task.CAEStatus = "geninv"
        for st in ("draft", "invalid", "sent", "valid", "aboest"):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)

        # Invoice
        task = get_task(factory=Invoice)
        for st in ("valid", "sent", "aboinv", "invalid"):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
        self.assertEqual(task.validate_status("nutt", "wait"), "wait")
        task.CAEStatus = "wait"
        for st in ("draft", "sent",):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
        self.assertEqual(task.validate_status("nutt", "invalid"), "invalid")
        self.assertEqual(task.validate_status("nutt", "valid"), "valid")
        task.CAEStatus = "valid"
        for st in ("draft", "invalid"):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
        for st in ("sent", "aboinv", "recinv", "paid"):
            self.assertEqual(task.validate_status("nutt", st), st)
        task.CAEStatus = "sent"
        for st in ("draft", "invalid", "valid"):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
        for st in ("aboinv", "recinv", "paid"):
            self.assertEqual(task.validate_status("nutt", st), st)
        task.CAEStatus = "paid"
        for st in ("draft", "invalid", "sent", "valid", "aboinv", "recinv",
                                                                    ):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)

        # CancelInvoice
        task = get_task(factory=CancelInvoice)
        # Removing Direct validation of the cancelinvoice
        task.CAEStatus = 'wait'
        task.CAEStatus = "valid"
        for st in ("draft",):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
        for st in ("sent", "paid", ):
            self.assertEqual(task.validate_status("nutt", st), st)
        task.CAEStatus = "sent"
        for st in ("draft", "valid"):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)
        task.CAEStatus = "paid"
        for st in ("draft", "sent", "valid"):
            self.assertRaises(Forbidden, task.validate_status, "nutt", st)

class TestComputing(BaseTestCase):
    def test_line_total(self):
        for index, line in enumerate(LINES):
            for obj in InvoiceLine, CancelInvoiceLine, EstimationLine:
                line_obj = obj(**line)
                self.assertEqual(line_obj.total(), EST_LINES_TOTAL[index])

    def test_lines_total(self):
        task = TaskCompute()
        task.lines = []
        for index, line in enumerate(LINES):
            task.lines.append(InvoiceLine(**line))
        self.assertEqual(task.lines_total(), sum(EST_LINES_TOTAL))
        for obj, line_obj in ((Invoice, InvoiceLine), \
                            (CancelInvoice, CancelInvoiceLine), \
                            (Estimation, EstimationLine)):
            task = get_task(factory=obj)
            for line in LINES:
                task.lines.append(line_obj(**line))
            self.assertEqual(task.lines_total(), sum(EST_LINES_TOTAL))

    def test_total_ht(self):
        est = get_estimation()
        self.assertEqual(est.total_ht(),
                    sum(EST_LINES_TOTAL)-ESTIMATION['discountHT'])

    def test_tva_amount(self):
        task = TaskCompute()
        task.tva = 1960
        # cf #501
        # ici 5010 correpond à 50€10
        self.assertEqual(task.tva_amount(5010), 981)

        est = get_estimation()
        self.assertEqual(est.tva_amount(), TVA)

    def test_total_ttc(self):
        line = InvoiceLine(cost=1030, quantity=1.25, rowIndex=1,
                            description='')
        # cf ticket #501
        # line total : 12.875
        # tva : 2.5235 -> 2.52
        # A confirmer :l'arrondi ici bas
        # => total : 15.39 (au lieu de 15.395)
        task = TaskCompute()
        task.tva = 1960
        task.lines = [line]
        self.assertEqual(task.total_ttc(), 1539)

    def test_total(self):
        est = get_estimation()
        self.assertEqual(est.total(), EST_TOTAL)

class TestEstimation(BaseTestCase):
    def test_get_name(self):
        self.assertEqual(Estimation.get_name(5), u"Devis 5")

    def test_duplicate_estimation(self):
        user = get_user(USER2)
        project = get_project()
        est = get_estimation(user, project)
        newest = est.duplicate(user, project)
        self.assertEqual(newest.CAEStatus, 'draft')
        self.assertEqual(newest.project, project)
        self.assertEqual(newest.statusPersonAccount, user)
        self.assertTrue(newest.number.startswith("PRO1_CLI1_D2_"))

    def test_duplicate_estimation_integration(self):
        """
            Here we test the duplication on a real world case
            specifically, the client is not loaded in the session
            causing the insert statement to be fired during duplication
        """
        from autonomie.models.user import User
        from autonomie.models.model import Project
        user = self.session.query(User).first()
        project = self.session.query(Project).first()
        est = get_estimation(user, project)
        self.assertEqual(est.statusPersonAccount, user)
        self.assertEqual(est.project, project)
        est.IDEmployee = user.id
        est = self.session.merge(est)
        self.session.flush()
        newest = est.duplicate(user, project)
        self.session.merge(newest)
        self.session.flush()

    def test_estimation_deposit(self):
        est = get_estimation()
        self.assertEqual(est.deposit_amount(), EST_DEPOSIT)

    def test_sold(self):
        est = get_estimation()
        self.assertEqual(est.sold(), EST_SOLD)

    def test_payments_sum(self):
        est = get_estimation()
        self.assertEqual(est.sold() + est.deposit_amount()
                + sum([p.amount for p in est.payment_lines[:-1]]),
                est.total())

    def test_get_number(self):
        project = get_project()
        seq_number = 15
        date = datetime.date(1969, 07, 31)
        self.assertEqual(Estimation.get_number(project, seq_number, date),
                        u"PRO1_CLI1_D15_0769")

    def test_gen_invoice(self):
        est = get_estimation()
        invoices = est.gen_invoices(1)
        for inv in invoices:
            self.session.add(inv)
            self.session.flush()
        #deposit :
        deposit = invoices[0]
        self.assertEqual(deposit.taskDate, datetime.date.today())
        self.assertEqual(deposit.total_ht(), est.deposit_amount())
        #intermediate invoices:
        intermediate_invoices = invoices[1:-1]
        for index, line in enumerate(PAYMENT_LINES[:-1]):
            inv = intermediate_invoices[index]
            self.assertEqual(inv.total_ht(), line['amount'])
            self.assertEqual(inv.taskDate, line['paymentDate'])

class TestInvoice(BaseTestCase):
    def test_get_name(self):
        self.assertEqual(Invoice.get_name(5), u"Facture 5")
        self.assertEqual(Invoice.get_name(5, sold=True), u"Facture de solde")
        self.assertEqual(Invoice.get_name(5, account=True),
                                                      u"Facture d'acompte 5")

    def test_get_number(self):
        project = get_project()
        seq_number = 15
        date = datetime.date(1969, 07, 31)
        self.assertEqual(Invoice.get_number(project, seq_number, date),
                        u"PRO1_CLI1_F15_0769")
        self.assertEqual(Invoice.get_number(project, seq_number, date,
                        deposit=True), u"PRO1_CLI1_FA15_0769")

    def test_gen_cancelinvoice(self):
        user = User(**USER)
        inv = get_invoice(user=user)
        cinv = inv.gen_cancelinvoice(user.id)
        self.session.add(cinv)
        self.session.flush()

        self.assertEqual(cinv.name, "Avoir 2")
        self.assertEqual(cinv.total_ht(), -1 * inv.total_ht())
        today = datetime.date.today()
        self.assertEqual(cinv.taskDate, today)

class TestCancelInvoice(BaseTestCase):
    def test_get_name(self):
        self.assertEqual(CancelInvoice.get_name(5), u"Avoir 5")

    def test_get_number(self):
        project = get_project()
        seq_number = 15
        date = datetime.date(1969, 07, 31)
        self.assertEqual(CancelInvoice.get_number(project, seq_number, date),
                        u"PRO1_CLI1_A15_0769")


class TestEstimationLine(BaseTestCase):
    def test_get_unity(self):
        i = InvoiceLine(unity='HOUR')
        self.assertEqual(i.get_unity_label(), u'heure(s)')
        i = InvoiceLine(unity='SHIT')
        self.assertEqual(i.get_unity_label(), u'-')
        self.assertEqual(i.get_unity_label(pretty=True), u'')

    def test_duplicate_line(self):
        line = EstimationLine(**LINES[1])
        dline = line.duplicate()
        for i in ('rowIndex', 'cost', "description", "quantity", "unity"):
            self.assertEqual(getattr(dline, i), getattr(line, i))

    def test_gen_invoiceline(self):
        line = EstimationLine(**LINES[1])
        iline = line.gen_invoice_line()
        for i in ('rowIndex', 'cost', "description", "quantity", "unity"):
            self.assertEqual(getattr(line, i), getattr(iline, i))

    def test_total(self):
        i = EstimationLine(cost=1.25, quantity=1.25)
        self.assertEqual(i.total(), 1.5625)

class TestInvoiceLine(BaseTestCase):
    def test_get_unity(self):
        i = InvoiceLine(unity='HOUR')
        self.assertEqual(i.get_unity_label(), u'heure(s)')
        i = InvoiceLine(unity='SHIT')
        self.assertEqual(i.get_unity_label(), u'-')
        self.assertEqual(i.get_unity_label(pretty=True), u'')

    def test_duplicate_line(self):
        line = InvoiceLine(**LINES[1])
        dline = line.duplicate()
        for i in ('rowIndex', 'cost', "description", "quantity", "unity"):
            self.assertEqual(getattr(dline, i), getattr(line, i))


    def test_gen_cancelinvoice_line(self):
        line = InvoiceLine(**LINES[1])
        cline = line.gen_cancelinvoice_line()
        for i in ('rowIndex', "description", "quantity", "unity"):
            self.assertEqual(getattr(cline, i), getattr(line, i))
        self.assertEqual(cline.cost, -1 * line.cost)

    def test_total(self):
        i = InvoiceLine(cost=1.25, quantity=1.25)
        self.assertEqual(i.total(), 1.5625)

class TestCancelInvoiceLine(BaseTestCase):
    def test_duplicate_line(self):
        line = CancelInvoiceLine(**LINES[1])
        dline = line.duplicate()
        for i in ('rowIndex', 'cost', "description", "quantity", "unity"):
            self.assertEqual(getattr(dline, i), getattr(line, i))

    def test_total(self):
        i = CancelInvoiceLine(cost=1.25, quantity=1.25)
        self.assertEqual(i.total(), 1.5625)

class TestPaymentLine(BaseTestCase):
    def test_duplicate(self):
        line = PaymentLine(**PAYMENT_LINES[0])
        dline = line.duplicate()
        for i in ('rowIndex', 'description', 'amount'):
            self.assertEqual(getattr(line, i), getattr(dline, i))
        today = datetime.date.today()
        self.assertEqual(dline.paymentDate, today)

