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
    from autonomie.views.admin.tva import (
        TvaDisableView,
        TvaEditView,
        TvaAddView,
    )
    config.add_route('/admin/vente/tvas', '/')

    appstruct = {
        'name': "test",
        'value': 0,
        "default": True,
        "mention" : "Test",
        "products": []
    }
    view = TvaAddView(get_csrf_request_with_db())
    view.submit_success(appstruct)

    assert dbsession.query(tva.Tva).filter(tva.Tva.name == 'test').count() == 1

    appstruct = {
        'id': 1, 'name':"21%", 'value':2100, "default": True, 'products': []
    }
    view = TvaEditView(get_csrf_request_with_db())
    view.submit_success(appstruct)
    assert dbsession.query(tva.Tva).filter(tva.Tva.id == 1).first().value == 2100

    request = get_csrf_request_with_db()
    request.context = dbsession.query(
        tva.Tva).filter(tva.Tva.id == 1).first()
    view = TvaDisableView(request)
    view.__call__()
    assert dbsession.query(tva.Tva).filter(
        tva.Tva.id == 1).first().active == False


def test_payment_mode_success(config, dbsession, get_csrf_request_with_db):
    from autonomie.views.admin.vente import PaymentModeAdmin
    config.add_route('admin_vente', '/')
    appstruct = {'datas': [
        {'label': u"Chèque"},
        {'label': u"Expèce"},
    ]}
    view = PaymentModeAdmin(get_csrf_request_with_db())
    view.submit_success(appstruct)
    assert dbsession.query(PaymentMode).count() == 2
    appstruct = {'datas': [
        {'label': u"Chèque"},
    ]}
    view.submit_success(appstruct)
    assert dbsession.query(PaymentMode).count() == 1


def test_workunit_success(config, dbsession, get_csrf_request_with_db):
    from autonomie.views.admin.vente import WorkUnitAdmin
    config.add_route('admin_vente', '/')
    appstruct = {'datas': [
        {'label': u"Semaines"},
        {'label': u"Jours",}
    ]}
    view = WorkUnitAdmin(get_csrf_request_with_db())
    view.submit_success(appstruct)
    assert dbsession.query(WorkUnit).count() == 2
    appstruct = {'datas': [
        {'label': u"Semaines"},
    ]}
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
    from autonomie.views.admin.vente import AdminVenteTreasuryMain
    config.add_route('admin_vente_treasury', '/')
    appstruct = {'compte_cg_contribution':"00000668",
            'compte_rrr':"000009558"}
    view = AdminVenteTreasuryMain(get_csrf_request_with_db())
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
