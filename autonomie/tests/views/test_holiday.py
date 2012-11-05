# -*- coding: utf-8 -*-
# * File Name : test_holiday.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 05-11-2012
# * Last Modified :
#
# * Project :
#
from datetime import date
from autonomie.models.holiday import Holiday
from mock import Mock
from autonomie.views.holiday import HolidayRegister, HolidayView, get_holidays
from autonomie.tests.base import BaseFunctionnalTest

class TestHolidayRegister(BaseFunctionnalTest):
    def test_success(self):
        self.config.add_route("holiday", "/")
        request = self.get_csrf_request()
        request.user = Mock(id=1)
        appstruct = {'holidays':[{'start_date':date(2010, 11,1),
                                    'end_date':date(2010, 11, 5)},
                                {'start_date':date(2010, 5, 8),
                                    'end_date':date(2010, 5, 25)}]}
        view = HolidayRegister(request)
        view.submit_success(appstruct)
        self.assertEqual(len(get_holidays(user_id=1).all()), 2)
        appstruct = {'holidays':[{'start_date':date(2010, 11,1),
                                  'end_date':date(2010, 11, 5)}]}
        request = self.get_csrf_request()
        request.user = Mock(id=1)
        view = HolidayRegister(request)
        view.submit_success(appstruct)
        self.assertEqual(len(get_holidays(user_id=1).all()), 1)

