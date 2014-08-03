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
from datetime import date, datetime
from autonomie.models import (
    activity,
    user,
    workshop,
)

from autonomie.views.workshop import (
    WorkshopAddView,
    WorkshopEditView,
    record_attendances_view,
    workshop_view,
    workshop_delete_view,
)
from pyramid.events import BeforeRender
from autonomie.views.subscribers import add_api
from autonomie.tests.base import BaseFunctionnalTest


class BaseTest(BaseFunctionnalTest):
    def addOne(self):
        appstruct = {
            'name': 'Workshop',
            'leaders': ['user1', 'user2'],
            'datetime': date.today(),
            'info1': 'Header1',
        }
        w = workshop.Workshop(**appstruct)

        start = datetime(2014, 06, 12, 8)
        stop = datetime(2014, 06, 12, 12)
        timeslot = workshop.Timeslot(
            name=u'matinée',
            start_time=start,
            end_time=stop,
        )
        w.timeslots.append(timeslot)
        self.session.add(w)
        self.session.flush()
        return w

    def getOne(self):
        return workshop.Workshop.query().first()


class TestWorkshopAddView(BaseTest):
    def test_success(self):
        self.config.add_route('toto', '/toto')
        self.config.add_route('workshop', '/workshop/{id}')

        start = datetime(2014, 06, 12, 15)
        stop = datetime(2014, 06, 12, 18)

        appstruct = {
            'come_from': "/toto",
            'name': 'test',
            'info1': 'header',
            'timeslots': [{
                'name': 'timeslot',
                'start_time': start,
                'end_time': stop,
            }]
        }
        view = WorkshopAddView(self.get_csrf_request())
        result = view.submit_success(appstruct)
        a = self.getOne()

        assert a.info1 == 'header'
        assert a.timeslots[0].start_time == start
        assert a.timeslots[0].end_time == stop


class TestWorkshopEditView(BaseTest):
    def test_success(self):
        req = self.get_csrf_request()
        req.context = self.addOne()
        timeslot_id = req.context.timeslots[0].id
        start = datetime(2014, 06, 12, 15)
        stop = datetime(2014, 06, 12, 18)

        self.config.add_route('workshop', '/workshop/{id}')
        appstruct = {
            'come_from': '',
            'info2': 'subheader',
            'timeslots': [
                {
                    'name': u'Matinéee',
                    'id': timeslot_id,
                    'start_time': req.context.timeslots[0].start_time,
                    'end_time': req.context.timeslots[0].end_time,
                },
                {
                    'id': None,
                    'name': u'timeslot',
                    'start_time': start,
                    'end_time': stop,
                },
            ]
        }
        view = WorkshopEditView(req)
        result = view.submit_success(appstruct)
        a = self.getOne()

        assert a.timeslots[0].name == u'Matinéee'
        assert a.timeslots[0].start_time == datetime(2014, 06, 12, 8)

        assert a.timeslots[1].name == u'timeslot'
        assert a.info2 == 'subheader'


class TestWorkshopFuncViews(BaseTest):

    def test_workshop_view_only_view(self):
        self.config.add_route('workshop', '/workshop/{id}')
        context = self.addOne()
        request = self.get_csrf_request()
        request.user = user.User.query().first()
        result = workshop_view(context, request)
        assert result.status == '302 Found'
        assert result.location == '/workshop/{id}?action=edit'.format(
            id=context.id
        )

    def test_workshop_delete_view(self):
        self.config.add_route('workshops', '/workshops')
        request = self.get_csrf_request()
        request.referer = None
        context = self.addOne()
        result = workshop_delete_view(context, request)
        assert result.status == '302 Found'
        assert result.location == '/workshops'
        assert self.getOne() == None

#    def test_timeslot_pdf_view(self):
#        self.config.add_subscriber(add_api, BeforeRender)
#        self.config.add_static_view("static", "autonomie:static")
#        context = self.addTimeslot()
#        request = self.get_csrf_request()
#        result = timeslot_pdf_view(context, request)
#        datestr = date.today().strftime("%e_%m_%Y")
#        assert ('Content-Disposition',
#                'attachment; filename="atelier_{0}_{1}.pdf"'.format(
#                    date, timeslot_id)
#               )
