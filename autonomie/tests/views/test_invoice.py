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
from autonomie.tests.tools import Dummy


TODAY = datetime.date.today()


def test_add_invoice(config, get_csrf_request_with_db, project, phase, company,
                     user, customer, ):
    from autonomie.models.task.invoice import Invoice
    from autonomie.views.invoices.invoice import InvoiceAdd
    config.add_route('/invoices/{id}', "/")
    value = {
        "name": u"Facture",
        'course': True,
        'project_id': project.id,
        'phase_id': phase.id,
        'customer_id': customer.id,
    }

    request = get_csrf_request_with_db()
    request.context = project
    request.current_company = company.id
    request.matched_route = Dummy(name="project_invoices")
    request.user = user
    view = InvoiceAdd(request)
    view.submit_success(value)

    # view.submit_success(value)
    invoice = Invoice.query().first()

    assert invoice.name == u"Facture"
    assert invoice.phase_id == phase.id
    assert invoice.customer_id == customer.id
    assert invoice.project_id == project.id
    assert invoice.course is True


# def test_duplicate(config, content, dbsession, invoice, get_csrf_request_with_db):
#     from autonomie.views.invoice import duplicate
#     config.testing_securitypolicy(userid="test", groupids=('admin',),
#                                   permissive=True)
#     config.add_route('invoice', '/inv')
#     #The invoice status need to be at least wait to be duplicated
#     invoice.status = 'wait'
#     request = get_csrf_request_with_db(
#         post={'submit':'duplicate', 'phase':"1", 'project':"1", 'customer':"1"}
#     )
#     request.context = invoice
#     request.matched_route = "invoice"
#     duplicate(request)
#     dbsession.flush()
#     invoices = Invoice.query().filter(Invoice.phase_id==1).all()
#     assert len(invoices) == 2
#
# def test_delete(invoice, get_csrf_request_with_db):
#     from autonomie.views.taskaction import make_task_delete_view
#     invoice.status = 'wait'
#     request = get_csrf_request_with_db(post={'submit':'delete'})
#     request.context = invoice
#     request.matched_route = "invoice"
#     view = make_task_delete_view("message")
#     view(request)
#     invoice = getone()
#     assert invoice == None
