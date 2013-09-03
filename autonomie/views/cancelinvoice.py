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

from pyramid.httpexceptions import HTTPFound

from autonomie.views.forms.task import get_cancel_invoice_schema
from autonomie.views.forms.task import get_cancel_invoice_appstruct
from autonomie.views.forms.task import get_cancel_invoice_dbdatas
from autonomie.models.task.invoice import CancelInvoice
from autonomie.models.task.invoice import CancelInvoiceLine
from autonomie.utils.forms import merge_session_with_post
from autonomie.exception import Forbidden

from autonomie.utils.views import submit_btn
from autonomie.views.taskaction import TaskFormView
from autonomie.views.taskaction import context_is_editable
from autonomie.views.taskaction import TaskStatusView
from autonomie.views.taskaction import populate_actionmenu
from autonomie.views.taskaction import get_set_financial_year_form

from autonomie.views.taskaction import make_pdf_view
from autonomie.views.taskaction import make_html_view
from autonomie.views.taskaction import make_task_delete_view

log = logging.getLogger(__name__)


def add_lines_to_cancelinvoice(task, appstruct):
    """
        Add the lines to the current cancelinvoice
    """
    task.lines = []
    for line in appstruct['lines']:
        task.lines.append(CancelInvoiceLine(**line))
    return task


class CancelInvoiceAdd(TaskFormView):
    """
        Invoice Add view
    """
    title = "Nouvel avoir"
    schema = get_cancel_invoice_schema()
    buttons = (submit_btn,)
    model = CancelInvoice
    add_template_vars = ('title', 'company', 'tvas', 'load_options_url', )

    @property
    def company(self):
        # Current context is a project
        return self.context.company

    def before(self, form):
        super(CancelInvoiceAdd, self).before(form)
        populate_actionmenu(self.request)
        form.widget.template = "autonomie:deform_templates/form.pt"

    def submit_success(self, appstruct):
        log.debug("Submitting cancelinvoice add")
        appstruct = get_cancel_invoice_dbdatas(appstruct)

        # Since the call to get_next_cancelinvoice_number commits the current
        # transaction, it needs to be called before creating our cancelinvoice, to
        # avoid missing arguments errors
        snumber = self.context.get_next_cancelinvoice_number()

        cinvoice = CancelInvoice()
        cinvoice.project = self.context
        cinvoice.owner = self.request.user
        cinvoice = merge_session_with_post(cinvoice, appstruct["cancelinvoice"])
        cinvoice.set_sequenceNumber(snumber)
        cinvoice.set_number()
        cinvoice.set_name()
        try:
            cinvoice = self.set_task_status(cinvoice)
            # Line handling
            cinvoice = add_lines_to_cancelinvoice(cinvoice, appstruct)
            self.dbsession.add(cinvoice)
            self.dbsession.flush()
            self.session.flash(u"L'avoir a bien été ajoutée.")
        except Forbidden, err:
            self.request.session.flash(err.message, queue='error')
        return HTTPFound(self.request.route_path("project",
                                                 id=self.context.id))


class CancelInvoiceEdit(TaskFormView):
    """
        CancelInvoice edition view
        current context is an cancelinvoice
    """
    schema = get_cancel_invoice_schema()
    buttons = (submit_btn,)
    model = CancelInvoice
    add_template_vars = ('title', 'company', 'tvas', 'load_options_url', )

    @property
    def company(self):
        # Current context is an cancelinvoice
        return self.context.project.company

    @property
    def title(self):
        return u"Édition de l'avoir {task.number}".format(task=self.context)

    def get_dbdatas_as_dict(self):
        """
            Returns dbdatas as a dict of dict
        """
        return {'cancelinvoice': self.context.appstruct(),
                'lines': [line.appstruct()
                          for line in self.context.lines],
                'discounts': [line.appstruct()
                              for line in self.context.discounts]}

    def before(self, form):
        if not context_is_editable(self.request, self.context):
            raise HTTPFound(self.request.route_path("cancelinvoice",
                                id=self.context.id,
                                _query=dict(view='html')))

        super(CancelInvoiceEdit, self).before(form)
        populate_actionmenu(self.request)
        form.widget.template = "autonomie:deform_templates/form.pt"

    def appstruct(self):
        """
            Return the current edited context as a colander data model
        """
        dbdatas = self.get_dbdatas_as_dict()
        # Get colander's schema compatible datas
        return get_cancel_invoice_appstruct(dbdatas)

    def submit_success(self, appstruct):
        log.debug("Submitting cancelinvoice edit")
        appstruct = get_cancel_invoice_dbdatas(appstruct)

        # Since the call to get_next_cancelinvoice_number commits the current
        # transaction, it needs to be called before creating our cancelinvoice,
        # to avoid missing arguments errors

        cinvoice = self.context
        cinvoice = merge_session_with_post(cinvoice, appstruct["cancelinvoice"])
        try:
            cinvoice = self.set_task_status(cinvoice)
            # Line handling
            cinvoice = add_lines_to_cancelinvoice(cinvoice, appstruct)
            cinvoice = self.dbsession.merge(cinvoice)
            self.dbsession.flush()
            self.session.flash(u"L'avoir a bien été éditée.")
        except Forbidden, err:
            self.request.session.flash(err.message, queue='error')
        return HTTPFound(self.request.route_path("project",
                                                 id=self.context.project.id))


class CancelInvoiceStatus(TaskStatusView):

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
        cancelinvoice = params
        cancelinvoice = self.request.dbsession.merge(cancelinvoice)
        log.debug(u"Set financial year of the cancelinvoice :{0}"\
                .format(cancelinvoice.id))
        msg = u"L'année comptable de référence a bien été modifiée"
        msg = msg.format(self.request.route_path("cancelinvoice",
                                                id=cancelinvoice.id))
        self.request.session.flash(msg)

    def post_valid_process(self, task, status, params):
        msg = u"L'avoir porte le numéro <b>{0}</b>"
        self.session.flash(msg.format(task.officialNumber))


def includeme(config):
    config.add_route('project_cancelinvoices',
                    '/projects/{id:\d+}/cancelinvoices',
                    traverse='/projects/{id}')
    config.add_route('cancelinvoice',
                    '/cancelinvoice/{id:\d+}',
                    traverse='/cancelinvoices/{id}')
    delete_msg = u"L'avoir {task.number} a bien été supprimé."
    config.add_view(make_pdf_view("tasks/cancelinvoice.mako"),
                    route_name='cancelinvoice',
                    request_param='view=pdf',
                    permission='view')
    config.add_view(make_html_view(CancelInvoice, "tasks/cancelinvoice.mako"),
                route_name='cancelinvoice',
                renderer='tasks/view_only.mako',
                permission='view',
                request_param='view=html')
    config.add_view(CancelInvoiceStatus,
                    route_name='cancelinvoice',
                    request_param='action=status',
                    permission='edit')
    config.add_view(CancelInvoiceAdd,
                    route_name="project_cancelinvoices",
                    renderer="tasks/edit.mako",
                    permission="edit")
    config.add_view(CancelInvoiceEdit,
                    route_name='cancelinvoice',
                    renderer="tasks/edit.mako",
                    permission='edit')

    config.add_view(make_task_delete_view(delete_msg),
                    route_name='cancelinvoice',
                    request_param='action=delete',
                    permission='edit')




