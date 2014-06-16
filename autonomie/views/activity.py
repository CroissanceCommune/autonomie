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

    1- An activity is initialized with a date, a status and a conseiller
    2- An activity is filled and optionnally a new one is initialized
    3- Activities are filled
"""
import logging
import deform
import itertools

from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission
from sqlalchemy.orm import aliased

from autonomie.utils.widgets import ViewLink
from autonomie.utils.pdf import (
        render_html,
        write_pdf,
        )
from autonomie.views import BaseListView
from autonomie.views.files import FileUploadView
from autonomie.models.activity import Activity
from autonomie.models import user
from autonomie.views.forms import (
        BaseFormView,
        merge_session_with_post,
        )
from autonomie.views.forms.activity import (
        CreateActivitySchema,
        NewActivitySchema,
        RecordActivitySchema,
        get_list_schema,
        STATUS_OPTIONS,
        get_activity_types,
        )
from autonomie.views import render_api

log = logging.getLogger(__name__)


# Sqlalchemy aliases used to outerjoin two times on the same table (but through
# two different relationships
CONSEILLER = aliased(user.User)
PARTICIPANTS = aliased(user.User)


ACTIVITY_SUCCESS_MSG = u"Le rendez-vous a bien été programmé \
<a href='{0}'>Voir</a>"

NEW_ACTIVITY_BUTTON = deform.Button(
    name='submit',
    type='submit',
    title=u"Programmer")


ACTIVITY_RECORD_BUTTON = deform.Button(
    name="submit",
    type="submit",
    title=u"Enregistrer et Terminer le rendez-vous")

ACTIVITY_USER_EXCUSED = deform.Button(
    name="excused",
    type="submit",
    title=u"Participant excusé")

ACTIVITY_USER_ABSENT = deform.Button(
    name="absent",
    type="submit",
    title=u"Participant excusé")


def new_activity(request, appstruct):
    """
    Add a new activity in the database
    """
    activity = Activity(status="planned")
    participants_ids = appstruct.pop('participants', [])
    if participants_ids:
        appstruct['participants'] = [user.User.get(id_) \
            for id_ in participants_ids]
    merge_session_with_post(activity, appstruct)
    request.dbsession.add(activity)
    request.dbsession.flush()
    return activity


def record_changes(request, appstruct, message, gotolist=False):
    """
    Record changes on the current activity, changes could be :
        edition
        record
    """
    activity = merge_session_with_post(request.context, appstruct)
    request.dbsession.merge(activity)
    request.session.flash(message)
    if gotolist:
        url = request.route_path(
            'activities',
            )
    else:
        url = request.route_path(
            'activity',
            id=request.context.id,
            _query=dict(action='edit'),
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
        counter=itertools.count(start=100)
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
    appstruct['participants'] = [p.id for p in participants]
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
        come_from = self.request.referrer
        current_user = self.request.user
        appstruct = {
                'conseiller_id': current_user.id,
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
    Activity panel : used during the activity to save datas
    """
    add_template_vars = ('title',
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
        participants_list = [render_api.format_account(account)
            for account in participants]
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
            buttons=(ACTIVITY_RECORD_BUTTON,),
            counter=self.counter,
            formid="record_form",
            action=submit_url,
            )
        form.set_appstruct(self.get_appstruct())
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

    def submit_success(self, appstruct):
        """
        called when the edition form is submitted
        """
        # Retrieving participants
        participants_ids = appstruct.pop('participants', [])
        appstruct['participants'] = [user.User.get(id_) \
                for id_ in participants_ids]

        message = u"Les informations ont bien été mises à jour"
        return record_changes(self.request, appstruct, message)

    def submit_failure(self, e):
        """
        Called when we failed to submit the values
        We add a token to know if we should display the form or not
        """
        return dict(form=e.render(), formerror=True)

class ActivityRecordView(BaseFormView):
    add_template_vars = ()

    schema = RecordActivitySchema()
    buttons = (ACTIVITY_RECORD_BUTTON,)

    def submit_success(self, appstruct):
        """
        Called when the record submit button is clicked
        """
        message = u"Les informations ont bien été enregistrées"
        return record_changes(self.request, appstruct, message, gotolist=True)


class ActivityList(BaseListView):
    title = u"Rendez-vous"
    schema = get_list_schema()
    sort_columns = dict(
            date=Activity.date,
            conseiller=CONSEILLER.lastname,
            )
    default_sort = 'date'
    default_direction = 'desc'

    def query(self):
        query = Activity.query()
        query = query.outerjoin(CONSEILLER, Activity.conseiller)
        return query

    def _get_conseiller_id(self, appstruct):
        """
        Return the id of the conseiller leading the activities
        """
        return appstruct['conseiller_id']

    def filter_conseiller(self, query, appstruct):
        """
        Add a filter on the conseiller to the current query
        """
        conseiller_id = self._get_conseiller_id(appstruct)
        if conseiller_id != -1:
            query = query.filter(Activity.conseiller_id==conseiller_id)
        return query

    def filter_participant(self, query, appstruct):
        participant_id = appstruct['participant_id']
        if participant_id != -1:
            query = query.outerjoin(PARTICIPANTS, Activity.participants)
            query = query.filter(
                    Activity.participants.any(PARTICIPANTS.id==participant_id)
                    )
        return query

    def filter_type(self, query, appstruct):
        type_id = appstruct['type_id']
        if type_id != -1:
            query = query.filter(Activity.type_id == type_id)
        return query

    def filter_status(self, query, appstruct):
        status = appstruct['status']
        if status != 'all':
            query = query.filter(Activity.status==status)
        return query


class ActivityListContractor(ActivityList):
    def _get_conseiller_id(self, appstruct):
        return -1

    def filter_participant(self, query, appstruct):
        company = self.context
        participants_ids = [u.id for u in company.employees]
        query = query.outerjoin(PARTICIPANTS, Activity.participants)
        query = query.filter(
            Activity.participants.any(PARTICIPANTS.id.in_(participants_ids))
            )
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
            render_api.format_date(request.context.date),
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
    date = context.date.strftime("%e_%M_%Y")
    filename = u"rdv_{0}.pdf".format(date)

    template = u"autonomie:templates/activity_pdf.mako"
    datas = dict(activity=context)
    html_str = render_html(request, template, datas)

    write_pdf(request, filename, html_str)

    return request.response


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
    config.add_route('activities', "/activities")
    config.add_route(
            'company_activities',
            "/company/{id}/activities",
            traverse="/companies/{id}")

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
            renderer="/activities.mako",
            )

    config.add_view(
            ActivityListContractor,
            route_name='company_activities',
            permission='edit',
            renderer="/activities.mako",
            )

    config.add_view(
            activity_view_only_view,
            route_name='activity',
            permission='view',
            renderer="/activity.mako",
            )

    config.add_view(
            activity_pdf_view,
            route_name='activity.pdf',
            permission='view',
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
            renderer="/activity_edit.mako",
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
            renderer='base/formpage.mako',
            permission='manage',
            request_param='action=attach_file',
            )
