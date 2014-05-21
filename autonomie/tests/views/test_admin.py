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

from autonomie.models import tva
from autonomie.models.task.invoice import PaymentMode
from autonomie.models.task import WorkUnit
from autonomie.models.config import get_config
from autonomie.models.treasury import ExpenseType
from autonomie.views.admin import (
    AdminTva,
    AdminMain,
    AdminPaymentMode,
    AdminWorkUnit,
    AdminExpense,
    AdminCae,
    AdminActivities,
    )
from autonomie.tests.base import BaseFunctionnalTest


class TestMainView(BaseFunctionnalTest):
    def test_success(self):
        self.config.add_route('admin_main', '/')
        appstruct = {"site":{'welcome':'testvalue'},
                     "document":{'footertitle':'testvalue2'}}
        view = AdminMain(self.get_csrf_request())
        view.submit_success(appstruct)
        self.assertTrue(get_config()['welcome'] == u'testvalue')
        self.assertTrue(get_config()['coop_pdffootertitle'] == u'testvalue2')


class TestTvaView(BaseFunctionnalTest):
    def test_success(self):
        self.config.add_route('admin_tva', '/')

        appstruct = {'tvas':[
            {'name':"19,6%", 'value':1960, "default":1, "products":[], 'id':0},
            {'name':"7%", "value":700, "default":0, "products":[], 'id':0}
            ]}
        view = AdminTva(self.get_csrf_request())
        view.submit_success(appstruct)
        self.assertEqual(self.session.query(tva.Tva)\
                .filter(tva.Tva.active==True).count(), 2)

        appstruct = {'tvas':[{'name':"19,6%", 'value':1960, "default":1,
            "id":0, "products":[]}]}
        view.submit_success(appstruct)
        self.assertEqual(self.session.query(tva.Tva)\
                .filter(tva.Tva.active==True).count(), 1)


class TestPaymentModeView(BaseFunctionnalTest):
    def test_success(self):
        self.config.add_route('admin_paymentmode', '/')
        appstruct = {'paymentmodes':[u"Chèque", u"Expèce"]}
        view = AdminPaymentMode(self.get_csrf_request())
        view.submit_success(appstruct)
        self.assertEqual(self.session.query(PaymentMode).count(), 2)
        appstruct = {'paymentmodes':[u"Chèque"]}
        view.submit_success(appstruct)
        self.assertEqual(self.session.query(PaymentMode).count(), 1)


class TestWorkUnitView(BaseFunctionnalTest):
    def test_success(self):
        self.config.add_route('admin_workunit', '/')
        appstruct = {'workunits':[u"Jours", u"Semaines"]}
        view = AdminWorkUnit(self.get_csrf_request())
        view.submit_success(appstruct)
        self.assertEqual(self.session.query(WorkUnit).count(), 2)
        appstruct = {'workunits':[u"Jours"]}
        view.submit_success(appstruct)
        self.assertEqual(self.session.query(WorkUnit).count(), 1)


class DummyForm(object):
    def set_appstruct(self, appstruct):
        self.appstruct = appstruct

class TestExpenseView(BaseFunctionnalTest):
    def test_success(self):
        self.config.add_route('admin_expense', '/')
        appstruct = {'expenses':[
            {'label':u"Restauration", "code":u"0001", "id":None},
            {'label':u"Déplacement", "code":u"0002", "id":None}],
                    'expenseskm':[
            {'label':u"Scooter", "code":u"0003", "amount":"0.852", "id":None}],
                    'expensestel':[
            {'label':u"Adsl-Téléphone", "code":u"0004", "percentage":"80",
                "id":None}]}
        view = AdminExpense(self.get_csrf_request())
        view.submit_success(appstruct)

        form = DummyForm()
        view.before(form)
        self.assertEqual(len(form.appstruct['expenses']), 2)
        self.assertEqual(form.appstruct['expenses'][0]['label'], u"Restauration")
        self.assertEqual(form.appstruct['expenses'][0]['code'], u"0001")
        self.assertEqual(form.appstruct['expenseskm'][0]['label'], u"Scooter")
        self.assertEqual(form.appstruct['expenseskm'][0]['amount'], 0.852)
        self.assertEqual(form.appstruct['expensestel'][0]['percentage'], 80)

    def test_success_id_preservation(self):
        self.config.add_route('admin_expense', '/')
        appstruct = {'expenses':[
            {'label':u"Restauration", "code":u"0001", "id":None}],
                    'expenseskm':[],
                    'expensestel':[]}
        view = AdminExpense(self.get_csrf_request())
        view.submit_success(appstruct)

        expense = ExpenseType.query().filter(ExpenseType.code=="0001").first()
        appstruct['expenses'][0]['id'] = expense.id
        appstruct['expenses'][0]['code'] = u"00002"
        view = AdminExpense(self.get_csrf_request())
        view.submit_success(appstruct)
        expense = ExpenseType.query().filter(ExpenseType.id==expense.id).first()
        self.assertEqual(expense.code, u"00002")

class TestCaeView(BaseFunctionnalTest):
    def test_success(self):
        self.config.add_route("admin_cae", "/")
        appstruct = {'compte_cg_contribution':"00000668",
                'compte_rrr':"000009558"}
        view = AdminCae(self.get_csrf_request())
        view.submit_success(appstruct)
        config = get_config()
        for key, value in appstruct.items():
            self.assertEqual(config[key], value)

class TestAdminActivities(BaseFunctionnalTest):
    def test_get_edited_elements(self):
        obj = AdminActivities(self.get_csrf_request())
        datas = {'tests':
            [
                {'id':5},
                {'id':4},
                {},
            ]
            }
        self.assertItemsEqual(obj.get_edited_elements(datas, 'tests')\
                .keys(), [5,4])


