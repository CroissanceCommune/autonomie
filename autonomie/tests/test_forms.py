# -*- coding: utf-8 -*-
# * File Name : test_forms.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 26-03-2012
# * Last Modified :
#
# * Project : autonomie
#
import colander
from deform.form import Form
from .base import BaseTestCase

class TestFormModels(BaseTestCase):
    def test_unique_login(self):
        from autonomie.views.forms import unique_login
        node = colander.SchemaNode(colander.String())
        self.assertRaises(colander.Invalid, unique_login, node,
                                                    "user1_login")

    def test_fpassword(self):
        from autonomie.views.forms import pwdSchema
        from autonomie.views.forms import auth
        schema = pwdSchema.bind(check=True)
        form = Form(schema)
        ok_values = dict(login='user1_login', password='user1')
        self.assertIsNone(auth(None, ok_values))
        wrong_values = dict(login='user1_login', password='wrongpass')
        self.assertRaises(colander.Invalid, auth, form, wrong_values)
        wrong_values = dict(login='noexist_login', password='')
        self.assertRaises(colander.Invalid, auth, form, wrong_values)



