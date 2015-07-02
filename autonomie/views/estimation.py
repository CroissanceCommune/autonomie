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
    Estimation views
"""
import logging
from deform import ValidationFailure

from pyramid.httpexceptions import HTTPFound

from sqlalchemy import extract
from beaker.cache import cache_region

from autonomie.exception import Forbidden
from autonomie.models.task import (
    Task,
    TaskLine,
    # TaskLineGroup,
    Estimation,
    PaymentLine,
)
from autonomie.models.task.task import DiscountLine
from autonomie.models.project import Project
from autonomie.models.customer import Customer
from autonomie.forms.task import (
    get_estimation_schema,
    get_estimation_appstruct,
    get_estimation_dbdatas,
)
from autonomie.forms.estimations import (
    get_list_schema,
)
from autonomie.forms import (
    merge_session_with_post,
)
from autonomie.views import (
    submit_btn,
    BaseListView,
)
from autonomie.views.files import FileUploadView
from autonomie.views.taskaction import (
    TaskStatusView,
    TaskFormView,
    context_is_editable,
    populate_actionmenu,
    task_pdf_view,
    task_html_view,
    make_task_delete_view,
)

log = logging.getLogger(__name__)


def add_lines_to_estimation(task, appstruct):
    """
        Add the lines to the current estimation
    """
    task.default_line_group.lines = []
    task.discounts = []
    task.payment_lines = []
    for line in appstruct['payment_lines']:
        task.payment_lines.append(PaymentLine(**line))
    for line in appstruct['lines']:
        task.default_line_group.lines.append(TaskLine(**line))
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
    add_template_vars = (
        'title', 'company', 'tvas', 'load_options_url', 'edit'
    )

    @property
    def company(self):
        # Current context is a project
        return self.context.company

    def before(self, form):
        super(EstimationAdd, self).before(form)
        populate_actionmenu(self.request)

    def submit_success(self, appstruct):
        log.debug("Submitting estimation add")
        appstruct = get_estimation_dbdatas(appstruct)
        # Next estimation number for current project
        snumber = self.context.get_next_estimation_number()

        estimation = Estimation()
        estimation.project = self.context
        estimation.owner = self.request.user
        estimation = merge_session_with_post(
            estimation,
            appstruct["estimation"]
        )
        estimation.set_sequence_number(snumber)
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
    edit = True
    add_template_vars = (
        'title', 'company', 'tvas', 'load_options_url', 'edit'
    )

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
                          for line in self.context.default_line_group.lines],
                'discounts': [line.appstruct()
                              for line in self.context.discounts],
                'payment_lines': [line.appstruct()
                                  for line in self.context.payment_lines]}

    def before(self, form):
        if not context_is_editable(self.request, self.context):
            raise HTTPFound(
                self.request.route_path(
                    "estimation",
                    id=self.context.id,
                    _query=dict(view='html')
                )
            )

        super(EstimationEdit, self).before(form)
        populate_actionmenu(self.request)

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
        estimation = merge_session_with_post(
            estimation,
            appstruct["estimation"]
        )
        try:
            estimation = self.set_task_status(estimation)
            # Line handling
            estimation = add_lines_to_estimation(estimation, appstruct)
            estimation = self.dbsession.merge(estimation)
            self.dbsession.flush()
            self.session.flash(u"Le devis a bien été modifié.")
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


def get_taskdates(dbsession):
    """
        Return all taskdates
    """
    @cache_region("long_term", "taskdates")
    def taskdates():
        """
            Cached version
        """
        return dbsession.query(Estimation.taskDate)
    return taskdates()


def get_years(dbsession):
    """
        We consider that all documents should be dated after 2000
    """
    estimations = get_taskdates(dbsession)

    @cache_region("long_term", "taskyears")
    def years():
        """
            cached version
        """
        return sorted(set([est.taskDate.year for est in estimations.all()]))
    return years()


class EstimationList(BaseListView):
    title = u""
    schema = get_list_schema()
    sort_columns = dict(
        taskDate=Estimation.taskDate,
        customer=Customer.name,
    )
    default_sort = 'taskDate'
    default_direction = 'desc'

    def query(self):
        query = Estimation.query().join(Task.project).join(Task.customer)
        company_id = self.request.context.id
        query = query.filter(Project.company_id == company_id)
        return query

    def filter_year(self, query, appstruct):
        """
            filter estimations by year
        """
        year = appstruct['year']
        query = query.filter(extract('year', Estimation.taskDate) == year)
        return query

    def filter_customer(self, query, appstruct):
        """
            filter estimations by customer
        """
        customer_id = appstruct['customer_id']
        if customer_id != -1:
            query = query.filter(Estimation.customer_id == customer_id)
        return query

    def filter_status(self, query, appstruct):
        """
            Filter estimations by status
        """
        status = appstruct['status']
        if status == 'all':
            query = query.filter(Estimation.CAEStatus.in_(
                ['valid', 'aboest', 'geninv']))
        else:
            query = query.filter(Estimation.CAEStatus == status)
        return query


def includeme(config):
    config.add_route(
        'project_estimations',
        '/projects/{id:\d+}/estimations',
        traverse='/projects/{id}',
    )
    config.add_route(
        'estimation',
        '/estimations/{id:\d+}',
        traverse='/estimations/{id}'
    )
    config.add_route(
        "estimations",
        "/company/{id:\d+}/estimations",
        traverse="/companies/{id}"
    )

    config.add_view(
        task_pdf_view,
        route_name='estimation',
        request_param='view=pdf',
        permission='view',
    )

    config.add_view(
        task_html_view,
        route_name='estimation',
        renderer='tasks/view_only.mako',
        request_param='view=html',
        permission='view',
    )

    delete_msg = u"Le devis {task.number} a bien été supprimé."
    config.add_view(
        make_task_delete_view(delete_msg),
        route_name='estimation',
        request_param='action=delete',
        permission='edit',
    )

    config.add_view(
        EstimationAdd,
        route_name="project_estimations",
        renderer='tasks/edit.mako',
        permission='edit',
    )

    config.add_view(
        EstimationEdit,
        route_name='estimation',
        renderer='tasks/edit.mako',
        permission='edit',
    )

    config.add_view(
        duplicate,
        route_name="estimation",
        request_param='action=duplicate',
        permission="view",
        renderer='base/formpage.mako',
    )

    config.add_view(
        EstimationStatus,
        route_name="estimation",
        request_param='action=status',
        permission="edit",
    )

    config.add_view(
        EstimationList,
        route_name="estimations",
        renderer="estimations.mako",
        permission="edit",
    )

    config.add_view(
        FileUploadView,
        route_name="estimation",
        renderer='base/formpage.mako',
        permission='edit',
        request_param='action=attach_file',
    )
