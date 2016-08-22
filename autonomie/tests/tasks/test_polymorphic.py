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

from autonomie.models.project import Phase, Project
from autonomie.models.user import User
from autonomie.models.customer import Customer
from autonomie.models.company import Company
from autonomie.models.task.task import Task
from autonomie.models.task.invoice import Invoice, Payment, CancelInvoice

INVOICE = dict( name=u"Facture 2",
                date=datetime.date(2012, 12, 10), #u"10-12-2012",
                description=u"Description de la facture",
                expenses=0,
                expenses_ht=0)


@pytest.fixture
def project(content):
    proj = Project.query().first()
    proj.code = "PRO1"
    proj.phases.append(Phase(name="test"))
    return proj


@pytest.fixture
def user(content):
    return User.query().first()


@pytest.fixture
def company(content):
    return Company.query().first()


@pytest.fixture
def customer(content):
    res = Customer.query().first()
    res.code = "CLI1"
    return res


@pytest.fixture
def invoice(project, user, customer, company):
    invoice = Invoice(
        company,
        customer,
        project,
        project.phases[-1],
        user,
    )
    for key, value in INVOICE.items():
        setattr(invoice, key, value)
    return invoice


def test_invoice(dbsession, invoice):
    phase_id = invoice.phase.id
    dbsession.add(invoice)
    dbsession.flush()
    task = dbsession.query(Task)\
            .filter(Task.phase_id==phase_id).first()
    assert isinstance(task, Invoice)


def test_payment(dbsession, invoice):
    phase_id = invoice.phase.id
    invoice.CAEStatus = "valid"
    invoice.record_payment(amount=1500, mode="CHEQUE", resulted=True)
    dbsession.add(invoice)
    dbsession.flush()
    p1 = dbsession.query(Payment).join(Task)\
            .filter(Task.phase_id==phase_id).first()
    assert isinstance(p1.task, Invoice)
    assert not isinstance(p1.task, CancelInvoice)

