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

from pyramid.httpexceptions import HTTPFound

from autonomie.models.task.estimation import (
        Estimation,
        EstimationLine,
        PaymentLine,
)
from autonomie.models.task.task import DiscountLine
from autonomie.views.forms.task import (
        get_estimation_schema,
        get_estimation_appstruct,
        get_estimation_dbdatas,
)
from autonomie.views.forms import merge_session_with_post
from autonomie.exception import Forbidden
from autonomie.utils.views import submit_btn
from autonomie.views.taskaction import (
        TaskStatusView,
        TaskFormView,
        context_is_editable,
        populate_actionmenu,
        make_pdf_view,
        make_html_view,
        make_task_delete_view,
)

log = logging.getLogger(__name__)


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
    """
        Estimation add view
        context is a project
    """
    title = "Nouveau devis"
    schema = get_estimation_schema()
    buttons = (submit_btn,)
    model = Estimation
    add_template_vars = ('title', 'company', 'tvas', 'load_options_url', )

    @property
    def company(self):
        # Current context is a project
        return self.context.company

    def before(self, form):
        super(EstimationAdd, self).before(form)
        populate_actionmenu(self.request)
        form.widget.template = "autonomie:deform_templates/form.pt"

    def submit_success(self, appstruct):
        log.debug("Submitting estimation add")
        appstruct = get_estimation_dbdatas(appstruct)
        # Next estimation number for current project
        snumber = self.context.get_next_estimation_number()

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


class EstimationEdit(TaskFormView):
    """
        estimation edit view
        current context is an estimation
    """
    schema = get_estimation_schema()
    buttons = (submit_btn,)
    model = Estimation
    add_template_vars = ('title', 'company', 'tvas', 'load_options_url', )

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


class EstimationStatus(TaskStatusView):
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
        params = dict(params.items())
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
        duplicate an estimation
    """
    try:
        ret_dict = EstimationStatus(request)()
    except ValidationFailure, err:
        log.exception(u"Duplication error")
        ret_dict = dict(form=err.render(),
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

