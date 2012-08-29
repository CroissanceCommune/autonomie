# -*- coding: utf-8 -*-
# * File Name : test_views_form_task.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 29-08-2012
# * Last Modified :
#
# * Project :
#
import colander
import deform

from mock import MagicMock
from .base import BaseFunctionnalTest
from .base import BaseViewTest
from .base import BaseTestCase

from autonomie.views.forms.task import deferred_total_validator
from autonomie.views.forms.task import deferred_amount_default

class TestTaskForms(BaseTestCase):
    def task(self):
        return MagicMock(topay=lambda :7940)

    def test_total_valid(self):
        c = colander.SchemaNode(colander.Integer())
        task = self.task()
        validator = deferred_total_validator("nutt", {'task':task})
        self.assertRaises(colander.Invalid, validator, c, 7941)
        validator(c, 0)
        validator(c, 7940)

    def test_paymentform_schema(self):
        from autonomie.views.forms.task import Payment
        schema = Payment().bind(task=self.task())
        form = deform.Form(schema)
        ok_values = [(u'action', u'payment'), (u'_charset_', u'UTF-8'), (u'__formid__', u'deform'), (u'amount', u'79.4'), (u'mode', u'CHEQUE'), (u'submit', u'paid')]
        form.validate(ok_values)

