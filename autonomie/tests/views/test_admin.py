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
from autonomie.models.treasury import ExpenseType
from autonomie.models.config import (
        get_config,
        Config,
        )

#from autonomie.views.admin.main import (
#    AdminWorkUnit,
#    AdminExpense,
#    AdminCae,
#    AdminActivities,
#    )


def test_success(config, get_csrf_request_with_db, dbsession):
    from autonomie.views.admin.main import AdminMain
    config.add_route('admin_main', '/')
    appstruct = {"site":{'welcome':'testvalue'},
                    "document":{'footertitle':'testvalue2'}}
    view = AdminMain(get_csrf_request_with_db())
    view.submit_success(appstruct)
    assert get_config()['welcome'] == u'testvalue'
    assert get_config()['coop_pdffootertitle'] == u'testvalue2'


def test_tvaview_success(config, get_csrf_request_with_db, dbsession):
    from autonomie.views.admin.main import AdminTva
    config.add_route('admin_tva', '/')

    appstruct = {'tvas':[
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

def test_expense_config_success(config, dbsession, get_csrf_request_with_db):
    from autonomie.views.admin.main import AdminExpense
    config.add_route('admin_expense', '/')
    appstruct = {
            "code_journal": "JOURNAL01",
            'compte_cg': "DOE548",
            'expenses':[
{'label':u"Restauration", "code":u"0001", "id":None, 'compte_tva':"CTVA" },

{'label':u"Déplacement", "code":u"0002", "id":None, 'code_tva':"TVA"}
        ],
                'expenseskm':[
{'label':u"Scooter", "code":u"0003", "amount":"0.852", "id":None,
    'code_tva':"TVA1"}],
                'expensestel':[
{'label':u"Adsl-Téléphone", "code":u"0004", "percentage":"80",
    "id":None, "code_tva": "TVA2", 'contribution': True}]}
    view = AdminExpense(get_csrf_request_with_db())
    view.submit_success(appstruct)

    assert "DOE548" == Config.get('compte_cg_ndf').value
    assert "JOURNAL01" == Config.get('code_journal_ndf').value

    form = DummyForm()
    view.before(form)
    assert len(form.appstruct['expenses']) == 2
    assert form.appstruct['expenses'][0]['label'] == u"Restauration"
    assert form.appstruct['expenses'][0]['code'] == u"0001"
    assert form.appstruct['expenses'][0]['compte_tva'] == "CTVA"
    assert form.appstruct['expenses'][1]['code_tva'] == "TVA"

    assert form.appstruct['expenseskm'][0]['label'] == u"Scooter"
    assert form.appstruct['expenseskm'][0]['amount'] == 0.852
    assert form.appstruct['expenseskm'][0]['code_tva'] == 'TVA1'
    assert form.appstruct['expensestel'][0]['percentage'] == 80
    assert form.appstruct['expensestel'][0]['code_tva'] == 'TVA2'
    assert form.appstruct['expensestel'][0]['contribution'] == True

def test_success_id_preservation(config, dbsession, get_csrf_request_with_db):
    from autonomie.views.admin.main import AdminExpense
    config.add_route('admin_expense', '/')
    appstruct = {'expenses':[
        {'label':u"Restauration", "code":u"0001", "id":None}],
                'expenseskm':[],
                'expensestel':[]}
    view = AdminExpense(get_csrf_request_with_db())
    view.submit_success(appstruct)

    expense = ExpenseType.query().filter(ExpenseType.code=="0001").first()

    appstruct['expenses'][0]['id'] = expense.id
    appstruct['expenses'][0]['code'] = u"00002"
    view = AdminExpense(get_csrf_request_with_db())
    view.submit_success(appstruct)
    expense = ExpenseType.query().filter(ExpenseType.id==expense.id).first()
    assert expense.code == u"00002"


def test_config_cae_success(config, dbsession, get_csrf_request_with_db):
    from autonomie.views.admin.main import AdminCae
    config.add_route("admin_index", "/")
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
