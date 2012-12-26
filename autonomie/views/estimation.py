# -*- coding: utf-8 -*-
# * File Name : estimation.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 24-04-2012
# * Last Modified :
#
# * Project :
#
"""
    Estimation views
"""
import logging
from deform import ValidationFailure
from deform import Form

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission

from autonomie.models.task.estimation import Estimation
from autonomie.models.task.estimation import EstimationLine
from autonomie.models.task.estimation import PaymentLine
from autonomie.models.task.task import DiscountLine
from autonomie.views.forms.task import get_estimation_schema
from autonomie.views.forms.task import get_estimation_appstruct
from autonomie.views.forms.task import get_estimation_dbdatas
from autonomie.utils.forms import merge_session_with_post
from autonomie.exception import Forbidden
from autonomie.views.mail import StatusChanged
from autonomie.utils.views import submit_btn
from autonomie.views.taskaction import StatusView
from autonomie.views.taskaction import TaskFormView
from autonomie.views.taskaction import make_pdf_view
from autonomie.views.taskaction import make_html_view
from autonomie.views.taskaction import make_task_delete_view
from autonomie.views.taskaction import context_is_editable
from autonomie.views.taskaction import populate_actionmenu

log = logging.getLogger(__name__)


#class EstimationView(TaskView):
#    """
#        All estimation related views
#        form
#        pdf
#        html
#    """
#    model = Estimation
#    type_ = "estimation"
#    schema = get_estimation_schema()
#    add_title = u"Nouveau devis"
#    edit_title = u"Édition du devis {task.number}"
#    route = "estimation"
#    template = "tasks/estimation.mako"
#
#    def get_dbdatas_as_dict(self):
#        """
#            Returns dbdatas as a dict of dict
#        """
#        return {'estimation': self.task.appstruct(),
#                'lines': [line.appstruct()
#                          for line in self.task.lines],
#                'discounts': [discount.appstruct()
#                              for discount in self.task.discounts],
#                'payment_lines': [line.appstruct()
#                                  for line in self.task.payment_lines]}
#
#    def is_editable(self):
#        """
#            Return True if the current task can be edited by the current user
#        """
#        if self.task.is_editable():
#            return True
#        if has_permission('manage', self.request.context, self.request):
#            if self.task.is_waiting():
#                return True
#        return False
#
#    @view_config(route_name="estimations", renderer='tasks/edit.mako',
#                permission='edit')
#    @view_config(route_name='estimation', renderer='tasks/edit.mako',
#                permission='edit')
#    def form(self):
#        """
#            Return the estimation edit view
#        """
#        if self.taskid:
#            if not self.is_editable():
#                return self.redirect_to_view_only()
#            title = self.edit_title.format(task=self.task)
#            edit = True
#            valid_msg = u"Le devis a bien été édité."
#        else:
#            title = self.add_title
#            edit = False
#            valid_msg = u"Le devis a bien été ajouté."
#
#        dbdatas = self.get_dbdatas_as_dict()
#        # Get colander's schema compatible datas
#        appstruct = get_estimation_appstruct(dbdatas)
#
#        schema = self.schema.bind(request=self.request)
#        self.request.js_require.add('address')
#        form = Form(schema, buttons=self.get_buttons(),
#                                counter=self.formcounter)
#        form.widget.template = 'autonomie:deform_templates/form.pt'
#
#        if 'submit' in self.request.params:
#            datas = self.request.params.items()
#            log.debug(u"Estimation form submission : {0}".format(datas))
#            try:
#                appstruct = form.validate(datas)
#            except ValidationFailure, e:
#                log.exception(u" - Values are not valid")
#                html_form = e.render()
#            else:
#                dbdatas = get_estimation_dbdatas(appstruct)
#                log.debug(u"Values are valid : {0}".format(dbdatas))
#                merge_session_with_post(self.task, dbdatas['estimation'])
#                if not edit:
#                    self.task.sequenceNumber = self.get_sequencenumber()
#                    self.task.name = self.get_taskname()
#                    self.task.number = self.get_tasknumber(
#                                                        self.task.taskDate)
#                try:
#                    self.request.session.flash(valid_msg, queue="main")
#                    self.task.project = self.project
#                    self.remove_lines_from_session()
#                    self.add_lines_to_task(dbdatas)
#                    self._status_process()
#                    self._set_modifications()
#                    self.request.registry.notify(StatusChanged(self.request,
#                                                    self.task))
#                    debug = " > Estimation has been added/edited succesfully"
#                    log.debug(debug)
#
#                except Forbidden, e:
#                    self.request.session.pop_flash("main")
#                    self.request.session.flash(e.message, queue='error')
#
#                # Redirecting to the project page
#                return self.project_view_redirect()
#        else:
#            html_form = form.render(appstruct)
#        return dict(title=title,
#                    company=self.company,
#                    html_form=html_form,
#                    action_menu=self.actionmenu,
#                    popups=self.popups
#                    )
#
#    def remove_lines_from_session(self):
#        """
#            Remove estimation lines and payment lines from the current session
#        """
#        # if edition we remove all estimation and payment lines
#        for line in self.task.lines:
#            self.dbsession.delete(line)
#        for line in self.task.payment_lines:
#            self.dbsession.delete(line)
#        for line in self.task.discounts:
#            self.dbsession.delete(line)
#
#    @view_config(route_name='estimation',
#                renderer='tasks/view_only.mako',
#                request_param='view=html',
#                permission='view')
#    def html(self):
#        """
#            Returns a page displaying an html rendering of the given task
#        """
#        if self.is_editable():
#            return HTTPFound(self.request.route_path(self.route,
#                                                     id=self.task.id))
#        title = u"Devis numéro : {0}".format(self.task.number)
#        return dict(
#                    title=title,
#                    task=self.task,
#                    html_datas=self._html(),
#                    action_menu=self.actionmenu,
#                    submit_buttons=self.get_buttons(),
#                    popups=self.popups
#                    )
#
#    @view_config(route_name='estimation', request_param='action=duplicate',
#            permission='edit', renderer='base/formpage.mako')
#    def duplicate(self):
#        """
#            Duplicates current estimation
#        """
#        try:
#            ret_dict = self._status()
#        except ValidationFailure, err:
#            log.exception(u"Error duplicating an estimation")
#            ret_dict = dict(html_form=err.render(),
#                    title=u"Duplication d'un document")
#        return ret_dict
#
#    def gen_invoices(self):
#        """
#            Called when an estimation status is changed
#            ( when no form is displayed : the estimation itself is not
#            editable anymore )
#        """
#        for invoice in self.task.gen_invoices(self.user.id):
#            self.dbsession.merge(invoice)
#        self.request.session.flash(u"Vos factures ont bien été générées",
#                                queue='main')
#
def add_lines_to_estimation(task, appstruct):
    """
        Add the lines to the current estimation
    """
    task.lines = []
    task.discounts = []
    task.payment_lines = []
    for line in appstruct['payment_lines']:
        task.payment_lines.append(PaymentLine(**line))
    for line in appstruct['lines']:
        task.lines.append(EstimationLine(**line))
    for line in appstruct.get('discounts', []):
        task.discounts.append(DiscountLine(**line))
    return task


class EstimationAdd(TaskFormView):
    title = "Nouveau devis"
    schema = get_estimation_schema()
    buttons = (submit_btn,)
    model = Estimation
    add_template_vars = ('title', 'company',)

    @property
    def company(self):
        # Current context is a project
        return self.context.company

    def before(self, form):
        super(EstimationAdd, self).before(form)
        populate_actionmenu(self.request)
        self.request.js_require.add('address')
        form.widget.template = "autonomie:deform_templates/form.pt"

    def submit_success(self, appstruct):
        log.debug("Submitting estimation add")
        appstruct = get_estimation_dbdatas(appstruct)
        # Next invoice number for current project
        snumber = self.context.get_next_invoice_number()

        estimation = Estimation()
        estimation.project = self.context
        estimation.owner = self.request.user
        estimation = merge_session_with_post(estimation, appstruct["estimation"])
        estimation.set_sequenceNumber(snumber)
        estimation.set_number()
        estimation.set_name()
        try:
            estimation = self.set_task_status(estimation)
            # Line handling
            estimation = add_lines_to_estimation(estimation, appstruct)
            self.dbsession.add(estimation)
            self.dbsession.flush()
            self.session.flash(u"Le devis a bien été ajoutée.")
        except Forbidden, err:
            self.request.session.flash(err.message, queue='error')
        return HTTPFound(self.request.route_path("project",
                                                 id=self.context.id))

    def set_task_status(self, estimation):
        params = dict(self.request.POST)
        status = params['submit']
        estimation.set_status(status, self.request, self.request.user.id, **params)
        self.request.registry.notify(StatusChanged(self.request, estimation))
        return estimation


class EstimationEdit(TaskFormView):
    schema = get_estimation_schema()
    buttons = (submit_btn,)
    model = Estimation
    add_template_vars = ('title', 'company',)

    @property
    def company(self):
        # Current context is an estimation
        return self.context.project.company

    @property
    def title(self):
        return u"Édition du devis {task.number}".format(task=self.context)

    def get_dbdatas_as_dict(self):
        """
            Returns dbdatas as a dict of dict
        """
        return {'estimation': self.context.appstruct(),
                'lines': [line.appstruct()
                          for line in self.context.lines],
                'discounts': [line.appstruct()
                          for line in self.context.discounts],
                'payment_lines': [line.appstruct()
                          for line in self.context.payment_lines]}

    def before(self, form):
        if not context_is_editable(self.request, self.context):
            raise HTTPFound(self.request.route_path("estimation",
                                id=self.context.id,
                                _query=dict(view='html')))

        super(EstimationEdit, self).before(form)
        populate_actionmenu(self.request)
        self.request.js_require.add('address')
        form.widget.template = "autonomie:deform_templates/form.pt"

    def appstruct(self):
        """
            Return the current edited context as a colander data model
        """
        dbdatas = self.get_dbdatas_as_dict()
        # Get colander's schema compatible datas
        return get_estimation_appstruct(dbdatas)

    def submit_success(self, appstruct):
        log.debug("Submitting estimation edit")
        appstruct = get_estimation_dbdatas(appstruct)

        # Since the call to get_next_estimation_number commits the current
        # transaction, it needs to be called before creating our estimation, to
        # avoid missing arguments errors

        estimation = self.context
        estimation = merge_session_with_post(estimation, appstruct["estimation"])
        try:
            estimation = self.set_task_status(estimation)
            # Line handling
            estimation = add_lines_to_estimation(estimation, appstruct)
            estimation = self.dbsession.merge(estimation)
            self.dbsession.flush()
            self.session.flash(u"Le devis a bien été éditée.")
        except Forbidden, err:
            self.request.session.flash(err.message, queue='error')
        return HTTPFound(self.request.route_path("project",
                                                 id=self.context.project.id))

    def set_task_status(self, estimation):
        # self.request.POST is a locked dict, we need a non locked one
        params = dict(self.request.POST)
        status = params['submit']
        estimation.set_status(status, self.request, self.request.user.id, **params)
        log.debug("Has been raised")
        self.request.registry.notify(StatusChanged(self.request, estimation))
        return estimation


class EstimationStatus(StatusView):
    """
        Handle the estimation status processing
    """

    def redirect(self):
        project_id = self.request.context.project.id
        return HTTPFound(self.request.route_path('project', id=project_id))

    def pre_geninv_process(self, task, status, params):
        """
            add a user param for invoice generation
        """
        params['user'] = self.request.user
        return params

    def post_geninv_process(self, task, status, params):
        for invoice in params:
            self.request.dbsession.merge(invoice)
        msg = u"Vos factures ont bien été générées"
        self.session.flash(msg)

    def post_aboest_process(self, task, status, params):
        msg = u"Le devis {0} a été annulé (indiqué sans suite)."
        self.session.flash(msg.format(task.number))

    def post_delete_process(self, task, status, params):
        msg = u"Le devis {0} a été supprimé"
        self.request.dbsession.delete(task)
        self.request.dbsession.flush()
        self.session.flash(msg.format(task.number))
        # Here we force redirection, nothing has to be merged
        raise self.redirect()

    def post_duplicate_process(self, task, status, params):
        estimation = params
        estimation = self.request.dbsession.merge(estimation)
        self.request.dbsession.flush()
        id_ = estimation.id
        log.debug("Post processing")
        msg = u"Le devis a bien été dupliqué, vous pouvez l'éditer \
<a href='{0}'>Ici</a>."
        msg = msg.format(self.request.route_path("estimation", id=id_))
        self.session.flash(msg)


def duplicate(request):
    """
        duplicate an invoice
    """
    try:
        ret_dict = EstimationStatus(request)()
    except ValidationFailure, err:
        log.exception(u"Duplication error")
        ret_dict = dict(html_form=err.render(),
                        title=u"Duplication d'un document")
    return ret_dict


def includeme(config):
    config.add_route('project_estimations',
                    '/projects/{id:\d+}/estimations',
                    traverse='/projects/{id}')
    config.add_route('estimation',
                     '/estimations/{id:\d+}',
                      traverse='/estimations/{id}')

    config.add_view(make_pdf_view("tasks/estimation.mako"),
                    route_name='estimation',
                    request_param='view=pdf',
                    permission='view')
    config.add_view(make_html_view(Estimation, "tasks/estimation.mako"),
                    route_name='estimation',
                    renderer='tasks/view_only.mako',
                    request_param='view=html',
                    permission='view')
    delete_msg = u"Le devis {task.number} a bien été supprimé."
    config.add_view(make_task_delete_view(delete_msg),
                    route_name='estimation',
                    request_param='action=delete',
                    permission='edit')
    config.add_view(EstimationAdd,
                    route_name="project_estimations",
                    renderer='tasks/edit.mako',
                    permission='edit')
    config.add_view(EstimationEdit,
                    route_name='estimation',
                    renderer='tasks/edit.mako',
                    permission='edit')
    config.add_view(duplicate,
                    route_name="estimation",
                    request_param='action=duplicate',
                    permission="view",
                    renderer='base/formpage.mako')

    config.add_view(EstimationStatus,
                    route_name="estimation",
                    request_param='action=status',
                    permission="edit")

