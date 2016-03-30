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

pytest.mark.usefixtures("config")

from autonomie.models import tva
from autonomie.models.task.invoice import PaymentMode
from autonomie.models.task import WorkUnit
from autonomie.models.config import (
    get_config,
    Config,
)


def test_main_config_success(config, get_csrf_request_with_db, dbsession):
    from autonomie.views.admin.main import AdminMain
    config.add_route('admin_main', '/')
    appstruct = {
        "site": {'welcome': 'testvalue'},
        "document": {'footertitle': 'testvalue2'}
    }
    view = AdminMain(get_csrf_request_with_db())
    view.submit_success(appstruct)
    assert get_config()['welcome'] == u'testvalue'
    assert get_config()['coop_pdffootertitle'] == u'testvalue2'


def test_tvaview_success(config, get_csrf_request_with_db, dbsession):
    from autonomie.views.admin.main import AdminTva
    config.add_route('admin_tva', '/')

    appstruct = {'tvas': [
        {'name':"19,6%", 'value':1960, "default":1, "products":[]},
        {'name':"7%", "value":700, "default":0, "products":[]}
        ]}
    view = AdminTva(get_csrf_request_with_db())
    view.submit_success(appstruct)
    assert dbsession.query(tva.Tva).filter(tva.Tva.active==True).count() == 2

    appstruct = {'tvas':[{'name':"19,6%", 'value':1960, "default":1,
        "products":[]}]}
    view.submit_success(appstruct)
    assert dbsession.query(tva.Tva).filter(tva.Tva.active==True).count() == 1


def test_payment_mode_success(config, dbsession, get_csrf_request_with_db):
    from autonomie.views.admin.main import AdminPaymentMode
    config.add_route('admin_paymentmode', '/')
    appstruct = {'paymentmodes':[u"Chèque", u"Expèce"]}
    view = AdminPaymentMode(get_csrf_request_with_db())
    view.submit_success(appstruct)
    assert dbsession.query(PaymentMode).count() == 2
    appstruct = {'paymentmodes':[u"Chèque"]}
    view.submit_success(appstruct)
    assert dbsession.query(PaymentMode).count() == 1


def test_workunit_success(config, dbsession, get_csrf_request_with_db):
    from autonomie.views.admin.main import AdminWorkUnit
    config.add_route('admin_workunit', '/')
    appstruct = {'workunits':[u"Jours", u"Semaines"]}
    view = AdminWorkUnit(get_csrf_request_with_db())
    view.submit_success(appstruct)
    assert dbsession.query(WorkUnit).count() == 2
    appstruct = {'workunits':[u"Jours"]}
    view.submit_success(appstruct)
    assert dbsession.query(WorkUnit).count() == 1


class DummyForm(object):
    def set_appstruct(self, appstruct):
        self.appstruct = appstruct

def test_base_config_view(config, dbsession, get_csrf_request_with_db):
    from autonomie.views.admin.tools import BaseConfigView
    from autonomie.forms.admin import get_config_schema

    class TestView(BaseConfigView):
        title = u"Test",
        keys = ('test_key1', 'test_key2')
        schema = get_config_schema(keys)
        validation_msg = u"Ok"
        redirect_path = "test"

    config.add_route(TestView.redirect_path, '/')

    appstruct = {'test_key1': 'test1', 'test_wrong_key': 'test error'}

    view = TestView(get_csrf_request_with_db())
    view.submit_success(appstruct)

    assert Config.get('test_key1').value == 'test1'
    assert Config.get('test_wrong_key') == None


def test_config_cae_success(config, dbsession, get_csrf_request_with_db):
    from autonomie.views.admin.main import AdminCae
    config.add_route(AdminCae.redirect_path, "/")
    appstruct = {'compte_cg_contribution':"00000668",
            'compte_rrr':"000009558"}
    view = AdminCae(get_csrf_request_with_db())
    view.submit_success(appstruct)
    config = get_config()
    for key, value in appstruct.items():
        assert config[key] == value

def test_admin_activities_get_edited_elements(config, dbsession, get_csrf_request_with_db):
    from autonomie.views.admin.main import AdminActivities
    obj = AdminActivities(get_csrf_request_with_db())
    datas = {'tests':
        [
            {'id':5},
            {'id':4},
            {},
        ]
        }
    res = obj.get_edited_elements(datas, 'tests')
    assert set(res.keys()) == set([5,4])
