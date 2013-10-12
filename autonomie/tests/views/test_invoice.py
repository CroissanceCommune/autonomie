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
from mock import MagicMock

from autonomie.views.invoice import InvoiceAdd
from autonomie.views.invoice import InvoiceStatus
from autonomie.views.invoice import duplicate
from autonomie.views.taskaction import make_task_delete_view

from autonomie.models.task.invoice import Invoice
from autonomie.models.user import User
from autonomie.models.project import Project
from autonomie.tests.base import BaseFunctionnalTest

TODAY = datetime.date.today()

APPSTRUCT = {'common': dict(phase_id=1,
                        customer_id=1,
                        address="address",
                        taskDate=TODAY,
                        description="Facture pour le customer test",
                        course="0",
                        displayedUnits="1",),
        'lines':dict(expenses=2000,
                     lines=[{'description':'text1', 'cost':10000,
                        'unity':'days', 'quantity':12, 'tva':1960}],
                     discounts=[{'description':'remise1', 'amount':1000,
                         'tva':1960}],),
        'payments':dict(paymentConditions="Payer à l'heure"),
        "communication":dict(statusComment=u"Aucun commentaire"),
        "submit":"draft"
        }


class Base(BaseFunctionnalTest):
    def task(self):
        return MagicMock(topay=lambda :7940, __name__='invoice',
                project=self.project())

    def project(self):
        return Project.query().first()

    def user(self):
        return User.query().first()

    def request(self, task=None, post_args=APPSTRUCT):
        request = self.get_csrf_request(post=post_args)
        if task is None:
            request.context = self.project()
            request.context.__name__ = 'project'
            request.matched_route = "project_invoices"
        else:
            request.matched_route = "invoice"
            request.context = task
        request.user = self.user()
        request.actionmenu = set()
        return request

    def addOne(self):
        self.config.add_route('project', '/')
        view = InvoiceAdd(self.request())
        view.submit_success(APPSTRUCT)

    def getOne(self):
        try:
            invoice = Invoice.query().filter(Invoice.phase_id==1).first()
            invoice.__name__ = 'invoice'
            return invoice
        except:
            return None

class TestInvoiceAdd(Base):
    def test_success(self):
        self.addOne()
        invoice = self.getOne()
        self.assertEqual(invoice.phase_id, 1)
        self.assertEqual(len(invoice.lines), 1)
        self.assertEqual(len(invoice.discounts), 1)

    def test_change_status(self):
        self.addOne()
        invoice = self.getOne()
        request = self.request(task=invoice, post_args={'submit':'wait'})
        view = InvoiceStatus(request)
        view()
        invoice = self.getOne()
        self.assertEqual(invoice.CAEStatus, "wait")

    def test_duplicate(self):
        self.config.testing_securitypolicy(userid="test",
                groupids=('admin',), permissive=True)
        self.config.add_route('invoice', '/inv')
        self.addOne()
        invoice = self.getOne()
        #The invoice status need to be at least wait to be duplicated
        invoice.CAEStatus = 'wait'
        request = self.request(task=invoice, post_args={'submit':'duplicate',
            'phase':"1", 'project':"1", 'customer':"1"})
        duplicate(request)
        invoices = Invoice.query().filter(Invoice.phase_id==1).all()
        self.assertEqual(len(invoices), 2)

    def test_delete(self):
        self.addOne()
        invoice = self.getOne()
        invoice.CAEstatus = 'wait'
        request = self.request(task=invoice, post_args={'submit':'delete'})
        view = make_task_delete_view("message")
        view(request)
        invoice = self.getOne()
        self.assertEqual(invoice, None)



