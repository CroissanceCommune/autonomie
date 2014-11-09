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
from autonomie.models.task.task import Task
from autonomie.models.task.invoice import Invoice, Payment, CancelInvoice

INVOICE = dict( name=u"Facture 2",
                sequenceNumber=2,
                taskDate=datetime.date(2012, 12, 10), #u"10-12-2012",
                description=u"Description de la facture",
                _number=u"invoicenumber",
                expenses=0,
                expenses_ht=0)

@pytest.fixture
def objects():
    user = User(login=u"test_user1", firstname=u"firstname",
                                       lastname=u"lastname")
    project = Project(name=u"Projet", code=u"PROJ")
    phase = Phase(name="test", project=project)
    return (user, phase, project)

def test_invoice(dbsession, objects):
    user, phase, project = objects
    inv = Invoice(**INVOICE)
    inv.project = project
    inv.phase = phase
    dbsession.add(inv)
    dbsession.flush()
    task = dbsession.query(Task)\
            .filter(Task.phase_id==phase.id).first()
    assert isinstance(task, Invoice)

def test_payment(dbsession, objects):
    user, phase, project = objects
    inv = Invoice(**INVOICE)
    inv.CAEStatus = "valid"
    #inv.project = project
    inv.phase = phase
    inv.record_payment(amount=1500, mode="CHEQUE", resulted=True)
    dbsession.add(inv)
    dbsession.flush()
    p1 = dbsession.query(Payment).join(Task)\
            .filter(Task.phase_id==phase.id).first()
    assert isinstance(p1.task, Invoice)
    assert not isinstance(p1.task, CancelInvoice)

