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

"""
    View for testing js scripts with qunit
    It's not really automated, but it's better than nuts
"""
from autonomie.resources import test_js


def testjs(request):
    """
        Only the template is interesting in this view
    """
    test_js.need()
    return dict(title=u"Page de test pour les composantes javascript")


def includeme(config):
    """
        Adding route and view for js tests usefull to test browser problems
    """
    config.add_route("testjs", "/testjs")
    config.add_view(testjs,
                    route_name='testjs',
                    permission="admin",
                    renderer='/tests/base.mako')
