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
from datetime import date
from autonomie.models import (
        activity,
        user,
        )
from autonomie.views.activity import (
        NewActivityView,
        activity_view_only_view,
        activity_delete_view,
        activity_pdf_view,
        NewActivityAjaxView,
        ACTIVITY_SUCCESS_MSG,
        ActivityRecordView,
        ActivityEditView,
        )
from pyramid.events import BeforeRender
from autonomie.views.subscribers import add_api
from autonomie.tests.base import BaseFunctionnalTest


class BaseTest(BaseFunctionnalTest):
    def addType(self, label='First type'):
        activity_type = activity.ActivityType(label=label)
        self.session.add(activity_type)
        self.session.flush()
        return activity_type.id

    def addOne(self):
        type_id = self.addType()
        appstruct = {
                'conseiller_id': 1,
                'date': date.today(),
                'type_id': type_id,
                'mode': 'par mail',
                }
        a = activity.Activity(**appstruct)
        self.session.add(a)
        self.session.flush()
        return a

    def getOne(self):
        return activity.Activity.query().first()


class TestNewActivityView(BaseTest):
    def test_success(self):
        self.config.add_route('toto', '/toto')
        self.config.add_route('activity', '/activity/{id}')
        self.addType()
        appstruct = {
                'come_from': "/toto",
                'conseiller_id': 1,
                'date': date.today(),
                'type_id': 1,
                'mode': 'par mail',
                }
        view = NewActivityView(self.get_csrf_request())
        view.submit_success(appstruct)
        a = self.getOne()
        for key, value in appstruct.items():
            self.assertTrue(getattr(a, key) == value)


class TestNewActivityAjaxView(BaseTest):
    def test_success(self):
        self.config.add_route('activity', '/activity/{id}')
        typeid = self.addType()
        appstruct = {
                'conseiller_id': 1,
                'date': date.today(),
                'type_id': typeid,
                'mode': 'par mail',
                }
        view = NewActivityAjaxView(self.get_csrf_request())
        result = view.submit_success(appstruct)
        self.assertTrue(result['message'].startswith(ACTIVITY_SUCCESS_MSG[:25]))
        a = self.getOne()
        for key, value in appstruct.items():
            self.assertTrue(getattr(a, key) == value)



class TestActivityRecordView(BaseTest):
    def test_success(self):
        req = self.get_csrf_request()
        req.context = self.addOne()
        self.config.add_route('activity', '/activity/{id}')
        appstruct = {
                'point': u"Point de suivi",
                'objectifs': u"Objectifs",
                }

        view = ActivityRecordView(req)
        view.submit_success(appstruct)
        a = self.getOne()
        self.assertEqual(a.point, appstruct['point'])
        self.assertEqual(a.objectifs, appstruct['objectifs'])


class TestActivityEditView(BaseTest):
    def test_success(self):
        req = self.get_csrf_request()
        req.context = self.addOne()
        self.config.add_route('activity', '/activity/{id}')
        # Add another type
        type_id = self.addType(label="Second type")
        appstruct = {
                'mode': u"par téléphone",
                'type_id': type_id,
                }
        view = ActivityEditView(req)
        view.submit_success(appstruct)
        a = self.getOne()
        self.assertEqual(a.mode, appstruct['mode'])
        self.assertEqual(a.type_object.label, "Second type")


class TestActivityFuncViews(BaseTest):

    def test_activity_view_only_view(self):
        self.config.add_route('activity', '/activity/{id}')
        context = self.addOne()
        request = self.get_csrf_request()
        result = activity_view_only_view(context, request)
        assert result.status == '302 Found'
        assert result.location == '/activity/{id}?action=edit'.format(
                id=context.id)


    def test_activity_delete_view(self):
        self.config.add_route('activities', '/activities')
        request = self.get_csrf_request()
        request.referer = None
        context = self.addOne()
        result = activity_delete_view(context, request)
        assert result.status == '302 Found'
        assert result.location == '/activities'
        assert self.getOne() == None

    def test_activity_delete_view_redirect(self):
        self.config.add_route('activities', '/activities')
        request = self.get_csrf_request()
        request.referer = "/titi"
        context = self.addOne()
        result = activity_delete_view(context, request)
        assert result.status == '302 Found'
        assert result.location == '/titi'
        assert self.getOne() == None


    def test_activity_pdf_view(self):
        self.config.add_subscriber(add_api, BeforeRender)
        self.config.add_static_view("static", "autonomie:static")
        context = self.addOne()
        request = self.get_csrf_request()
        result = activity_pdf_view(context, request)
        datestr = date.today().strftime("%e_%M_%Y")
        assert ('Content-Disposition',
                'attachment; filename="rdv_%s.pdf"' % datestr) in \
                        result.headerlist


