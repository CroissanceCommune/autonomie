# -*- coding: utf-8 -*-
# * File Name : test_commercial.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 06-02-2013
# * Last Modified :
#
# * Project :
#
"""
    Test the commercial handling module
"""
from datetime import date
from mock import Mock
from autonomie.views.commercial import compute_percent
from autonomie.views.commercial import compute_difference
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

    def test_compute_difference(self):
        index = 0
        projections = {}
        turnovers = {}
        self.assertEqual(None, compute_difference(index,
                                                  projections, turnovers))
        p = Mock(value=10)
        projections = {0:p}
        turnovers = {0:10}
        self.assertEqual(None, compute_difference(1, projections, turnovers))
        self.assertEqual(0, compute_difference(0, projections, turnovers))

    def test_compute_percent(self):
        pass

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
