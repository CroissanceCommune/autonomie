# -*- coding: utf-8 -*-
# * File Name : tests.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 18-09-2012
# * Last Modified :
#
# * Project :
#
"""
    View for testing js scripts with qunit
    It's not really automated, but it's better than nuts
"""



def testjs(request):
    """
        Only the template is interesting in this view
    """
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
