# -*- coding: utf-8 -*-
# * File Name : test_taskaction.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 26-12-2012
# * Last Modified :
#
# * Project :
#

from mock import MagicMock
from pyramid import testing

from autonomie.tests.base import BaseFunctionnalTest, BaseTestCase
from autonomie.tests.base import BaseViewTest
from autonomie.views.taskaction import (context_is_task, context_is_editable,
        get_paid_form, get_duplicate_form)

class TestFuncs(BaseViewTest):
    def test_context_is_task(self):
        context = MagicMock()
        for i in ("invoice", "cancelinvoice", "estimation"):
            context.__name__ = i
            self.assertTrue(context_is_task(context))

    def test_context_is_not_task(self):
        context = MagicMock()
        for i in ("invoices", "cancelinvoices", "estimations"):
            context.__name__ = i
            self.assertFalse(context_is_task(context))

    def test_context_is_editable(self):
        context = MagicMock()
        context.__name__ = "invoice"
        context.is_editable = lambda :True
        self.assertTrue(context_is_editable(None, context))
        context = MagicMock()
        context.__name__ = "notinvoice"
        self.assertTrue(context_is_editable(None, context))
        context = MagicMock()
        context.__name__ = 'invoice'
        context.is_editable = lambda :False
        context.is_waiting = lambda :True
        request = self.get_csrf_request()
        request.context = context
        self.assertTrue(context_is_editable(request, context))
