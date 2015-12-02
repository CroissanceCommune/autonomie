# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2014 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
"""
    Activity related views

    1- Add Edit activity metadatas
    2- Record activity attendances and datas
    3- Program a new activity
"""
import logging
import deform
import itertools

from js.deform import auto_need
from js.jquery_timepicker_addon import timepicker_fr

from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission
from sqlalchemy.orm import aliased

from autonomie.utils.widgets import ViewLink
from autonomie.utils.pdf import (
    render_html,
    write_pdf,
)
from autonomie.views import (
    BaseListView,
    BaseFormView,
)
from autonomie.forms import (
    merge_session_with_post,
)

from autonomie.views.files import FileUploadView
from autonomie.models.activity import (
    Activity,
    Attendance,
    )
from autonomie.models import (
    user,
    company,
)
from autonomie.forms.activity import (
    CreateActivitySchema,
    NewActivitySchema,
    RecordActivitySchema,
    get_list_schema,
    )
from autonomie.views import render_api

log = logging.getLogger(__name__)


CONSEILLER = aliased(user.User)

ACTIVITY_SUCCESS_MSG = u"Le rendez-vous a bien été programmé \
<a href='{0}'>Voir</a>"

NEW_ACTIVITY_BUTTON = deform.Button(
    name='submit',
    type='submit',
    title=u"Programmer")

ACTIVITY_RECORD_BUTTON = deform.Button(
    name="closed",
    type="submit",
    title=u"Enregistrer et Terminer le rendez-vous",
)

ACTIVITY_CANCEL_BUTTON = deform.Button(
    name="cancelled",
    type="submit",
    title=u"Enregistrer et Annuler le rendez-vous",
)

ACTIVITY_PDF_BUTTON = deform.Button(
    name="pdf",
    type="submit",
    title=u"Enregistrer et afficher le PDF",
)


def handle_rel_in_appstruct(appstruct):
    """
    Change related element ids in associated elements for further merge

    :param dict appstruct: The submitted dict
    """
    for (key, model) in (
        ('participants', user.User),
        ('conseillers', user.User),
        ('companies', company.Company),
    ):
        ids = set(appstruct.pop(key, []))
        if ids:
            datas = model.query().filter(model.id.in_(ids)).all()
            appstruct[key] = datas
    return appstruct


def new_activity(request, appstruct):
    """
    Add a new activity in the database
    """
    activity = Activity(status="planned")
    appstruct = handle_rel_in_appstruct(appstruct)

    merge_session_with_post(activity, appstruct)
    request.dbsession.add(activity)
    request.dbsession.flush()
    return activity


def record_changes(request, appstruct, message, gotolist=False,
                   query_options=None):
    """
    Record changes on the current activity, changes could be :
        edition
        record

    :param obj request: The pyramid request (context should be an activity)
    :param dict appstruct: The submitted datas
    :param str message: The string to display on user message
    :param bool gotolist: Should we redirect the user to the list view
    :param dict query_options: In case of single activity page redirect, add
    those options to the url
    """
    activity = merge_session_with_post(request.context, appstruct)
    request.dbsession.merge(activity)
    if message:
        request.session.flash(message)
    if gotolist:
        url = request.route_path(
            'activities',
            )
    else:
        url = request.route_path(
            "activity",
            id=request.context.id,
            _query=query_options,
            )

    return HTTPFound(url)


def _next_activity_url(request):
    """
    Return the url for the next activity form
    """
    return request.route_path('activities', _query=dict(action='new'))


def _get_next_activity_form_options(request, counter=None):
    """
    Return options needed to build the next activity form
    """
    submit_url = _next_activity_url(request)
    if counter is None:
        # To be sure we haven't id problems
        counter = itertools.count(start=100)
    return dict(
        counter=counter,
        formid="next_activity_form",
        action=submit_url,
    )


def _get_next_activity_form(request, counter):
    """
    Return the form used to configure the next activity
    """
    form = deform.Form(
        schema=CreateActivitySchema().bind(request=request),
        use_ajax=True,
        buttons=(NEW_ACTIVITY_BUTTON,),
        **_get_next_activity_form_options(request, counter)
    )
    return form


def _get_appstruct_from_activity(activity):
    """
    Return an activity as a form appstruct
    """
    appstruct = activity.appstruct()
    participants = activity.participants
    conseillers = activity.conseillers
    companies = activity.companies

    appstruct['participants'] = [p.id for p in participants]
    appstruct['conseillers'] = [c.id for c in conseillers]
    appstruct['companies'] = [c.id for c in companies]
    appstruct['attendances'] = [
        {
            'event_id': att.event_id,
            'account_id': att.account_id,
            'username': render_api.format_account(att.user),
            'status': att.status,
        } for att in activity.attendances]
    return appstruct


def populate_actionmenu(request):
    if has_permission('manage', request.context, request):
        link = ViewLink(u"Liste des rendez-vous", "manage", path="activities")
        request.actionmenu.add(link)
        link = ViewLink(
            u"Attacher un fichier",
            "manage",
            path="activity",
            id=request.context.id,
            _query=dict(action="attach_file")
        )
        request.actionmenu.add(link)
    else:
        # On doit rediriger l'utilisateur vers la liste des activités de son
        # entreprise, le problème c'est qu'on a pas l'id de celle-ci, on prend
        # donc le premier id d'entreprise qu'on trouve (c'est pas génial, mais
        # ça a le mérite de marcher)
        link = ViewLink(
            u"Liste des rendez-vous",
            "view",
            path="company_activities",
            id=request.user.companies[0].id
        )
        request.actionmenu.add(link)


class NewActivityView(BaseFormView):
    """
    View for new activity creation
    Only accessible with manage rights
    """
    title = u"Créer un nouveau rendez-vous"
    schema = NewActivitySchema()

    def before(self, form):
        """
        By default the activity is filled with the current user as conseiller
        """
        auto_need(form)
        timepicker_fr.need()
        come_from = self.request.referrer
        current_user = self.request.user
        appstruct = {
            'conseillers': [current_user.id],
            'come_from': come_from,
        }
        form.set_appstruct(appstruct)

    def submit_success(self, appstruct):
        """
        Create the new activity object
        """
        come_from = appstruct.pop('come_from')
        now = appstruct.pop('now', False)

        activity = new_activity(self.request, appstruct)

        activity_url = self.request.route_path(
            "activity",
            id=activity.id,
            _query=dict(action="edit")
        )

        if now or not come_from:
            redirect = activity_url
        else:
            msg = ACTIVITY_SUCCESS_MSG.format(activity_url)
            self.session.flash(msg)

            redirect = come_from
        return HTTPFound(redirect)


class NewActivityAjaxView(BaseFormView):
    """
    View for adding activities through ajax calls
    Simply returns a message
    """
    add_template_vars = ()
    schema = NewActivitySchema()
    use_ajax = True
    buttons = (NEW_ACTIVITY_BUTTON,)

    @property
    def form_options(self):
        form_options = _get_next_activity_form_options(self.request)
        return form_options

    def submit_success(self, appstruct):
        activity = new_activity(self.request, appstruct)
        activity_url = self.request.route_path(
            "activity",
            id=activity.id,
            _query=dict(action="edit")
        )
        form = self._get_form()
        form.set_appstruct(_get_appstruct_from_activity(activity))
        return dict(
            message=ACTIVITY_SUCCESS_MSG.format(activity_url),
            form=form.render()
        )


class ActivityEditView(BaseFormView):
    """
    Activity Edition View, entry point for activity recording, allow to modify
    metadatas, provide forms for other actions :
        recording
        program new activity
    """
    add_template_vars = (
        'title',
        'next_activity_form',
        'record_form',
    )

    schema = CreateActivitySchema()

    @property
    def title(self):
        """
        Dynamic page title
        """
        participants = self.request.context.participants
        participants_list = [
            render_api.format_account(account)
            for account in participants
        ]
        return u"Accompagnement de {0}".format(", ".join(participants_list))

    @property
    def next_activity_form(self):
        form = _get_next_activity_form(self.request, self.counter)
        form.set_appstruct(self.get_appstruct())
        return form.render()

    @property
    def record_form(self):
        """
        Return a form for recording the activity informations
        This form's submission will be handled in the ajax_submission page
        """
        submit_url = self.request.route_path(
            "activity",
            id=self.request.context.id,
            _query=dict(action="record"),
        )
        form = deform.Form(
            schema=RecordActivitySchema().bind(request=self.request),
            buttons=(
                ACTIVITY_RECORD_BUTTON,
                ACTIVITY_CANCEL_BUTTON,
                ACTIVITY_PDF_BUTTON,
            ),
            counter=self.counter,
            formid="record_form",
            action=submit_url,
        )
        form.set_appstruct(self.get_appstruct())
        auto_need(form)
        return form.render()

    def get_appstruct(self):
        return _get_appstruct_from_activity(self.request.context)

    def before(self, form):
        """
        fill the form before it will be handled
        """
        populate_actionmenu(self.request)
        self.counter = form.counter
        appstruct = self.get_appstruct()
        form.set_appstruct(appstruct)

        auto_need(form)
        timepicker_fr.need()

    def submit_success(self, appstruct):
        """
        called when the edition form is submitted
        """
        appstruct = handle_rel_in_appstruct(appstruct)

        message = u"Les informations ont bien été mises à jour"
        return record_changes(
            self.request,
            appstruct,
            message,
            query_options={'action': 'edit'}
        )


class ActivityRecordView(BaseFormView):
    """
    Allow to record an activity content (attendance and datas)
    Should only return redirect
    """
    add_template_vars = ()

    schema = RecordActivitySchema()
    buttons = (
        ACTIVITY_RECORD_BUTTON,
        ACTIVITY_CANCEL_BUTTON,
        ACTIVITY_PDF_BUTTON,
    )

    def record_attendance(self, appstruct):
        """
        Record the attendances status in both cancelled and closed activity
        """
        for datas in appstruct.pop('attendances', []):
            account_id = datas['account_id']
            event_id = datas['event_id']

            obj = Attendance.get((account_id, event_id))
            if obj is not None:
                obj.status = datas['status']
                self.dbsession.merge(obj)

    def closed_success(self, appstruct):
        """
        Called when the record submit button is clicked
        """
        message = u"Les informations ont bien été enregistrées"
        self.record_attendance(appstruct)
        self.context.status = 'closed'
        return record_changes(self.request, appstruct, message, gotolist=True)

    def cancelled_success(self, appstruct):
        """
        Called when the cancelled button is clicked
        """
        message = u"Le rendez-vous a bien été annulé"
        self.record_attendance(appstruct)
        self.context.status = 'cancelled'
        return record_changes(self.request, appstruct, message, gotolist=True)

    def pdf_success(self, appstruct):
        """
        Called when the pdf button is clicked
        """
        self.record_attendance(appstruct)
        return record_changes(
            self.request,
            appstruct,
            message=None,
            gotolist=False,
            query_options={'action': 'edit', 'show': 'pdf'},
        )


class ActivityList(BaseListView):
    title = u"Rendez-vous"
    schema = get_list_schema(is_admin=True)
    sort_columns = dict(
        datetime=Activity.datetime,
        conseiller=user.User.lastname,
    )
    default_sort = 'datetime'
    default_direction = 'desc'

    def query(self):
        query = Activity.query()
        return query

    def _get_conseiller_id(self, appstruct):
        """
        Return the id of the conseiller leading the activities
        """
        return appstruct.get('conseiller_id')

    def filter_conseiller(self, query, appstruct):
        """
        Add a filter on the conseiller to the current query
        """
        conseiller_id = self._get_conseiller_id(appstruct)
        if conseiller_id is not None:
            query = query.filter(
                Activity.conseillers.any(user.User.id == conseiller_id)
            )
        return query

    def filter_participant(self, query, appstruct):
        participant_id = appstruct.get('participant_id')

        if participant_id is not None:
            query = query.filter(
                Activity.attendances.any(
                    Attendance.account_id == participant_id
                )
                )
        return query

    def filter_user_status(self, query, appstruct):
        status = appstruct.get("user_status")
        if status is not None:
            query = query.filter(
                Activity.attendances.any(Attendance.status == status)
            )
        return query

    def filter_type(self, query, appstruct):
        type_id = appstruct.get('type_id')
        if type_id is not None:
            query = query.filter(Activity.type_id == type_id)
        return query

    def filter_status(self, query, appstruct):
        status = appstruct.get('status')

        if status is not None:
            query = query.filter(Activity.status == status)

        return query


class ActivityListContractor(ActivityList):
    """
    Activity list but for contractors
    """
    schema = get_list_schema(is_admin=False)

    def _get_conseiller_id(self, appstruct):
        return None

    def filter_participant(self, query, appstruct):
        company = self.context
        log.info("The current context : %s" % company.id)
        participants_ids = [u.id for u in company.employees]
        log.info(participants_ids)
        query = query.filter(
            Activity.attendances.any(
                Attendance.account_id.in_(participants_ids)
            )
        )
        log.debug(query)
        return query


def activity_view_only_view(context, request):
    """
    Single Activity view-only view
    """
    if has_permission('manage', context, request):
        url = request.route_path(
            'activity',
            id=context.id,
            _query=dict(action='edit'),
        )
        return HTTPFound(url)
    title = u"Rendez-vous du %s" % (
        render_api.format_datetime(request.context.datetime),
    )
    populate_actionmenu(request)
    return dict(title=title, activity=request.context)


def activity_delete_view(context, request):
    """
    Deletion activity view
    """
    url = request.referer
    request.dbsession.delete(context)
    request.session.flash(u"Le rendez-vous a bien été supprimé")
    if not url:
        url = request.route_path('activities')
    return HTTPFound(url)


def activity_pdf_view(context, request):
    """
    Return a pdf output of the current activity
    """
    from autonomie.resources import pdf_css
    pdf_css.need()
    date = context.datetime.strftime("%e_%m_%Y")
    filename = u"rdv_{0}_{1}.pdf".format(date, context.id)

    template = u"autonomie:templates/accompagnement/activity_pdf.mako"
    datas = dict(activity=context)
    html_str = render_html(request, template, datas)

    write_pdf(request, filename, html_str)

    return request.response


def activity_html_view(activity, request):
    """
    Return an html view of the current activity

        activity

            context retrieved through traversal
    """
    return dict(activity=activity)


def includeme(config):
    """
    Add view to the pyramid registry
    """
    config.add_route(
        'activity',
        "/activities/{id:\d+}",
        traverse='/activities/{id}',
    )
    config.add_route(
        'activity.pdf',
        "/activities/{id:\d+}.pdf",
        traverse='/activities/{id}',
    )
    config.add_route(
        'activity.html',
        "/activities/{id:\d+}.html",
        traverse='/activities/{id}',
    )
    config.add_route('activities', "/activities")
    config.add_route(
        'company_activities',
        "/company/{id}/activities",
        traverse="/companies/{id}",
    )

    config.add_view(
        NewActivityView,
        route_name='activities',
        permission='manage',
        request_param='action=new',
        renderer="/base/formpage.mako",
    )

    config.add_view(
        NewActivityAjaxView,
        route_name='activities',
        permission='manage',
        request_param='action=new',
        xhr=True,
        renderer="/base/formajax.mako",
    )

    config.add_view(
        ActivityList,
        route_name='activities',
        permission='manage',
        renderer="/accompagnement/activities.mako",
    )

    config.add_view(
        ActivityListContractor,
        route_name='company_activities',
        permission='edit',
        renderer="/accompagnement/activities.mako",
    )

    config.add_view(
        activity_view_only_view,
        route_name='activity',
        permission='view',
        renderer="/accompagnement/activity.mako",
    )

    config.add_view(
        activity_pdf_view,
        route_name='activity.pdf',
        permission='view',
    )

    config.add_view(
        activity_html_view,
        route_name='activity.html',
        permission='view',
        renderer='/accompagnement/activity_pdf.mako',
    )

    config.add_view(
        activity_delete_view,
        route_name='activity',
        permission='manage',
        request_param='action=delete',
    )

    config.add_view(
        ActivityEditView,
        route_name='activity',
        permission='manage',
        request_param='action=edit',
        renderer="/accompagnement/activity_edit.mako",
    )

    config.add_view(
        ActivityRecordView,
        route_name='activity',
        permission='manage',
        request_param='action=record',
        renderer="/base/formajax.mako",
    )

    config.add_view(
        FileUploadView,
        route_name="activity",
        renderer='/base/formpage.mako',
        permission='manage',
        request_param='action=attach_file',
    )
