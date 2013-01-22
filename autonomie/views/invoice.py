# -*- coding: utf-8 -*-
# * File Name : invoice.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 03-05-2012
# * Last Modified :
#
# * Project :
#
"""
    Invoice views
"""
import logging

from deform import ValidationFailure
from pyramid.security import has_permission
from pyramid.httpexceptions import HTTPFound

from autonomie.models.task.invoice import Invoice
from autonomie.models.task.invoice import InvoiceLine
from autonomie.models.task.task import DiscountLine
from autonomie.views.forms.task import get_invoice_schema
from autonomie.views.forms.task import get_invoice_appstruct
from autonomie.views.forms.task import get_invoice_dbdatas
from autonomie.utils.forms import merge_session_with_post
from autonomie.exception import Forbidden
from autonomie.views.mail import StatusChanged
from autonomie.utils.widgets import ViewLink

from autonomie.utils.views import submit_btn
from autonomie.views.taskaction import TaskFormView
from autonomie.views.taskaction import get_paid_form
from autonomie.views.taskaction import context_is_editable
from autonomie.views.taskaction import StatusView
from autonomie.views.taskaction import populate_actionmenu

from autonomie.views.taskaction import make_pdf_view
from autonomie.views.taskaction import make_html_view
from autonomie.views.taskaction import make_task_delete_view

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
    add_template_vars = ('title', 'company',)

    @property
    def company(self):
        # Current context is a project
        return self.context.company

    def before(self, form):
        super(InvoiceAdd, self).before(form)
        populate_actionmenu(self.request)
        form.widget.template = "autonomie:deform_templates/form.pt"

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
        invoice.set_sequenceNumber(snumber)
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

    def set_task_status(self, invoice):
        # self.request.POST is a locked dict, we need a non locked one
        params = dict(self.request.POST)
        status = params['submit']
        invoice.set_status(status, self.request, self.request.user.id, **params)
        self.request.registry.notify(StatusChanged(self.request, invoice))
        return invoice

class InvoiceEdit(TaskFormView):
    """
        Invoice edition view
        current context is an invoice
    """
    schema = get_invoice_schema()
    buttons = (submit_btn,)
    model = Invoice
    add_template_vars = ('title', 'company',)

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
        form.widget.template = "autonomie:deform_templates/form.pt"

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
            self.session.flash(u"La facture a bien été éditée.")
        except Forbidden, err:
            self.request.session.flash(err.message, queue='error')
        return HTTPFound(self.request.route_path("project",
                                                 id=self.context.project.id))

    def set_task_status(self, invoice):
        # self.request.POST is a locked dict, we need a non locked one
        params = dict(self.request.POST)
        status = params['submit']
        invoice.set_status(status, self.request, self.request.user.id, **params)
        log.debug("Has been raised")
        self.request.registry.notify(StatusChanged(self.request, invoice))
        return invoice


class InvoiceStatus(StatusView):
    """
        Handle the invoice status processing
        Is called when the status btn from the html view or
        the edit view are pressed

        context is an invoice
    """

    def redirect(self):
        project_id = self.request.context.project.id
        return HTTPFound(self.request.route_path('project', id=project_id))

    def post_valid_process(self, task, status, params):
        msg = u"La facture porte le numéro <b>{0}</b>"
        self.session.flash(msg.format(task.officialNumber))

    def pre_gencinv_process(self, task, status, params):
        params['user'] = self.request.user
        return params

    def post_gencinv_process(self, task, status, params):
        cancelinvoice = params
        cancelinvoice = self.request.dbsession.merge(cancelinvoice)
        self.request.dbsession.flush()
        id_ = cancelinvoice.id
        log.debug(u"Generated cancelinvoice {0}".format(id_))
        msg = u"Un avoir a été généré, vous pouvez l'éditer \
<a href='{0}'>Ici</a>."
        msg = msg.format(self.request.route_path("cancelinvoice", id=id_))
        self.session.flash(msg)

    def post_duplicate_process(self, task, status, params):
        invoice = params
        invoice = self.request.dbsession.merge(invoice)
        self.request.dbsession.flush()
        id_ = invoice.id
        log.debug(u"Duplicated invoice : {0}".format(id_))
        msg = u"La facture a bien été dupliquée, vous pouvez l'éditer \
<a href='{0}'>Ici</a>."
        msg = msg.format(self.request.route_path("invoice", id=id_))
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


def includeme(config):
    config.add_route('project_invoices',
                     '/projects/{id:\d+}/invoices',
                     traverse='/projects/{id}')
    config.add_route('invoice',
                     '/invoices/{id:\d+}',
                     traverse='/invoices/{id}')
    delete_msg = u"La facture {task.number} a bien été supprimée."
    config.add_view(make_pdf_view("tasks/invoice.mako"),
                    route_name='invoice',
                    request_param='view=pdf',
                    permission='view')
    config.add_view(make_html_view(Invoice, "tasks/invoice.mako"),
                route_name='invoice',
                renderer='tasks/view_only.mako',
                permission='view',
                request_param='view=html')

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

    config.add_view(InvoiceAdd,
                    route_name="project_invoices",
                    renderer='tasks/edit.mako',
                    permission='edit')
    config.add_view(InvoiceEdit,
                    route_name="invoice",
                    renderer='tasks/edit.mako',
                    permission='edit')
