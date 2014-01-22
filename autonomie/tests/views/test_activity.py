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
        ActivityRecordView,
        ActivityEditView,
        )
from autonomie.tests.base import BaseFunctionnalTest


class BaseTest(BaseFunctionnalTest):
    def addType(self, label='First type'):
        print "Adding a type"
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
