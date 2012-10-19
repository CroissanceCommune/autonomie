# -*- coding: utf-8 -*-
# * File Name : test_forms_project.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 19-10-2012
# * Last Modified :
#
# * Project :
#
import colander
from mock import MagicMock
from autonomie.views.forms.project import build_client_value
from autonomie.views.forms.project import get_clients_from_request

from autonomie.tests.base import BaseTestCase

class TestProjectForm(BaseTestCase):
    def test_build_client_value(self):
        client = MagicMock(id=12, name=5)
        # deform is expecting a string (while it's an integer type
        self.assertEqual(build_client_value(client)[0], '12')

    def test_get_clients_from_request(self):
        clients = ['clients']
        comp = MagicMock(__name__='company', clients=clients)
        req = MagicMock(context=comp)
        self.assertEqual(get_clients_from_request(req), clients)
        proj = MagicMock(__name__='project', company=comp)
        req = MagicMock(context=proj)
        self.assertEqual(get_clients_from_request(req), clients)


