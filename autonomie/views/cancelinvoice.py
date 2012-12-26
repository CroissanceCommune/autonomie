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
from autonomie.views.mail import StatusChanged

from autonomie.utils.views import submit_btn
from autonomie.views.taskaction import TaskFormView
from autonomie.views.taskaction import context_is_editable
from autonomie.views.taskaction import StatusView
from autonomie.views.taskaction import populate_actionmenu

from autonomie.views.taskaction import make_pdf_view
from autonomie.views.taskaction import make_html_view
from autonomie.views.taskaction import make_task_delete_view

log = logging.getLogger(__name__)


#class CancelInvoiceView(TaskView):
#    """
#        all views for cancelled invoices
#    """
#    type_ = "cancelinvoice"
#    model = CancelInvoice
#    schema = get_cancel_invoice_schema()
#    add_title = u"Nouvel avoir"
#    edit_title = u"Édition de l'avoir {task.number}"
#    route = "cancelinvoice"
#    template = "tasks/cancelinvoice.mako"
#
#    def form(self):
#        """
#            Cancel invoice add/edit
#        """
#        if self.taskid:
#            if not self.is_editable():
#                return self.redirect_to_view_only()
#            title = self.edit_title.format(task=self.task)
#            edit = True
#            valid_msg = u"L'avoir a bien été édité."
#        else:
#            title = self.add_title
#            edit = False
#            valid_msg = u"L'avoir a bien été ajouté."
#
#        #Retrieving datas
#        dbdatas = self.get_dbdatas_as_dict()
#        appstruct = appstruct = get_cancel_invoice_appstruct(dbdatas)
#
#        #Building form
#        schema = self.schema.bind(request=self.request)
#        self.request.js_require.add('address')
#        form = Form(schema, buttons=self.get_buttons())
#        form.widget.template = "autonomie:deform_templates/form.pt"
#
#        if 'submit' in self.request.params:
#            datas = self.request.params.items()
#            log.debug(u"Cancelinvoice form submission : {0}".format(datas))
#            try:
#                appstruct = form.validate(datas)
#            except ValidationFailure, e:
#                html_form = e.render()
#            else:
#                dbdatas = get_cancel_invoice_dbdatas(appstruct)
#                log.debug(u"Values are valid : {0}".format(dbdatas))
#                merge_session_with_post(self.task, dbdatas['cancelinvoice'])
#                if not edit:
#                    self.task.sequenceNumber = self.get_sequencenumber()
#                    self.task.name = self.get_taskname()
#                    self.task.number = self.get_tasknumber(self.task.taskDate)
#                try:
#                    self.request.session.flash(valid_msg, queue="main")
#                    self.task.project = self.project
#                    self.remove_lines_from_session()
#                    self.add_lines_to_task(dbdatas)
#                    self._status_process()
#                    self._set_modifications()
#                except Forbidden, e:
#                    self.request.session.pop_flash("main")
#                    self.request.session.flash(e.message, queue='error')
#
#                # Redirecting to the project page
#                return self.project_view_redirect()
#
#        else:
#            html_form = form.render(appstruct)
#        return dict(title=title,
#                    company=self.company,
#                    html_form=html_form,
#                    popups=self.popups,
#                    action_menu=self.actionmenu)
#
#    def get_dbdatas_as_dict(self):
#        """
#            Returns dbdatas as a dict of dict
#        """
#        return {'cancelinvoice': self.task.appstruct(),
#                'lines': [line.appstruct()
#                          for line in self.task.lines],
#                }
#
#    @view_config(route_name="cancelinvoice", renderer="tasks/edit.mako",
#                permission='edit')
#    @view_config(route_name="cancelinvoice", permission="edit",
#                                   request_param='action=status')
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
    add_template_vars = ('title', 'company',)

    @property
    def company(self):
        # Current context is a project
        return self.context.company

    def before(self, form):
        super(CancelInvoiceAdd, self).before(form)
        populate_actionmenu(self.request)
        self.request.js_require.add('address')
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
            self.session.flash(u"La facture a bien été ajoutée.")
        except Forbidden, err:
            self.request.session.flash(err.message, queue='error')
        return HTTPFound(self.request.route_path("project",
                                                 id=self.context.id))

    def set_task_status(self, cinvoice):
        # self.request.POST is a locked dict, we need a non locked one
        params = dict(self.request.POST)
        status = params['submit']
        cinvoice.set_status(status, self.request, self.request.user.id, **params)
        self.request.registry.notify(StatusChanged(self.request, cinvoice))
        return cinvoice


class CancelInvoiceEdit(TaskFormView):
    """
        CancelInvoice edition view
        current context is an cancelinvoice
    """
    schema = get_cancel_invoice_schema()
    buttons = (submit_btn,)
    model = CancelInvoice
    add_template_vars = ('title', 'company',)

    @property
    def company(self):
        # Current context is an cancelinvoice
        return self.context.project.company

    @property
    def title(self):
        return u"Édition de la facture {task.number}".format(task=self.context)

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
        self.request.js_require.add('address')
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
        # transaction, it needs to be called before creating our cancelinvoice, to
        # avoid missing arguments errors

        cinvoice = self.context
        cinvoice = merge_session_with_post(cinvoice, appstruct["cancelinvoice"])
        try:
            cinvoice = self.set_task_status(cinvoice)
            # Line handling
            cinvoice = add_lines_to_cancelinvoice(cinvoice, appstruct)
            cinvoice = self.dbsession.merge(cinvoice)
            self.dbsession.flush()
            self.session.flash(u"La facture a bien été éditée.")
        except Forbidden, err:
            self.request.session.flash(err.message, queue='error')
        return HTTPFound(self.request.route_path("project",
                                                 id=self.context.project.id))

    def set_task_status(self, cinvoice):
        # self.request.POST is a locked dict, we need a non locked one
        params = dict(self.request.POST)
        status = params['submit']
        cinvoice.set_status(status, self.request, self.request.user.id, **params)
        log.debug("Has been raised")
        self.request.registry.notify(StatusChanged(self.request, cinvoice))
        return cinvoice


class CancelInvoiceStatus(StatusView):
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




