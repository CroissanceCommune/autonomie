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
from deform import ValidationFailure
from pyramid.httpexceptions import HTTPFound

from autonomie.forms.invoices import (
    get_cancel_invoice_schema,
)
from autonomie.forms.task import (
    get_cancel_invoice_appstruct,
    get_cancel_invoice_dbdatas,
)
from autonomie.models.task import (
    CancelInvoice,
    TaskLine,
    TaskLineGroup,
)
from autonomie.forms import (
    merge_session_with_post,
)
from autonomie.views.files import FileUploadView
from autonomie.views import (
    submit_btn,
    BaseEditView,
)
from autonomie.exception import Forbidden
from autonomie.views.invoice import (
    InvoiceFormActions,
    CommonInvoiceStatusView,
)
from autonomie.views.taskaction import (
    TaskFormView,
    context_is_editable,
    populate_actionmenu,
    task_pdf_view,
    get_task_html_view,
    make_task_delete_view,
)


log = logging.getLogger(__name__)


def add_lines_to_cancelinvoice(task, appstruct):
    """
        Add the lines to the current cancelinvoice
    """
    task.default_line_group.lines = []
    task.line_groups = [task.default_line_group]
    for group in appstruct['groups']:
        lines = group.pop('lines', [])
        group = TaskLineGroup(**group)
        for line in lines:
            group.lines.append(TaskLine(**line))
        task.line_groups.append(group)

    for line in appstruct['lines']:
        task.default_line_group.lines.append(TaskLine(**line))
    return task


class CancelInvoiceAdd(TaskFormView):
    """
        Invoice Add view
    """
    title = "Nouvel avoir"
    schema = get_cancel_invoice_schema()
    buttons = (submit_btn,)
    model = CancelInvoice
    add_template_vars = ('edit', )
    form_actions_factory = InvoiceFormActions

    @property
    def company(self):
        # Current context is a project
        return self.context.company

    def before(self, form):
        super(CancelInvoiceAdd, self).before(form)
        populate_actionmenu(self.request)

    def submit_success(self, appstruct):
        log.debug("Submitting cancelinvoice add")
        appstruct = get_cancel_invoice_dbdatas(appstruct)

        # Since the call to get_next_cancelinvoice_number commits the current
        # transaction, it needs to be called before creating our cancelinvoice,
        # to avoid missing arguments errors
        snumber = self.context.get_next_cancelinvoice_number()

        cinvoice = CancelInvoice()
        cinvoice.project = self.context
        cinvoice.owner = self.request.user
        cinvoice = merge_session_with_post(
            cinvoice,
            appstruct["task"]
        )
        cinvoice.set_sequence_number(snumber)
        cinvoice.set_number()
        cinvoice.set_name()
        try:
            cinvoice = self.set_task_status(cinvoice)
            cinvoice.invoice.check_resulted(user_id=self.request.user.id)
            self.dbsession.merge(cinvoice.invoice)
            # Line handling
            cinvoice = add_lines_to_cancelinvoice(cinvoice, appstruct)
            self.dbsession.add(cinvoice)
            self.dbsession.flush()
            self.session.flash(u"L'avoir a bien été ajoutée.")
        except Forbidden, err:
            self.request.session.flash(err.message, queue='error')
        return HTTPFound(
            self.request.route_path(
                "project",
                id=self.context.id
            )
        )


class CancelInvoiceEdit(TaskFormView):
    """
        CancelInvoice edition view
        current context is an cancelinvoice
    """
    schema = get_cancel_invoice_schema()
    buttons = (submit_btn,)
    model = CancelInvoice
    edit = True
    add_template_vars = ('edit', )
    form_actions_factory = InvoiceFormActions

    @property
    def company(self):
        # Current context is an cancelinvoice
        return self.context.project.company

    @property
    def title(self):
        return u"Édition de l'avoir {task.number}".format(task=self.context)

    def before(self, form):
        if not context_is_editable(self.request, self.context):
            raise HTTPFound(
                self.request.route_path(
                    "cancelinvoice",
                    id=self.context.id,
                    _query=dict(view='html')
                )
            )

        super(CancelInvoiceEdit, self).before(form)
        populate_actionmenu(self.request)

    def appstruct(self):
        """
            Return the current edited context as a colander data model
        """
        dbdatas = self.context.__json__(self.request)
        # Get colander's schema compatible datas
        return get_cancel_invoice_appstruct(dbdatas)

    def submit_success(self, appstruct):
        log.debug("Submitting cancelinvoice edit")
        appstruct = get_cancel_invoice_dbdatas(appstruct)

        # Since the call to get_next_cancelinvoice_number commits the current
        # transaction, it needs to be called before creating our cancelinvoice,
        # to avoid missing arguments errors

        cinvoice = self.context
        cinvoice = merge_session_with_post(
            cinvoice,
            appstruct["task"]
        )
        try:
            cinvoice = self.set_task_status(cinvoice)
            cinvoice.invoice.check_resulted(user_id=self.request.user.id)
            self.dbsession.merge(cinvoice.invoice)
            # Line handling
            cinvoice = add_lines_to_cancelinvoice(cinvoice, appstruct)
            cinvoice = self.dbsession.merge(cinvoice)
            self.dbsession.flush()
            self.session.flash(u"L'avoir a bien été modifié.")
        except Forbidden, err:
            self.request.session.flash(err.message, queue='error')
        return HTTPFound(self.request.route_path("project",
                                                 id=self.context.project.id))


class CancelInvoiceStatusView(CommonInvoiceStatusView):
    """
    Cancelinvoice specific status view
    """
    def post_valid_process(self, task, status, cancelinvoice):
        """
        Launched after a cancelinvoice has been validated
        """
        log.debug(u"+ post_valid_process : checking if the associated invoice \
is resulted")
        invoice = task.invoice
        invoice = invoice.check_resulted(user_id=self.request.user.id)
        self.request.dbsession.merge(invoice)
        msg = u"L'avoir porte le numéro <b>{0}{1}</b>"
        self.session.flash(msg.format(task.prefix, task.official_number))


def set_financial_year(request):
    """
        Set the financial year of a document
    """
    try:
        ret_dict = CancelInvoiceStatusView(request)()
    except ValidationFailure, err:
        log.exception(u"Financial year set error")
        ret_dict = dict(
            form=err.render(),
            title=u"Année comptable de référence"
        )
    return ret_dict


def set_products(request):
    """
        Set products in a document
    """
    try:
        ret_dict = CancelInvoiceStatusView(request)()
    except ValidationFailure, err:
        log.exception(u"Error setting products")
        ret_dict = dict(
            form=err.render(),
            title=u"Année comptable de référence",
        )
    return ret_dict


class AdminCancelInvoice(BaseEditView):
    schema = SQLAlchemySchemaNode(CancelInvoice)


def includeme(config):
    config.add_route(
        'project_cancelinvoices',
        '/projects/{id:\d+}/cancelinvoices',
        traverse='/projects/{id}'
    )

    config.add_route(
        'cancelinvoice',
        '/cancelinvoice/{id:\d+}',
        traverse='/cancelinvoices/{id}'
    )

    config.add_view(
        task_pdf_view,
        route_name='cancelinvoice',
        request_param='view=pdf',
        permission='view',
    )

    config.add_view(
        get_task_html_view(InvoiceFormActions),
        route_name='cancelinvoice',
        renderer='tasks/view_only.mako',
        permission='view',
        request_param='view=html',
    )

    config.add_view(
        CancelInvoiceStatusView,
        route_name='cancelinvoice',
        request_param='action=status',
        permission='edit',
    )

    config.add_view(
        CancelInvoiceAdd,
        route_name="project_cancelinvoices",
        renderer="tasks/edit.mako",
        permission="edit",
    )

    config.add_view(
        CancelInvoiceEdit,
        route_name='cancelinvoice',
        renderer="tasks/edit.mako",
        permission='edit',
    )

    delete_msg = u"L'avoir {task.number} a bien été supprimé."
    config.add_view(
        make_task_delete_view(delete_msg),
        route_name='cancelinvoice',
        request_param='action=delete',
        permission='edit',
    )

    config.add_view(
        set_financial_year,
        route_name="cancelinvoice",
        request_param='action=set_financial_year',
        permission="view",
        renderer='base/formpage.mako',
    )

    config.add_view(
        set_products,
        route_name="cancelinvoice",
        request_param='action=set_products',
        permission="view",
        renderer='base/formpage.mako',
    )

    config.add_view(
        FileUploadView,
        route_name="cancelinvoice",
        renderer='base/formpage.mako',
        permission='edit',
        request_param='action=attach_file',
    )

    config.add_view(
        AdminCancelInvoice,
        route_name='cancelinvoice',
        renderer="base/formpage.mako",
        permission="admin",
        request_param="token=admin",
    )
