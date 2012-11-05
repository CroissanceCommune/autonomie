# -*- coding: utf-8 -*-
# * File Name : test_forms_holiday.py
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
import datetime
import colander

from autonomie.tests.base import BaseTestCase
from autonomie.views.forms.holiday import date_validator, HolidaySchema

class TestHolidays(BaseTestCase):
    def test_date_validator(self):
        start_date = datetime.date(2012, 11, 1)
        end_date = datetime.date(2012, 11, 2)
        form = HolidaySchema()
        self.assertNotRaises(date_validator, form, {'start_date':start_date,
                                            'end_date': end_date})
        self.assertRaises(colander.Invalid, date_validator, form,
                               {'start_date':end_date, 'end_date': start_date})
