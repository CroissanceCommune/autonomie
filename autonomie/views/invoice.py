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
    Invoice views
"""
import logging

from colanderalchemy import SQLAlchemySchemaNode
from deform import ValidationFailure
from pyramid.httpexceptions import HTTPFound

from autonomie.exception import Forbidden
from autonomie.models.task.invoice import (
    Invoice,
    InvoiceLine,
)
from autonomie.models.task.task import DiscountLine
from autonomie.forms.task import (
    get_invoice_schema,
    get_invoice_appstruct,
    get_invoice_dbdatas,
)
from autonomie.views import (
    merge_session_with_post,
    submit_btn,
    BaseEditView,
)
from autonomie.views.files import FileUploadView
from autonomie.views.taskaction import (
    TaskFormView,
    get_paid_form,
    get_set_financial_year_form,
    get_set_products_form,
    context_is_editable,
    TaskStatusView,
    populate_actionmenu,
    task_pdf_view,
    task_html_view,
    make_task_delete_view,
)


log = logging.getLogger(__name__)


def add_lines_to_invoice(task, appstruct):
    """
        Add the lines to the current invoice
    """
    # Needed for edition only
    task.lines = []
    task.discounts = []
    for line in appstruct['lines']:
        task.lines.append(InvoiceLine(**line))
    for line in appstruct.get('discounts', []):
        task.discounts.append(DiscountLine(**line))
    return task

class InvoiceAdd(TaskFormView):
    """
        Invoice Add view
    """
    title = "Nouvelle facture"
    schema = get_invoice_schema()
    buttons = (submit_btn,)
    model = Invoice
    add_template_vars = (
        'title', 'company', 'tvas', 'load_options_url', 'edit',
    )

    @property
    def company(self):
        # Current context is a project
        return self.context.company

    def before(self, form):
        super(InvoiceAdd, self).before(form)
        populate_actionmenu(self.request)

    def submit_success(self, appstruct):
        log.debug("Submitting invoice add")
        appstruct = get_invoice_dbdatas(appstruct)

        # Since the call to get_next_invoice_number commits the current
        # transaction, it needs to be called before creating our invoice, to
        # avoid missing arguments errors
        snumber = self.context.get_next_invoice_number()

        invoice = Invoice()
        invoice.project = self.context
        invoice.owner = self.request.user
        invoice = merge_session_with_post(invoice, appstruct["invoice"])
        invoice.set_sequence_number(snumber)
        invoice.set_number()
        invoice.set_name()
        try:
            invoice = self.set_task_status(invoice)
            # Line handling
            invoice = add_lines_to_invoice(invoice, appstruct)
            self.dbsession.add(invoice)
            self.dbsession.flush()
            self.session.flash(u"La facture a bien été ajoutée.")
        except Forbidden, err:
            self.request.session.flash(err.message, queue='error')
        return HTTPFound(self.request.route_path("project",
                                                 id=self.context.id))

class InvoiceEdit(TaskFormView):
    """
        Invoice edition view
        current context is an invoice
    """
    schema = get_invoice_schema()
    buttons = (submit_btn,)
    model = Invoice
    edit = True
    add_template_vars = (
        'title', 'company', 'tvas', 'load_options_url', 'edit',
    )

    @property
    def company(self):
        # Current context is an invoice
        return self.context.project.company

    @property
    def title(self):
        return u"Édition de la facture {task.number}".format(task=self.context)

    def get_dbdatas_as_dict(self):
        """
            Returns dbdatas as a dict of dict
        """
        return {'invoice': self.context.appstruct(),
                'lines': [line.appstruct()
                          for line in self.context.lines],
                'discounts': [line.appstruct()
                              for line in self.context.discounts]}

    def before(self, form):
        if not context_is_editable(self.request, self.context):
            raise HTTPFound(self.request.route_path("invoice",
                                id=self.context.id,
                                _query=dict(view='html')))

        super(InvoiceEdit, self).before(form)
        populate_actionmenu(self.request)

    def appstruct(self):
        """
            Return the current edited context as a colander data model
        """
        dbdatas = self.get_dbdatas_as_dict()
        # Get colander's schema compatible datas
        return get_invoice_appstruct(dbdatas)

    def submit_success(self, appstruct):
        log.debug("Submitting invoice edit")
        appstruct = get_invoice_dbdatas(appstruct)

        # Since the call to get_next_invoice_number commits the current
        # transaction, it needs to be called before creating our invoice, to
        # avoid missing arguments errors

        invoice = self.context
        invoice = merge_session_with_post(invoice, appstruct["invoice"])
        try:
            invoice = self.set_task_status(invoice)
            # Line handling
            invoice = add_lines_to_invoice(invoice, appstruct)
            invoice = self.dbsession.merge(invoice)
            self.dbsession.flush()
            self.session.flash(u"La facture a bien été modifiée.")
        except Forbidden, err:
            self.request.session.flash(err.message, queue='error')
        return HTTPFound(self.request.route_path("project",
                                                 id=self.context.project.id))


class InvoiceStatus(TaskStatusView):
    """
        Handle the invoice status processing
        Is called when the status btn from the html view or
        the edit view are pressed

        context is an invoice
    """

    def redirect(self):
        project_id = self.request.context.project.id
        return HTTPFound(self.request.route_path('project', id=project_id))

    def pre_set_products_process(self, task, status, params):
        """
            Pre processed method for product configuration
        """
        log.debug(u"+ Setting products for an invoice (pre-step)")
        form = get_set_products_form(self.request)
        appstruct = form.validate(params.items())
        log.debug(appstruct)
        return appstruct

    def post_set_products_process(self, task, status, params):
        log.debug(u"+ Setting products for an invoice (post-step)")
        invoice = params
        invoice = self.request.dbsession.merge(invoice)
        log.debug(u"Configuring prodicts for invoice :{0}".format(invoice.id))
        msg = u"Les codes produits ont bien été configurés"
        msg = msg.format(self.request.route_path("invoice", id=invoice.id))
        self.request.session.flash(msg)

    def pre_gencinv_process(self, task, status, params):
        params = dict(params.items())
        params['user'] = self.request.user
        return params

    def post_gencinv_process(self, task, status, params):
        cancelinvoice = params
        cancelinvoice = self.request.dbsession.merge(cancelinvoice)
        self.request.dbsession.flush()
        id_ = cancelinvoice.id
        log.debug(u"Generated cancelinvoice {0}".format(id_))
        msg = u"Un avoir a été généré, vous pouvez le modifier \
<a href='{0}'>Ici</a>."
        msg = msg.format(self.request.route_path("cancelinvoice", id=id_))
        self.session.flash(msg)

    def post_duplicate_process(self, task, status, params):
        invoice = params
        invoice = self.request.dbsession.merge(invoice)
        self.request.dbsession.flush()
        id_ = invoice.id
        log.debug(u"Duplicated invoice : {0}".format(id_))
        msg = u"La facture a bien été dupliquée, vous pouvez le modifier \
<a href='{0}'>Ici</a>."
        msg = msg.format(self.request.route_path("invoice", id=id_))
        self.request.session.flash(msg)

    def pre_set_financial_year_process(self, task, status, params):
        """
            Handle form validation before setting the financial year of
            the current task
        """
        form = get_set_financial_year_form(self.request)
        # if an error is raised here, it will be cached a level higher
        appstruct = form.validate(params.items())
        log.debug(u" * Form has been validated")
        return appstruct

    def post_set_financial_year_process(self, task, status, params):
        invoice = params
        invoice = self.request.dbsession.merge(invoice)
        log.debug(u"Set financial year of the invoice :{0}".format(invoice.id))
        msg = u"L'année comptable de référence a bien été modifiée"
        msg = msg.format(self.request.route_path("invoice", id=invoice.id))
        self.request.session.flash(msg)

    def pre_paid_process(self, task, status, params):
        """
            Validate a payment form's data
        """
        form = get_paid_form(self.request)
        # We don't try except on the data validation, since this is done in the
        # original wrapping call (see register_payment)
        appstruct = form.validate(params.items())
        return appstruct

    def post_valid_process(self, task, status, params):
        msg = u"La facture porte le numéro <b>{0}</b>"
        self.session.flash(msg.format(task.official_number))


def register_payment(request):
    """
        register_payment view
    """
    log.info(u"'{0}' is registering a payment".format(request.user.login))
    try:
        ret_dict = InvoiceStatus(request)()
    except ValidationFailure, err:
        log.exception(u"An error has been detected")
        ret_dict = dict(form=err.render(),
                        title=u"Enregistrement d'un paiement")
    return ret_dict


def duplicate(request):
    """
        duplicate an invoice
    """
    try:
        ret_dict = InvoiceStatus(request)()
    except ValidationFailure, err:
        log.exception(u"Duplication error")
        ret_dict = dict(form=err.render(),
                        title=u"Duplication d'un document")
    return ret_dict


def set_financial_year(request):
    """
        Set the financial year of a document
    """
    try:
        ret_dict = InvoiceStatus(request)()
    except ValidationFailure, err:
        log.exception(u"Financial year set error")
        ret_dict = dict(form=err.render(),
                title=u"Année comptable de référence")
    return ret_dict


def set_products(request):
    """
        Set products in a document
    """
    try:
        ret_dict = InvoiceStatus(request)()
    except ValidationFailure, err:
        log.exception(u"Error setting products")
        ret_dict = dict(form=err.render(),
                title=u"Année comptable de référence")
    return ret_dict


class AdminInvoice(BaseEditView):
    """
    Vue pour l'administration de factures ?token=admin

    Vue accessible aux utilisateurs admin
    """
    schema = SQLAlchemySchemaNode(Invoice)


def includeme(config):
    config.add_route('project_invoices',
                     '/projects/{id:\d+}/invoices',
                     traverse='/projects/{id}')
    config.add_route('invoice',
                     '/invoices/{id:\d+}',
                     traverse='/invoices/{id}')

    delete_msg = u"La facture {task.number} a bien été supprimée."
    config.add_view(
        task_pdf_view,
        route_name='invoice',
        request_param='view=pdf',
        permission='view',
        )
    config.add_view(
        task_html_view,
        route_name='invoice',
        renderer='tasks/view_only.mako',
        permission='view',
        request_param='view=html',
        )

    config.add_view(make_task_delete_view(delete_msg),
                    route_name='invoice',
                    request_param='action=delete',
                    permission='edit')
    config.add_view(InvoiceStatus,
                    route_name='invoice',
                    request_param='action=status',
                    permission='edit')
    config.add_view(register_payment,
                    route_name="invoice",
                    request_param='action=payment',
                    permission="manage",
                    renderer='base/formpage.mako')
    config.add_view(duplicate,
                    route_name="invoice",
                    request_param='action=duplicate',
                    permission="view",
                    renderer='base/formpage.mako')
    config.add_view(set_financial_year,
                    route_name="invoice",
                    request_param='action=set_financial_year',
                    permission="view",
                    renderer='base/formpage.mako')
    config.add_view(set_products,
                    route_name="invoice",
                    request_param='action=set_products',
                    permission="view",
                    renderer='base/formpage.mako')

    config.add_view(InvoiceAdd,
                    route_name="project_invoices",
                    renderer='tasks/edit.mako',
                    permission='edit')
    config.add_view(InvoiceEdit,
                    route_name="invoice",
                    renderer='tasks/edit.mako',
                    permission='edit')

    config.add_view(
            FileUploadView,
            route_name="invoice",
            renderer='base/formpage.mako',
            permission='edit',
            request_param='action=attach_file',
            )

    config.add_view(
        AdminInvoice,
        route_name='invoice',
        renderer="base/formpage.mako",
        permission="admin",
        request_param="token=admin",
    )
