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

import pytest
from datetime import datetime
from datetime import date
from autonomie.models.activity import (
    ActivityType,
    Activity,
)
from pyramid.events import BeforeRender
from autonomie.subscribers.before_render import add_api


def add_type(dbsession, label):
    activity_type = ActivityType(label=label)
    dbsession.add(activity_type)
    dbsession.flush()
    return activity_type.id


@pytest.fixture
def activitytype(dbsession):
    return add_type(dbsession, "First type")


@pytest.fixture
def activity(dbsession, activitytype):
    appstruct = {
        'datetime': datetime.now(),
        'type_id': activitytype,
        'mode': 'par mail',
        'name': 'test',
    }
    a = Activity(**appstruct)
    dbsession.add(a)
    dbsession.flush()
    return a


def query():
    return Activity.query().first()


def test_new_activity_success(config, activitytype, get_csrf_request_with_db):
    from autonomie.views.activity import NewActivityView
    config.add_route('toto', '/toto')
    config.add_route('activity', '/activity/{id}')
    now = datetime.now().replace(microsecond=0)
    appstruct = {
        'name': 'test',
        'come_from': "/toto",
        'datetime': now,
        'type_id': activitytype,
        'mode': 'par mail',
    }
    view = NewActivityView(get_csrf_request_with_db())
    view.submit_success(appstruct)
    a = query()
    for key, value in appstruct.items():
        assert getattr(a, key) == value


def test_newactivity_ajax_success(config, activitytype, get_csrf_request_with_db):
    from autonomie.views.activity import (
        NewActivityAjaxView,
        ACTIVITY_SUCCESS_MSG,
    )
    config.add_route('activities', '/activities')
    config.add_route('activity', '/activity/{id}')
    config.add_route('activities', '/activities')
    now = datetime.now().replace(microsecond=0)
    appstruct = {
        'datetime': now,
        'type_id': activitytype,
        'name': 'test',
        'mode': 'par mail',
    }
    view = NewActivityAjaxView(get_csrf_request_with_db())
    result = view.submit_success(appstruct)
    assert result['message'].startswith(ACTIVITY_SUCCESS_MSG[:25])
    a = query()
    for key, value in appstruct.items():
        getattr(a, key) == value



def test_activity_record_success(config, get_csrf_request_with_db, activity):
    from autonomie.views.activity import ActivityRecordView
    req = get_csrf_request_with_db()
    req.context = activity
    config.add_route('activity', '/activity/{id}')
    config.add_route('activities', '/activities')
    appstruct = {
            'point': u"Point de suivi",
            'objectifs': u"Objectifs",
            }

    view = ActivityRecordView(req)
    view.closed_success(appstruct)
    a = query()
    assert a.point == appstruct['point']
    assert a.objectifs == appstruct['objectifs']


def test_activity_edit_success(config, get_csrf_request_with_db, dbsession, activity):
    from autonomie.views.activity import ActivityEditView
    req = get_csrf_request_with_db()
    req.context = activity
    config.add_route('activity', '/activity/{id}')
    # Add another type
    type_id = add_type(dbsession, label="Second type")

    appstruct = {
            'mode': u"par téléphone",
            'type_id': type_id,
            }
    view = ActivityEditView(req)
    view.submit_success(appstruct)
    a = query()
    assert a.mode == appstruct['mode']
    assert a.type_object.label == "Second type"


def test_activity_view_only_view(config, activity, get_csrf_request_with_db):
    from autonomie.views.activity import activity_view_only_view
    config.add_route('activity', '/activity/{id}')
    request = get_csrf_request_with_db()
    result = activity_view_only_view(activity, request)
    assert result.status == '302 Found'
    assert result.location == '/activity/{id}?action=edit'.format(
            id=activity.id)


def test_activity_delete_view(config, activity, get_csrf_request_with_db):
    from autonomie.views.activity import activity_delete_view
    config.add_route('activities', '/activities')
    request = get_csrf_request_with_db()
    request.referer = None
    result = activity_delete_view(activity, request)

    assert result.status == '302 Found'
    assert result.location == '/activities'
    assert query() == None

def test_activity_delete_view_redirect(config, activity, get_csrf_request_with_db):
    from autonomie.views.activity import activity_delete_view
    config.add_route('activities', '/activities')
    request = get_csrf_request_with_db()
    request.referer = "/titi"
    result = activity_delete_view(activity, request)
    assert result.status == '302 Found'
    assert result.location == '/titi'
    assert query() == None


def test_activity_pdf_view(config, activity, get_csrf_request_with_db):
    from autonomie.views.activity import activity_pdf_view
    config.add_subscriber(add_api, BeforeRender)
    config.add_static_view("static", "autonomie:static")
    request = get_csrf_request_with_db()
    result = activity_pdf_view(activity, request)
    datestr = date.today().strftime("%e_%m_%Y")
    assert ('Content-Disposition',
            'attachment; filename="rdv_%s_%s.pdf"' % \
                (datestr, activity.id)) in  result.headerlist


