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
    from autonomie.views.project.routes import PROJECT_ITEM_INVOICE_ROUTE
    from autonomie.views.invoices.invoice import InvoiceAddView
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
    request.matched_route = Dummy(name=PROJECT_ITEM_INVOICE_ROUTE)
    request.user = user
    view = InvoiceAddView(request)
    view.submit_success(value)

    # view.submit_success(value)
    invoice = Invoice.query().first()

    assert invoice.name == u"Facture"
    assert invoice.phase_id == phase.id
    assert invoice.customer_id == customer.id
    assert invoice.project_id == project.id
    assert invoice.course is True
