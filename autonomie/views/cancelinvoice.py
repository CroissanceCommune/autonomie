# -*- coding: utf-8 -*-
# * File Name : cancelinvoice.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 19-06-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    View for assets
"""
import logging

from deform import Form

from pyramid.view import view_config
from deform import ValidationFailure
from pyramid.httpexceptions import HTTPFound

from autonomie.views.forms.task import get_cancel_invoice_schema
from autonomie.views.forms.task import get_cancel_invoice_appstruct
from autonomie.views.forms.task import get_cancel_invoice_dbdatas
from autonomie.models.model import CancelInvoice
from autonomie.models.model import CancelInvoiceLine
from autonomie.utils.forms import merge_session_with_post
from autonomie.utils.exception import Forbidden

from .base import TaskView
log = logging.getLogger(__name__)

class CancelInvoiceView(TaskView):
    """
        all views for cancelled invoices
    """
    type_ = "cancelinvoice"
    model = CancelInvoice
    schema = get_cancel_invoice_schema()
    add_title = u"Nouvel avoir"
    edit_title = u"Édition de l'avoir {task.number}"
    route = "cancelinvoice"
    template = "tasks/cancelinvoice.mako"

    @view_config(route_name="cancelinvoices",
                 renderer="tasks/edit.mako",
                 permission="manage")
    @view_config(route_name="cancelinvoice", renderer="tasks/edit.mako",
                permission='manage')
    def form(self):
        """
            Cancel invoice add/edit
        """
        if not self.is_editable():
            return self.redirect_to_view_only()
        log.debug("# CancelInvoice Form #")
        if self.taskid:
            title = self.edit_title.format(task=self.task)
            edit = True
            valid_msg = u"L'avoir a bien été édité."
        else:
            title = self.add_title
            edit = False
            valid_msg = u"L'avoir a bien été ajouté."

        #Retrieving datas
        dbdatas = self.get_dbdatas_as_dict()
        appstruct = appstruct = get_cancel_invoice_appstruct(dbdatas)

        #Building form
        schema = self.schema.bind(phases=self.get_phases_choice(),
                                  tvas=self.get_tvas(),
                                  tasktype='cancelinvoice')
        form = Form(schema, buttons=self.get_buttons())
        form.widget.template = "autonomie:deform_templates/form.pt"

        if 'submit' in self.request.params:
            log.debug(" + Values have been submitted")
            datas = self.request.params.items()
            log.debug(datas)
            try:
                appstruct = form.validate(datas)
            except ValidationFailure, e:
                html_form = e.render()
            else:
                log.debug("  + Values are valid")
                dbdatas = get_cancel_invoice_dbdatas(appstruct)
                log.debug(dbdatas)
                merge_session_with_post(self.task, dbdatas['cancelinvoice'])
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
                except Forbidden, e:
                    self.request.session.pop_flash("main")
                    self.request.session.flash(e.message, queue='error')

                # Redirecting to the project page
                return self.project_view_redirect()

        else:
            html_form = form.render(appstruct)
        return dict(title=title,
                    client=self.project.client,
                    company=self.company,
                    html_form=html_form,
                    action_menu=self.actionmenu)

    def is_editable(self):
        """
            Return True if the current task can be edited by the current user
        """
        return self.task.is_editable()

    def set_lines(self):
        """
            set the lines
        """
        self.task_lines = self.task.lines

    def get_dbdatas_as_dict(self):
        """
            Returns dbdatas as a dict of dict
        """
        return {'cancelinvoice':self.task.appstruct(),
                'lines':[line.appstruct()
                            for line in self.task_lines],
                }

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
            eline = CancelInvoiceLine()
            merge_session_with_post(eline, line)
            self.task.lines.append(eline)

    @view_config(route_name='cancelinvoice',
                 renderer='tasks/view_only.mako',
                 request_param='view=html',
                 permission='view')
    def html(self):
        """
            Html output of the document
        """
        if self.is_editable():
            return HTTPFound(self.request.route_path(self.route,
                                                    id=self.task.id))
        title = u"Avoir numéro : {0}".format(self.task.number)
        return dict(title=title,
                    task=self.task,
                    html_datas=self._html(),
                    action_menu=self.actionmenu,
                    submit_buttons=self.get_buttons())

    @view_config(route_name='cancelinvoice',
                    request_param='view=pdf',
                    permission='view')
    def pdf(self):
        """
            Returns a pdf displaying the given task
        """
        return self._pdf()

    @view_config(route_name="cancelinvoice", permission="manage",
                                   request_param='action=status')
    def status(self):
        """
            Status change view
        """
        return self._status()

    def _post_status_process(self, status):
        """
            post status process
        """
        if status == "valid":
            self.task.valid_callback()
            self.request.session.flash(u"L'avoir porte le numéro \
<b>{0}</b>".format(self.task.officialNumber), queue='main')

        elif status == 'paid':
            paymentMode = self.request.params.get('paymentMode')
            self.task.paymentMode = paymentMode

    def _can_change_status(self, status):
        """
            Handle the permissions on status change depending on actual
            permission
        """
        return True
