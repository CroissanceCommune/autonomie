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
from deform import Form
from pyramid.view import view_config
from pyramid.security import has_permission
from pyramid.httpexceptions import HTTPFound

from autonomie.models.model import Invoice
from autonomie.models.model import InvoiceLine
from autonomie.views.forms.task import get_invoice_schema
from autonomie.views.forms.task import get_invoice_appstruct
from autonomie.views.forms.task import get_invoice_dbdatas
from autonomie.utils.forms import merge_session_with_post
from autonomie.exception import Forbidden
from autonomie.views.mail import StatusChanged

from .base import TaskView

log = logging.getLogger(__name__)

class InvoiceView(TaskView):
    """
        All invoice related views
        form
        pdf
        html
    """
    type_ = "invoice"
    model = Invoice
    schema = get_invoice_schema()
    add_title = u"Nouvelle facture"
    edit_title = u"Édition de la facture {task.number}"
    route = "invoice"
    template = "tasks/invoice.mako"

    def set_lines(self):
        """
            set the lines attributes
        """
        self.task_lines = self.task.lines

    def get_dbdatas_as_dict(self):
        """
            Returns dbdatas as a dict of dict
        """
        return {'invoice':self.task.appstruct(),
                'lines':[line.appstruct()
                                       for line in self.task_lines],
                }

    def is_editable(self):
        """
            Return True if the current task can be edited by the current user
        """
        if self.task.is_editable():
            return True
        if has_permission('manage', self.request.context, self.request):
            if self.task.is_waiting():
                return True
        return False

    @view_config(route_name="project_invoices", renderer='tasks/edit.mako',
            permission='edit')
    @view_config(route_name='invoice', renderer='tasks/edit.mako',
            permission='edit')
    def invoice_form(self):
        """
            Return the invoice edit view
        """
        log.debug("#  Invoice Form #")
        if not self.is_editable():
            return self.redirect_to_view_only()
        if self.taskid:
            title = self.edit_title.format(task=self.task)
            edit = True
            valid_msg = u"La facture a bien été éditée."
        else:
            title = self.add_title
            edit = False
            valid_msg = u"La facture a bien été ajoutée."

        dbdatas = self.get_dbdatas_as_dict()
        # Get colander's schema compatible datas
        appstruct = get_invoice_appstruct(dbdatas)

        schema = self.schema.bind(
                                phases=self.get_phases_choice(),
                                tvas=self.get_tvas(),
                            )
        form = Form(schema, buttons=self.get_buttons(),
                counter=self.formcounter)
        form.widget.template = "autonomie:deform_templates/form.pt"

        if 'submit' in self.request.params:
            log.debug(" + Values have been submitted")
            datas = self.request.params.items()
            log.debug(datas)
            try:
                appstruct = form.validate(datas)
            except ValidationFailure, err:
                html_form = err.render()
            else:
                log.debug("  + Values are valid")
                dbdatas = get_invoice_dbdatas(appstruct)
                log.debug(dbdatas)
                merge_session_with_post(self.task, dbdatas['invoice'])
                if not edit:
                    self.task.sequenceNumber = self.get_sequencenumber()
                    self.task.name = self.get_taskname()
                    self.task.number = self.get_tasknumber(self.task.taskDate)
                try:
                    self.request.session.flash(valid_msg, queue="main")
                    self.task.project = self.project
                    self.remove_lines_from_session()
                    self.add_lines_to_task(dbdatas)
                    self._status_process()
                    self._set_modifications()
                    self.request.registry.notify(StatusChanged(self.request,
                                                    self.task))
                except Forbidden, err:
                    self.request.session.pop_flash("main")
                    self.request.session.flash(err.message, queue='error')

                # Redirecting to the project page
                return self.project_view_redirect()
        else:
            html_form = form.render(appstruct)
        return dict(title=title,
                    client=self.project.client,
                    company=self.company,
                    html_form = html_form,
                    action_menu=self.actionmenu,
                    popups=self.popups
                    )

    def remove_lines_from_session(self):
        """
            Remove invoice lines and payment lines from the current session
        """
        # if edition we remove all invoice lines
        for line in self.task.lines:
            self.dbsession.delete(line)

    def add_lines_to_task(self, dbdatas):
        """
            Add the lines to the current invoice
        """
        for line in dbdatas['lines']:
            eline = InvoiceLine()
            merge_session_with_post(eline, line)
            self.task.lines.append(eline)

    @view_config(route_name='invoice',
                renderer='tasks/view_only.mako',
                permission='view',
                request_param='view=html')
    def html(self):
        """
            Returns a page displaying an html rendering of the given task
        """
        if self.is_editable():
            return HTTPFound(self.request.route_path('invoice',
                                                id=self.task.id))
        title = u"Facture numéro : {0}".format(self.task.number)
        return dict(
                    title=title,
                    task=self.task,
                    html_datas=self._html(),
                    action_menu=self.actionmenu,
                    popups=self.popups,
                    submit_buttons=self.get_buttons(),
                    )

    @view_config(route_name='invoice',
                request_param='view=pdf',
                permission='view')
    def pdf(self):
        """
            Returns a page displaying an html rendering of the given task
        """
        return self._pdf()

    @view_config(route_name="invoice", request_param='action=status',
                permission="edit")
    def status(self):
        """
            Status change view
        """
        return self._status()

    def _post_status_process(self, status, ret_data):
        """
            Change the current task's status
        """
        if status == "valid":
            self.request.session.flash(u"La facture porte le numéro \
<b>{0}</b>".format(self.task.officialNumber), queue='main')

        elif status == 'gencinv':
            cancelinvoice = ret_data
            cancelinvoice = self.dbsession.merge(cancelinvoice)
            self.dbsession.flush()
            id_ = cancelinvoice.id
            log.debug(u"   + The cancel id : {0}".format(id_))
            self.request.session.flash(u"Un avoir a été généré, \
vous pouvez l'éditer <a href='{0}'>Ici</a>.".format(
            self.request.route_path("cancelinvoice", id=id_)), queue="main")
        elif status == "duplicate":
            invoice = ret_data
            log.debug(invoice)
            invoice = self.dbsession.merge(invoice)
            self.dbsession.flush()
            id_ = invoice.id
            log.debug(u"   + The new invoice id : {0}".format(id_))
            self.request.session.flash(u"La facture a bien été dupliquée, \
              vous pouvez l'éditer <a href='{0}'>Ici</a>."\
                   .format(self.request.route_path("invoice", id=id_)), "main")

    def _pre_status_process(self, status, params):
        """
            Validates the current payment form before setting the status
        """
        params = super(InvoiceView, self)._pre_status_process(status, params)
        if status == "paid":
            form = self._paid_form()
            appstruct = form.validate(params.items())
            log.debug("Appstruct : %s" % appstruct)
            return appstruct
        return params

    @view_config(route_name="invoice", request_param='action=payment',
                permission="manage", renderer='base/formpage.mako')
    def register_payment(self):
        """
            register_payment view
        """
        log.info(u"Registering a payment")
        try:
            ret_dict = self._status()
        except ValidationFailure, err:
            log.exception(u"An error has been detected")
            ret_dict = dict(html_form=err.render(),
                    title=u"Enregistrement d'un paiement")
        log.debug(ret_dict)
        return ret_dict

    @view_config(route_name="invoice", request_param='action=duplicate',
                permission="view", renderer='base/formpage.mako')
    def duplicate(self):
        """
            duplicate an invoice
        """
        log.info(u"Duplicating an invoice")
        try:
            ret_dict = self._status()
        except ValidationFailure, err:
            log.exception(u"An error has been detected")
            ret_dict = dict(html_form=err.render(),
                            title=u"Duplication d'un document")
        log.debug(ret_dict)
        return ret_dict
