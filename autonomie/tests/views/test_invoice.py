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
import pytest
import datetime
from mock import MagicMock


from autonomie.models.task.invoice import Invoice
from autonomie.models.user import User
from autonomie.models.project import Project

TODAY = datetime.date.today()

APPSTRUCT = {'common': dict(phase_id=1,
                        customer_id=1,
                        address="address",
                        taskDate=TODAY,
                        description="Facture pour le customer test",
                        course="0",
                        display_units="1",),
        'lines':dict(expenses=2000,
                     lines=[{'description':'text1', 'cost':10000,
                        'unity':'days', 'quantity':12, 'tva':1960}],
                     discounts=[{'description':'remise1', 'amount':1000,
                         'tva':1960}],),
        'payments':dict(payment_conditions="Payer à l'heure"),
        "communication":dict(statusComment=u"Aucun commentaire"),
        "submit":"draft"
        }

@pytest.fixture
def project(content):
    return Project.query().first()

@pytest.fixture
def task(project):
    return MagicMock(
        topay=lambda :7940,
        __name__='invoice',
        project=project)

@pytest.fixture
def user(content):
    return User.query().first()


@pytest.fixture
def invoice(config, get_csrf_request_with_db, project, user):
    print(Invoice.query().all())
    assert len(Invoice.query().all()) == 0
    from autonomie.views.invoice import InvoiceAdd
    config.add_route('project', '/')
    request = get_csrf_request_with_db(post=APPSTRUCT)
    request.context = project
    request.context.__name__ = 'project'
    request.matched_route = "project_invoices"
    request.user = user
    request.context = project
    view = InvoiceAdd(request)
    view.submit_success(APPSTRUCT)
    return getone()

def getone():
    invoice = Invoice.query().filter(Invoice.phase_id==1).first()
    if invoice is not None:
        invoice.__name__ = 'invoice'
    return invoice

def test_add_invoice(invoice):
    assert invoice.phase_id == 1
    assert len(invoice.lines) == 1
    assert len(invoice.discounts) == 1
    assert invoice.description == "Facture pour le customer test"

def test_change_status(invoice, get_csrf_request_with_db):
    request = get_csrf_request_with_db(post={'submit':'wait'})
    request.context = invoice
    request.matched_route = "invoice"

    from autonomie.views.invoice import InvoiceStatus
    view = InvoiceStatus(request)
    view()
    invoice = getone()
    assert invoice.CAEStatus == "wait"

def test_duplicate(config, content, dbsession, invoice, get_csrf_request_with_db):
    from autonomie.views.invoice import duplicate
    config.testing_securitypolicy(userid="test", groupids=('admin',),
                                  permissive=True)
    config.add_route('invoice', '/inv')
    #The invoice status need to be at least wait to be duplicated
    invoice.CAEStatus = 'wait'
    request = get_csrf_request_with_db(
        post={'submit':'duplicate', 'phase':"1", 'project':"1", 'customer':"1"}
    )
    request.context = invoice
    request.matched_route = "invoice"
    duplicate(request)
    dbsession.flush()
    invoices = Invoice.query().filter(Invoice.phase_id==1).all()
    assert len(invoices) == 2

def test_delete(invoice, get_csrf_request_with_db):
    from autonomie.views.taskaction import make_task_delete_view
    invoice.CAEstatus = 'wait'
    request = get_csrf_request_with_db(post={'submit':'delete'})
    request.context = invoice
    request.matched_route = "invoice"
    view = make_task_delete_view("message")
    view(request)
    invoice = getone()
    assert invoice == None



