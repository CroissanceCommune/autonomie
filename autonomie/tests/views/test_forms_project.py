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
