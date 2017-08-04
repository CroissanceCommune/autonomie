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

"""
    View for assets
"""
import logging

from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.task import (
    CancelInvoice,
)
from autonomie.views.files import FileUploadView
from autonomie.views import (
    BaseEditView,
)
from autonomie.views.task.views import (
    TaskEditView,
    TaskDeleteView,
    TaskHtmlView,
    TaskPdfView,
)


log = logging.getLogger(__name__)


class CancelInvoiceEditView(TaskEditView):
    def title(self):
        return u"Modification de l'avoir {task.name}".format(
            task=self.context
        )


class CancelInvoiceDeleteView(TaskDeleteView):
    pass


class CancelInvoiceHtmlView(TaskHtmlView):
    label = u"Avoir"


class CancelInvoicePdfView(TaskPdfView):
    pass


class CancelInvoiceAdminView(BaseEditView):
    factory = CancelInvoice
    schema = SQLAlchemySchemaNode(CancelInvoice)


# class CancelInvoiceStatusView(CommonInvoiceStatusView):
#     """
#     Cancelinvoice specific status view
#     """
#     def post_valid_process(self, task, status, cancelinvoice):
#         """
#         Launched after a cancelinvoice has been validated
#         """
#         log.debug(u"+ post_valid_process : checking if the associated invoice \
# is resulted")
#         invoice = task.invoice
#         invoice = invoice.check_resulted(user_id=self.request.user.id)
#         self.request.dbsession.merge(invoice)
#         msg = u"L'avoir porte le numéro <b>{0}{1}</b>"
#         self.session.flash(msg.format(task.prefix, task.official_number))
#
#
# def set_financial_year(request):
#     """
#         Set the financial year of a document
#     """
#     try:
#         ret_dict = CancelInvoiceStatusView(request)()
#     except ValidationFailure, err:
#         log.exception(u"Financial year set error")
#         ret_dict = dict(
#             form=err.render(),
#             title=u"Année comptable de référence"
#         )
#     return ret_dict
#
#
# def set_products(request):
#     """
#         Set products in a document
#     """
#     try:
#         ret_dict = CancelInvoiceStatusView(request)()
#     except ValidationFailure, err:
#         log.exception(u"Error setting products")
#         ret_dict = dict(
#             form=err.render(),
#             title=u"Année comptable de référence",
#         )
#     return ret_dict


def add_routes(config):
    """
    Add module related routes
    """
    config.add_route(
        '/cancelinvoices/{id}',
        '/cancelinvoice/{id:\d+}',
        traverse='/cancelinvoices/{id}'
    )
    for extension in ('html', 'pdf'):
        config.add_route(
            '/cancelinvoices/{id}.%s' % extension,
            '/cancelinvoices/{id:\d+}.%s' % extension,
            traverse='/cancelinvoices/{id}'
        )
    for action in (
        'addfile', 'delete', 'admin',
        'set_financial_year',
        'set_products',
    ):
        config.add_route(
            '/cancelinvoices/{id}/%s' % action,
            '/cancelinvoices/{id:\d+}/%s' % action,
            traverse='/cancelinvoices/{id}'
        )


def includeme(config):
    add_routes(config)

    config.add_view(
        CancelInvoiceEditView,
        route_name='/cancelinvoices/{id}',
        renderer="tasks/edit.mako",
        permission='edit.cancelinvoice',
    )

    config.add_view(
        CancelInvoiceAdminView,
        route_name='/cancelinvoices/{id}/admin',
        renderer="base/formpage.mako",
        permission="admin",
        request_param="token=admin",
    )

    config.add_view(
        CancelInvoiceDeleteView,
        route_name='/cancelinvoices/{id}/delete',
        permission='delete.invoice',
    )

    config.add_view(
        CancelInvoicePdfView,
        route_name='/cancelinvoices/{id}.pdf',
        permission='view.cancelinvoice',
    )

    config.add_view(
        CancelInvoiceHtmlView,
        route_name='/cancelinvoices/{id}.html',
        renderer='tasks/view_only.mako',
        permission='view.cancelinvoice',
    )

    config.add_view(
        FileUploadView,
        route_name='/cancelinvoices/{id}/addfile',
        renderer='base/formpage.mako',
        permission='edit.cancelinvoice',
    )
#    config.add_view(
#        set_financial_year,
#        route_name='/cancelinvoices/{id}/set_financial_year',
#        request_param='action=set_financial_year',
#        permission="admin_treasury",
#        renderer='base/formpage.mako',
#    )
#
#    config.add_view(
#        set_products,
#        route_name='/cancelinvoices/{id}/set_products',
#        permission="admin_treasury",
#        renderer='base/formpage.mako',
#    )
