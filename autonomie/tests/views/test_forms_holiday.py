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

import datetime
import colander
import pytest

from autonomie.forms.holiday import date_validator, HolidaySchema

def test_date_validator():
    start_date = datetime.date(2012, 11, 1)
    end_date = datetime.date(2012, 11, 2)
    form = HolidaySchema()
    date_validator(form, {'start_date':start_date, 'end_date': end_date})
    with pytest.raises(colander.Invalid):
        date_validator(form, {'start_date':end_date, 'end_date': start_date})
