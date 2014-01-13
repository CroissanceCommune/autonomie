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

from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission
from sqlalchemy.orm import aliased

from autonomie.views.base import BaseListView
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
        ActivityListSchema,
        STATUS_OPTIONS,
        get_activity_types,
        )
from autonomie.views import render_api

log = logging.getLogger(__name__)


ACTIVITY_SUCCESS_MSG = u"L'activité a bien été programmée <a href='{0}'>Voir</a>"

class NewActivityView(BaseFormView):
    """
        View for new activity creation
        Only accessible with manage rights
    """
    title = u"Créer une nouvelle activité"
    schema = NewActivitySchema()

    def before(self, form):
        """
        By default the activity is filled with the current user as conseiller
        """
        come_from = self.request.referrer
        user = self.request.user
        appstruct = {
                'conseiller_id': user.id,
                'come_from': come_from,
                }
        form.set_appstruct(appstruct)

    def submit_success(self, appstruct):
        """
        Create the new activity object
        """
        log.debug("A new activity will be created")
        log.debug(appstruct)
        activity = Activity(status="planned")
        come_from = appstruct.pop('come_from')
        now = appstruct.pop('now', False)
        participants_ids = appstruct.pop('participants')
        appstruct['participants'] = [user.User.get(id_) \
                for id_ in participants_ids]
        merge_session_with_post(activity, appstruct)
        self.dbsession.add(activity)
        self.dbsession.flush()

        activity_url = self.request.route_path(
                        "activity",
                        id=activity.id,
                        _query=dict(action="edit")
                        )

        msg = ACTIVITY_SUCCESS_MSG.format(activity_url)

        if not self.request.is_xhr:
            self.session.flash(msg)
            if now or not come_from:
                redirect = activity_url
            else:
                redirect = come_from
            return HTTPFound(redirect)
        else:
            # On a validé un formulaire en ajax (depuis la page
            # d'accompagnement)
            return dict(message=msg)


class ActivityEdit(BaseFormView):
    """
    Activity panel : used during the activity to save datas
    """
    add_template_vars = ('title', 'next_activity_form', 'record_form',)

    schema = CreateActivitySchema()
    buttons = ()

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
        submit_url = self.request.route_path(
            "activities",
            _query=dict(action="new")
            )
        form = deform.Form(
                schema=CreateActivitySchema().bind(request=self.request),
                buttons=('submit',),
                use_ajax=True,
                counter=self.counter,
                formid="next_activity_form",
                action=submit_url,
                )
        form.set_appstruct(self.get_appstruct())
        return form.render()

    @property
    def record_form(self):
        """
            Return a form for recording the activity informations
        """
        form = deform.Form(
                schema=RecordActivitySchema().bind(request=self.request),
                buttons=(),
                counter=self.counter,
                formid="record_form",
                )
        form.set_appstruct(self.get_appstruct())
        return form.render()

    def get_appstruct(self):
        appstruct = self.request.context.appstruct()
        participants = self.request.context.participants
        appstruct['participants'] = [p.id for p in participants]
        return appstruct


    def before(self, form):
        """
        fill the form before it will be handled
        """
        self.counter = form.counter
        appstruct = self.get_appstruct()
        form.set_appstruct(appstruct)

CONSEILLER = aliased(user.User)
PARTICIPANTS = aliased(user.User)

class ActivityList(BaseListView):
    title = u"Accompagnement"
    schema = ActivityListSchema()
    sort_columns = dict(
            date=Activity.date,
            conseiller=CONSEILLER.lastname,
            )
    default_sort = 'date'
    default_direction = 'desc'

    def default_form_values(self, values):
        """
        Provide default form values for the manually rendered form
        """
        values = super(ActivityList, self).default_form_values(values)
        values['status_options'] = STATUS_OPTIONS
        values['conseiller_options'] = user.get_user_by_roles(
                ['admin',  'manager'])
        values['participants_options'] = user.User.query()
        values['type_options'] = get_activity_types()
        return values

    def query(self):
        log.debug(u"Querying activities")
        query = Activity.query()
        query = query.outerjoin(CONSEILLER, Activity.conseiller)
        query = query.outerjoin(PARTICIPANTS, Activity.participants)
        return query

    def filter_conseiller(self, query, appstruct):
        """
        Add a filter on the conseiller to the current query
        """
        conseiller_id = appstruct['conseiller_id']
        if conseiller_id != -1:
            query = query.filter(Activity.conseiller_id==conseiller_id)
        return query

    def filter_participant(self, query, appstruct):
        participant_id = appstruct['participant_id']
        if participant_id != -1:
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
    return dict(activity=request.context)


def activity_delete_view(context, request):
    """
    Deletion activity view
    """
    url = request.referer
    request.dbsession.delete(context)
    request.session.flash(u"L'activité a bien été supprimée")
    if not url:
        url = request.route_path('activities')
    return HTTPFound(url)


def includeme(config):
    """
    Add view to the pyramid registry
    """
    config.add_route(
            'activity',
            "/activities/{id:\d+}",
            traverse='/activities/{id}',
            )
    config.add_route('activities', "/activities")

    config.add_view(
            NewActivityView,
            route_name='activities',
            permission='manage',
            request_param='action=new',
            renderer="/base/formpage.mako",
            )
    config.add_view(
            NewActivityView,
            route_name='activities',
            permission='manage',
            request_param='action=new',
            xhr=True,
            renderer="/base/formajax.mako",
            )
    config.add_view(
            ActivityList,
            route_name='activities',
            permission='view',
            renderer="/activities.mako",
            )

    config.add_view(
            activity_view_only_view,
            route_name='activity',
            permission='view',
            renderer="/activity.mako",
            )

    config.add_view(
            activity_delete_view,
            route_name='activity',
            permission='manage',
            request_param='action=delete',
            )

    config.add_view(
            ActivityEdit,
            route_name='activity',
            permission='manage',
            request_param='action=edit',
            renderer="/activity_edit.mako",
            )
