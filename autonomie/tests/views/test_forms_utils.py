# -*- coding: utf-8 -*-
# * File Name : test_forms_utils.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 17-10-2012
# * Last Modified :
#
# * Project :
#
import colander
from autonomie.views.forms.utils import BaseFormView, CustomForm

from autonomie.tests.base import BaseTestCase, BaseViewTest

class TestCustomForm(BaseTestCase):
    def test_render(self):
        schema = DummySchema()
        form = CustomForm(schema)
        form.appstruct = {'test':u'A value'}
        self.assertTrue('A value' in form.render())

class TestBaseFormView(BaseViewTest):
    def make_one(self, req):
        return BaseFormView(req)

    def test_init(self):
        req = self.get_csrf_request()
        form = self.make_one(req)
        self.assertEqual(form.dbsession, req.dbsession)
        self.assertEqual(form.session, req.session)

    def test_more_vars_called(self):
        req = self.get_csrf_request()
        form = self.make_one(req)
        form.schema = DummySchema()
        form.add_template_vars = ('arg',)
        form.arg = u"Test arg"
        result = form.__call__()
        self.assertTrue(result['arg'], u"Test arg")


class DummySchema(colander.MappingSchema):
    test = colander.SchemaNode(colander.String(), title=u"test")

