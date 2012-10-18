# -*- coding: utf-8 -*-
# * File Name : test_admin.py
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
from autonomie.models import tva
from autonomie.models.config import get_config
from autonomie.views.admin import AdminTva, AdminMain
from autonomie.tests.base import BaseFunctionnalTest

class TestTvaView(BaseFunctionnalTest):
    def test_success(self):
        self.config.add_route('admin_tva', '/')
        appstruct = {'tvas':[{'name':"19,6%", 'value':1960, "default":1},
                {'name':"7%", "value":700, "default":0}]}
        view = AdminTva(self.get_csrf_request())
        view.submit_success(appstruct)
        self.assertEqual(len(self.session.query(tva.Tva).all()), 2)
        appstruct = {'tvas':[{'name':"19,6%", 'value':1960, "default":1}]}
        view.submit_success(appstruct)
        self.assertEqual(len(self.session.query(tva.Tva).all()), 1)

class TestMainView(BaseFunctionnalTest):
    def test_success(self):
        self.config.add_route('admin_main', '/')
        appstruct = {"site":{'welcome':'testvalue'},
                     "document":{'footertitle':'testvalue2'}}
        view = AdminMain(self.get_csrf_request())
        view.submit_success(appstruct)
        print get_config()
        self.assertTrue(get_config()['welcome'] == u'testvalue')
        self.assertTrue(get_config()['coop_pdffootertitle'] == u'testvalue2')
