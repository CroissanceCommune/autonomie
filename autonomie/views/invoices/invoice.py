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
from deform import Button
from deform import Form

from pyramid.httpexceptions import HTTPFound

from autonomie.models.tva import Tva
from autonomie.models.task import (
    TaskLine,
    TaskLineGroup,
    DiscountLine,
    Invoice,
)
from autonomie.models.project import (
    Phase,
    Project,
)
from autonomie.models.customer import Customer
from autonomie.utils.widgets import (
    Submit,
    PopUp,
)
from autonomie.forms.tasks.base import (
    get_new_task_schema,
)
from autonomie.forms.tasks.invoice import (
    FinancialYearSchema,
    SetProductsSchema,
    get_payment_schema,
)
from autonomie.views import (
    submit_btn,
    BaseEditView,
    BaseFormView,
    BaseView,
)
from autonomie.views.files import FileUploadView
from autonomie.views.taskaction import (
    TaskFormActions,
    TaskStatusView,
    populate_actionmenu,
    task_pdf_view,
    get_task_html_view,
    make_task_delete_view,
    context_is_task,
)


logger = log = logging.getLogger(__name__)


def get_paid_form(request, counter=None):
    """
        Return a payment form
    """
    valid_btn = Button(
        name='submit',
        value="paid",
        type='submit',
        title=u"Valider",
    )
    schema = get_payment_schema(request).bind(request=request)
    action = request.route_path(
        "/invoices/{id}/addpayment",
        id=request.context.id,
        _query=dict(action='payment')
    )
    form = Form(
        schema=schema,
        buttons=(valid_btn,),
        action=action,
        counter=counter,
    )
    return form


def get_set_products_form(request, counter=None):
    """
        Return a form used to set products reference to :
            * invoice lines
            * cancelinvoice lines
    """
    schema = SetProductsSchema().bind(request=request)
    action = request.route_path(
        "/%ss/{id}/set_products" % request.context.type_,
        id=request.context.id,
    )
    valid_btn = Button(
        name='submit',
        value="set_products",
        type='submit',
        title=u"Valider"
    )
    form = Form(schema=schema, buttons=(valid_btn,), action=action,
                counter=counter)
    return form


def get_set_financial_year_form(request, counter=None):
    """
        Return the form to set the financial year of an
        invoice or a cancelinvoice
    """
    schema = FinancialYearSchema().bind(request=request)
    action = request.route_path(
        "/%ss/{id}/set_financial_year" % request.context.type_,
        id=request.context.id,
    )
    valid_btn = Button(
        name='submit',
        value="set_financial_year",
        type='submit',
        title=u"Valider",
    )
    form = Form(
        schema=schema,
        buttons=(valid_btn,),
        action=action,
        counter=counter,
    )
    return form


def add_lines_to_invoice(task, appstruct):
    """
        Add the lines to the current invoice
    """
    # Needed for edition only
    task.default_line_group.lines = []
    task.line_groups = [task.default_line_group]
    task.discounts = []

    for group in appstruct['groups']:
        lines = group.pop('lines', [])
        group = TaskLineGroup(**group)
        for line in lines:
            group.lines.append(TaskLine(**line))
        task.line_groups.append(group)
    for line in appstruct['lines']:
        task.default_line_group.lines.append(TaskLine(**line))

    for line in appstruct.get('discounts', []):
        task.discounts.append(DiscountLine(**line))

    return task


class InvoiceFormActions(TaskFormActions):
    """
    The form actions class specific to invoices
    """

    def _set_financial_year_form(self):
        """
            Return the form for setting the financial year of a document
        """
        form = get_set_financial_year_form(self.request, self.formcounter)
        form.set_appstruct(
            {
                'financial_year': self.context.financial_year,
                'prefix': self.context.prefix,
            }
        )
        self.formcounter = form.counter
        return form

    def _set_financial_year_btn(self):
        """
            Return the button for the popup with the financial year set form
            of the current document
        """
        if context_is_task(self.context):
            title = u"Année comptable de référence"
            form = self._set_financial_year_form()
            popup = PopUp(
                "set_financial_year_form_container",
                title,
                form.render(),
            )
            self.request.popups[popup.name] = popup
            yield popup.open_btn(css='btn btn-primary')

    def _set_products_form(self):
        """
            Return the form for configuring the products for each lines
        """
        form = get_set_products_form(self.request, self.formcounter)
        form.set_appstruct(
            {
                'lines': [
                    line.appstruct() for line in self.context.all_lines
                ]
            }
        )
        self.formcounter = form.counter
        return form

    def _set_products_btn(self):
        """
            Popup fire button
        """
        title = u"Configuration des produits"
        form = self._set_products_form()
        popup = PopUp("set_products_form", title, form.render())
        self.request.popups[popup.name] = popup
        yield popup.open_btn(css='btn btn-primary')

    def _paid_form(self):
        """
            return the form for payment registration
        """
        form = get_paid_form(self.request, self.formcounter)
        appstruct = []
        for tva_value, value in self.context.topay_by_tvas().items():
            tva = Tva.by_value(tva_value)
            appstruct.append({'tva_id': tva.id, 'amount': value})
            form.set_appstruct({'tvas': appstruct})

        self.formcounter = form.counter
        return form

    def _paid_btn(self):
        """
            Return a button to set a paid btn and a select to choose
            the payment mode
        """

        if self.request.has_permission("add_payment.invoice"):
            form = self._paid_form()
            title = u"Notifier un paiement"
            popup = PopUp("paidform", title, form.render())
            self.request.popups[popup.name] = popup
            yield popup.open_btn(css='btn btn-primary')

    def _aboinv_btn(self):
        """
            Return a button to abort an invoice
        """
        yield Submit(
            u"Annuler cette facture",
            value="aboinv",
            request=self.request,
            confirm=u"Êtes-vous sûr de vouloir annuler cette facture ?"
        )

    def _gencinv_btn(self):
        """
            Return a button for generating a cancelinvoice
        """
        if self.request.context.topay() != 0:
            yield Submit(
                u"Générer un avoir",
                value="gencinv",
                request=self.request,
            )


class InvoiceAdd(BaseFormView):
    """
        Invoice Add view
    """
    title = "Nouvelle facture"
    schema = get_new_task_schema()
    buttons = (submit_btn,)

    def before(self, form):
        super(InvoiceAdd, self).before(form)
        populate_actionmenu(self.request)

    def submit_success(self, appstruct):
        log.debug("Submitting invoice add")

        name = appstruct['name']
        phase_id = appstruct['phase_id']
        phase = Phase.get(phase_id)
        project_id = appstruct['project_id']
        project = Project.get(project_id)
        customer_id = appstruct['customer_id']
        customer = Customer.get(customer_id)

        invoice = Invoice(
            self.context.company,
            customer,
            project,
            phase,
            self.request.user,
        )
        invoice.name = name
        invoice.course = appstruct['course']
        self.dbsession.add(invoice)
        self.dbsession.flush()
        return HTTPFound(
            self.request.route_path("/invoices/{id}", id=invoice.id)
        )


class InvoiceEditView(BaseView):

    @property
    def title(self):
        return u"Modification de la facture {task.name}".format(
            task=self.context
        )

    def __call__(self):
        populate_actionmenu(self.request)
        return dict(context=self.context, title=self.title)


class CommonInvoiceStatusView(TaskStatusView):
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

    def post_set_products_process(self, task, status, invoice):
        log.debug(u"+ Setting products for an invoice (post-step)")
        invoice = self.request.dbsession.merge(invoice)
        log.debug(
            u"Configuring products for {context.__name__} :{context.id}".
            format(context=invoice)
        )
        msg = u"Les codes produits ont bien été configurés"
        self.request.session.flash(msg)

    def pre_gencinv_process(self, task, status, params):
        params = dict(params.items())
        params['user'] = self.request.user
        return params

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
        log.debug(u"Set financial year and prefix of the invoice :{0}".format(
            invoice.id))
        msg = u"Le document a bien été modifié"
        msg = msg.format(self.request.route_path(
            "/invoices/{id}.html", id=invoice.id
        ))
        self.request.session.flash(msg)


class InvoiceStatusView(CommonInvoiceStatusView):
    def pre_paid_process(self, task, status, params):
        """
            Validate a payment form's data
        """
        form = get_paid_form(self.request)
        # We don't try except on the data validation, since this is done in the
        # original wrapping call (see taskaction set_status)
        appstruct = form.validate(params.items())

        if 'amount' in appstruct:
            # Les lignes de facture ne conservent pas le lien avec les objets
            # Tva, ici on en a une seule, on récupère l'objet et on le set sur
            # le amount
            appstruct['tva_id'] = Tva.by_value(
                self.context.get_tvas().keys()[0]
            ).id

        elif 'tvas' in appstruct:
            # Ce champ ne servait que pour tester las somme des valeurs saisies
            appstruct.pop('payment_amount')
            # si on a plusieurs tva :
            for tva_payment in appstruct['tvas']:
                remittance_amount = appstruct['remittance_amount']
                tva_payment['remittance_amount'] = remittance_amount
                tva_payment['date'] = appstruct['date']
                tva_payment['mode'] = appstruct['mode']
                tva_payment['bank_id'] = appstruct.get('bank_id')
                tva_payment['resulted'] = appstruct.get('resulted', False)
        else:
            raise Exception(u"On a rien à faire ici")

        logger.debug(u"In pre paid process")
        logger.debug(u"Returning : {0}".format(appstruct))
        return appstruct

    def post_valid_process(self, task, status, params):
        msg = u"La facture porte le numéro <b>{0}</b>"
        self.session.flash(msg.format(task.official_number))

    def post_gencinv_process(self, task, status, params):
        cancelinvoice = params
        cancelinvoice = self.request.dbsession.merge(cancelinvoice)
        self.request.dbsession.flush()
        id_ = cancelinvoice.id
        log.debug(u"Generated cancelinvoice {0}".format(id_))
        msg = u"Un avoir a été généré, vous pouvez le modifier \
<a href='{0}'>Ici</a>."
        msg = msg.format(
            self.request.route_path(
                "/cancelinvoices/{id}.html", id=id_
            )
        )
        self.session.flash(msg)

    def post_duplicate_process(self, task, status, params):
        invoice = params
        invoice = self.request.dbsession.merge(invoice)
        self.request.dbsession.flush()
        id_ = invoice.id
        log.debug(u"Duplicated invoice : {0}".format(id_))
        msg = u"La facture a bien été dupliquée, vous pouvez le modifier \
<a href='{0}'>Ici</a>."
        msg = msg.format(
            self.request.route_path(
                "/invoices/{id}.html", id=id_
            )
        )
        self.request.session.flash(msg)


def register_payment(request):
    """
        register_payment view
    """
    log.info(u"'{0}' is registering a payment".format(request.user.login))
    try:
        ret_dict = InvoiceStatusView(request)()
    except ValidationFailure, err:
        log.exception(u"An error has been detected")
        log.error(err.error)
        ret_dict = dict(form=err.render(),
                        title=u"Enregistrement d'un paiement")
    return ret_dict


def duplicate(request):
    """
        duplicate an invoice
    """
    try:
        ret_dict = InvoiceStatusView(request)()
    except ValidationFailure, err:
        log.exception(u"Duplication error")
        log.error(err.error)
        ret_dict = dict(form=err.render(),
                        title=u"Duplication d'un document")
    return ret_dict


def set_financial_year(request):
    """
        Set the financial year of a document
    """
    try:
        ret_dict = InvoiceStatusView(request)()
    except ValidationFailure, err:
        log.exception(u"Financial year set error")
        log.error(err.error)
        ret_dict = dict(
            form=err.render(),
            title=u"Année comptable de référence",
        )
    return ret_dict


def set_products(request):
    """
        Set products in a document
    """
    try:
        ret_dict = InvoiceStatusView(request)()
    except ValidationFailure, err:
        log.exception(u"Error setting products")
        log.error(err.error)
        ret_dict = dict(
            form=err.render(),
            title=u"Année comptable de référence",
        )
    return ret_dict


class AdminInvoice(BaseEditView):
    """
    Vue pour l'administration de factures /invoices/id/admin

    Vue accessible aux utilisateurs admin
    """
    factory = Invoice
    schema = SQLAlchemySchemaNode(Invoice)


def add_routes(config):
    """
    add module related routes
    """
    config.add_route(
        'project_invoices',
        '/projects/{id:\d+}/invoices',
        traverse='/projects/{id}'
    )

    config.add_route(
        '/invoices/{id}',
        '/invoices/{id:\d+}',
        traverse='/invoices/{id}',
    )
    for extension in ('html', 'pdf'):
        config.add_route(
            '/invoices/{id}.%s' % extension,
            '/invoices/{id:\d+}.%s' % extension,
            traverse='/invoices/{id}'
        )
    for action in (
        'addfile', 'delete', 'duplicate', 'admin',
        'set_financial_year',
        'set_products',
        'addpayment',
    ):
        config.add_route(
            '/invoices/{id}/%s' % action,
            '/invoices/{id:\d+}/%s' % action,
            traverse='/invoices/{id}'
        )


def includeme(config):
    add_routes(config)

    config.add_view(
        InvoiceAdd,
        route_name="project_invoices",
        renderer='tasks/edit.mako',
        permission='add_invoice',
    )

    # Invoice related views
    config.add_view(
        AdminInvoice,
        route_name='/invoices/{id}/admin',
        renderer="base/formpage.mako",
        permission="admin",
    )

    config.add_view(
        task_pdf_view,
        route_name='/invoices/{id}.pdf',
        permission='view.invoice',
    )

    config.add_view(
        get_task_html_view(InvoiceFormActions),
        route_name='/invoices/{id}.html',
        renderer='tasks/view_only.mako',
        permission='view.invoice',
    )

    delete_msg = u"La facture {task.name} a bien été supprimée."
    config.add_view(
        make_task_delete_view(delete_msg),
        route_name='/invoices/{id}/delete',
        permission='delete.invoice',
    )

    config.add_view(
        duplicate,
        route_name="/invoices/{id}/duplicate",
        permission="edit.invoice",
        renderer='base/formpage.mako',
    )

    config.add_view(
        set_financial_year,
        route_name="/invoices/{id}/set_financial_year",
        permission="admin_treasury",
        renderer='base/formpage.mako',
    )

    config.add_view(
        set_products,
        route_name="/invoices/{id}/set_products",
        permission="admin_treasury",
        renderer='base/formpage.mako',
    )

    config.add_view(
        register_payment,
        route_name="/invoices/{id}/addpayment",
        permission="add_payment.invoice",
        renderer='base/formpage.mako',
    )

    config.add_view(
        FileUploadView,
        route_name="/invoices/{id}/addfile",
        renderer='base/formpage.mako',
        permission='add.file',
    )

    config.add_view(
        InvoiceEditView,
        route_name="/invoices/{id}",
        renderer='tasks/form.mako',
        permission='edit.invoice',
        layout='opa'
    )
