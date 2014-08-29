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

import colander
from autonomie.views import BaseFormView

from autonomie.tests.base import BaseTestCase, BaseViewTest

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
