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

from autonomie.models.project import Phase, Project
from autonomie.models.user import User
from autonomie.models.task.task import Task
from autonomie.models.task.invoice import Invoice, Payment, CancelInvoice

INVOICE = dict( name=u"Facture 2",
                sequenceNumber=2,
                taskDate=datetime.date(2012, 12, 10), #u"10-12-2012",
                description=u"Description de la facture",
                _number=u"invoicenumber",
                expenses=0)

class TestPolymorphic(BaseTestCase):
    def setitUp(self):
        self.user = User(login=u"test_user1", firstname=u"firstname",
                                              lastname=u"lastname")
        self.project = Project(name=u"Projet", code=u"PROJ")
        self.phase = Phase(name="test", project=self.project)

    def test_invoice(self):
        self.setitUp()
        inv = Invoice(**INVOICE)
        inv.project = self.project
        inv.phase = self.phase
        self.session.add(inv)
        self.session.flush()
        task = self.session.query(Task)\
                .filter(Task.phase_id==self.phase.id).first()
        self.assertTrue(isinstance(task, Invoice))

    def test_payment(self):
        self.setitUp()
        inv = Invoice(**INVOICE)
        inv.CAEStatus = "valid"
        #inv.project = self.project
        inv.phase = self.phase
        inv.record_payment(amount=1500, mode="CHEQUE", resulted=True)
        self.session.add(inv)
        self.session.flush()
        p1 = self.session.query(Payment).join(Task)\
                .filter(Task.phase_id==self.phase.id).first()
        self.assertTrue(isinstance(p1.task, Invoice))
        self.assertFalse(isinstance(p1.task, CancelInvoice))

