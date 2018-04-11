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
import pytest

from autonomie.models.config import (
    get_config,
)
pytest.mark.usefixtures("config")


def test_main_config_success(config, get_csrf_request_with_db, dbsession):
    from autonomie.views.admin.main import (
        AdminMainView,
        MAIN_URL,
    )
    config.add_route(MAIN_URL, '/')
    appstruct = {
        "site": {'welcome': 'testvalue'},
        "document": {'footertitle': 'testvalue2'}
    }
    view = AdminMainView(get_csrf_request_with_db())
    view.submit_success(appstruct)
    assert get_config()['welcome'] == u'testvalue'
    assert get_config()['coop_pdffootertitle'] == u'testvalue2'
