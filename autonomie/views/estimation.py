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
import deform
import datetime

from pyramid.httpexceptions import HTTPFound

from sqlalchemy import (
    extract,
    distinct,
)
from beaker.cache import cache_region

from autonomie.exception import Forbidden
from autonomie.models.task import (
    Task,
    TaskLine,
    TaskLineGroup,
    Estimation,
    PaymentLine,
)
from autonomie.models.task.task import DiscountLine
from autonomie.models.customer import Customer
from autonomie.models.company import Company
from autonomie.utils.widgets import (
    Submit,
)
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
    TaskFormActions,
    TaskFormView,
    context_is_editable,
    populate_actionmenu,
    task_pdf_view,
    get_task_html_view,
    make_task_delete_view,
)

log = logger = logging.getLogger(__name__)


def add_lines_to_estimation(task, appstruct):
    """
        Add the lines to the current estimation
    """
    task.default_line_group.lines = []
    task.line_groups = [task.default_line_group]
    task.discounts = []
    task.payment_lines = []

    for line in appstruct['payment_lines']:
        task.payment_lines.append(PaymentLine(**line))

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


class EstimationFormActions(TaskFormActions):
    """
    estimation specific form actions buttons and forms
    """
    def _aboest_btn(self):
        """
            Return a button to abort an estimation
        """
        yield Submit(u"Indiquer sans suite",
                     title=u"Indiquer que le devis n'aura pas de suite",
                     value="aboest",
                     request=self.request)

    def _geninv_btn(self):
        """
            Return a button for invoice generation
        """
        if not self.context.invoices:
            yield Submit(
                u"Générer les factures",
                title=u"Générer les factures correspondantes au devis",
                value="geninv",
                request=self.request,
            )
        else:
            yield Submit(
                u"Re-générer les factures",
                title=u"Re-générer les factures correspondantes au devis",
                value="geninv",
                request=self.request,
                confirm=u"Êtes-vous sûr de vouloir re-générer des factures \
pour ce devis ?"
            )


class EstimationAdd(TaskFormView):
    """
        Estimation add view
        context is a project
    """
    title = "Nouveau devis"
    schema = get_estimation_schema()
    buttons = (submit_btn,)
    model = Estimation
    form_actions_factory = EstimationFormActions

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

        customer_id = appstruct["task"]['customer_id']
        customer = Customer.get(customer_id)

        estimation = Estimation(
            self.context.company,
            customer,
            self.context,
            self.context.phases[0],
            self.request.user,
        )
        estimation = merge_session_with_post(
            estimation,
            appstruct['task']
        )
        try:
            # Line handling
            estimation = add_lines_to_estimation(estimation, appstruct)
            self.dbsession.add(estimation)
            self.dbsession.flush()
            estimation = self.set_task_status(estimation)
            self.session.flash(u"Le devis a bien été ajouté.")
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
    add_template_vars = ('edit', )
    form_actions_factory = EstimationFormActions

    @property
    def company(self):
        # Current context is an estimation
        return self.context.project.company

    @property
    def title(self):
        return u"Édition du devis {task.name}".format(task=self.context)

    def before(self, form):
        if not context_is_editable(self.request):
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
        dbdatas = self.context.__json__(self.request)
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
            appstruct['task']
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
        prefix = self.request.config.get('invoiceprefix', '')
        for invoice in params:
            invoice.prefix = prefix
            self.request.dbsession.merge(invoice)
        msg = u"Vos factures ont bien été générées"
        self.session.flash(msg)

    def post_aboest_process(self, task, status, params):
        msg = u"Le devis {0} a été annulé (indiqué sans suite)."
        self.session.flash(msg.format(task.name))

    def post_delete_process(self, task, status, params):
        msg = u"Le devis {0} a été supprimé"
        self.request.dbsession.delete(task)
        self.request.dbsession.flush()
        self.session.flash(msg.format(task.name))
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
    except deform.ValidationFailure, err:
        log.exception(u"Duplication error")
        ret_dict = dict(form=err.render(),
                        title=u"Duplication d'un document")
    return ret_dict


def get_years(dbsession):
    """
        We consider that all documents should be dated after 2000
    """
    @cache_region("long_term", "taskyears")
    def years():
        """
            cached version
        """
        query = dbsession.query(extract('year', Estimation.date)).distinct()
        years = list(query)
        return sorted(years)
    return years()


class GlobalEstimationList(BaseListView):
    title = u""
    add_template_vars = (u'title', 'is_admin',)
    schema = get_list_schema(is_global=True)
    sort_columns = dict(
        date=Estimation.date,
        customer=Customer.name,
        company=Company.name,
    )
    default_sort = 'date'
    default_direction = 'desc'
    is_admin = True

    def query(self):
        query = self.request.dbsession.query(
            distinct(Estimation.id),
            Estimation.name,
            Estimation.internal_number,
            Estimation.CAEStatus,
            Estimation.date,
            Estimation.description,
            Estimation.ht,
            Estimation.tva,
            Estimation.ttc,
            Customer.id,
            Customer.name,
            Company.id,
            Company.name
        )
        query = query.outerjoin(Task.company)
        query = query.outerjoin(Task.customer)
        return query

    def filter_date(self, query, appstruct):
        period = appstruct.get('period', {})
        if period.get('start'):
            start = period.get('start')
            end = period.get('end')
            if end is None:
                end = datetime.date.today()
            query = query.filter(Task.date.between(start, end))
        else:
            year = appstruct.get('year')
            if year is not None:
                query = query.filter(extract('year', Estimation.date) == year)
        return query

    def _get_company_id(self, appstruct):
        return appstruct.get('company_id')

    def filter_company(self, query, appstruct):
        company_id = self._get_company_id(appstruct)
        if company_id is not None:
            query = query.filter(Task.company_id == company_id)
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

    def more_template_vars(self, response_dict):
        """
        Add template vars to the response dict

        :param obj result: A Sqla Query
        :returns: vars to pass to the template
        :rtype: dict
        """
        ret_dict = BaseListView.more_template_vars(self, response_dict)
        records = response_dict['records']
        ret_dict['totalht'] = sum(r[6] for r in records)
        ret_dict['totaltva'] = sum(r[7] for r in records)
        ret_dict['totalttc'] = sum(r[8] for r in records)
        return ret_dict


class EstimationList(GlobalEstimationList):
    schema = get_list_schema(is_global=False)
    is_admin = False

    def _get_company_id(self, appstruct):
        """
        Return the current context's company id
        """
        return self.request.context.id


def add_routes(config):
    """
    Add module's specific routes
    """
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
        "company_estimations",
        "/company/{id:\d+}/estimations",
        traverse="/companies/{id}"
    )
    config.add_route(
        "estimations",
        "/estimations",
    )


def includeme(config):
    add_routes(config)

    config.add_view(
        EstimationAdd,
        route_name="project_estimations",
        renderer='tasks/edit.mako',
        permission='add_estimation',
    )

    config.add_view(
        EstimationEdit,
        route_name='estimation',
        renderer='tasks/edit.mako',
        permission='edit_estimation',
    )

    config.add_view(
        EstimationList,
        route_name="company_estimations",
        renderer="estimations.mako",
        permission="list_estimations",
    )

    config.add_view(
        GlobalEstimationList,
        route_name="estimations",
        renderer="estimations.mako",
        permission="admin_tasks",
    )

    delete_msg = u"Le devis {task.name} a bien été supprimé."
    config.add_view(
        make_task_delete_view(delete_msg),
        route_name='estimation',
        request_param='action=delete',
        permission='delete_estimation',
    )

    config.add_view(
        duplicate,
        route_name="estimation",
        request_param='action=duplicate',
        permission="edit_estimation",
        renderer='base/formpage.mako',
    )

    config.add_view(
        EstimationStatus,
        route_name="estimation",
        request_param='action=status',
        permission="edit_estimation",
    )

    config.add_view(
        task_pdf_view,
        route_name='estimation',
        request_param='view=pdf',
        permission='view_estimation',
    )

    config.add_view(
        get_task_html_view(EstimationFormActions),
        route_name='estimation',
        renderer='tasks/view_only.mako',
        request_param='view=html',
        permission='view_estimation',
    )

    config.add_view(
        FileUploadView,
        route_name="estimation",
        renderer='base/formpage.mako',
        permission='edit_estimation',
        request_param='action=attach_file',
    )
