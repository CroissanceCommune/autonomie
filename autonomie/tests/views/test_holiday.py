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
from autonomie.models.user import User
from autonomie.views.holiday import (RestHoliday,
                                    get_holidays)
#HolidayRegister, HolidayView,
from autonomie.tests.base import BaseFunctionnalTest

class TestHolidayRegister(BaseFunctionnalTest):
    def user(self):
        return User.query().first()

    def test_success(self):
#        self.config.add_route("user_holiday", "/")
        user = self.user()

        # Add
        request = self.get_csrf_request()
        request.context = user
        appstruct = {"start_date": "2013-04-15", "end_date": "2013-04-28"}
        request.json_body = appstruct
        view = RestHoliday(request)
        view.post()
        holidays = get_holidays(user_id=user.id).all()
        self.assertEqual(len(holidays), 1)

        # Add second one
        appstruct = {"start_date": "2013-04-01", "end_date": "2013-04-05"}
        request.json_body = appstruct
        view = RestHoliday(request)
        view.post()
        holidays = get_holidays(user_id=user.id).all()
        self.assertEqual(len(holidays), 2)

        # Delete
        request.matchdict['lid'] = holidays[1].id
        view = RestHoliday(request)
        view.delete()
        self.assertEqual(len(get_holidays(user_id=user.id).all()), 1)

        #edition + delete
        appstruct = {"start_date": "2013-04-13", "end_date": "2013-04-27"}
        request.json_body = appstruct
        request.matchdict['lid'] = holidays[0].id
        view = RestHoliday(request)
        view.put()

        holiday = get_holidays(user_id=user.id).all()[0]
        self.assertEqual(holiday.start_date.day, 13)

