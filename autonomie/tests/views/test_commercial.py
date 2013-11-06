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
    Test the commercial handling module
"""
from datetime import date
from mock import Mock
from autonomie.views.commercial import compute_turnover_difference
from autonomie.views.commercial import DisplayCommercialHandling
from autonomie.models.treasury import TurnoverProjection

from autonomie.tests.base import BaseFunctionnalTest

APPSTRUCT = {'month':11, 'value':'1500', 'comment':"Some comments go here"}

class TestCommercial(BaseFunctionnalTest):
    def addOne(self, year=None):
        self.config.add_route('commercial_handling', '/')
        req = self.get_csrf_request()
        if year:
            req.GET = {'year':year}
        view = DisplayCommercialHandling(req)
        view.submit_success(APPSTRUCT)

    def getOne(self):
        try:
            return TurnoverProjection.query().first()
        except:
            return None

    def get_csrf_request(self, post={}):
        req = super(TestCommercial, self).get_csrf_request(post)
        req.context = Mock(id=1)
        return req

    def test_compute_turnover_difference(self):
        index = 0
        projections = {}
        turnovers = {}
        self.assertEqual(None, compute_turnover_difference(index,
                                                  projections, turnovers))
        p = Mock(value=10)
        projections = {0:p}
        turnovers = {0:10}
        self.assertEqual(None, compute_turnover_difference(1, projections, turnovers))
        self.assertEqual(0, compute_turnover_difference(0, projections, turnovers))


    def test_submit_year(self):
        req = self.get_csrf_request()
        req.GET = {'year':'2010'}
        view = DisplayCommercialHandling(req)
        self.assertEqual(view.submit_year(), {'year':2010})
        req.GET = {}
        self.assertEqual(view.submit_year(), {'year':date.today().year})

    def test_add(self):
        self.addOne()
        proj = self.getOne()
        self.assertNotEqual(proj, None)
        self.assertEqual(proj.value, 1500)
        self.assertEqual(proj.comment, u"Some comments go here")
        self.assertEqual(proj.year, date.today().year)

    def test_add_year(self):
        self.addOne(2002)
        proj = self.getOne()
        self.assertNotEqual(proj, None)
        self.assertEqual(proj.value, 1500)
        self.assertEqual(proj.comment, u"Some comments go here")
        self.assertEqual(proj.year, 2002)


    def test_edit(self):
        self.addOne()
        appstruct = APPSTRUCT.copy()
        appstruct['value'] = 10
        req = self.get_csrf_request()
        view = DisplayCommercialHandling(req)
        view.submit_success(appstruct)
        proj = self.getOne()
        self.assertEqual(proj.value, 10)
