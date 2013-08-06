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
from autonomie.models.task.invoice import PaymentMode
from autonomie.models.task import WorkUnit
from autonomie.models.config import get_config
from autonomie.models.treasury import ExpenseType
from autonomie.views.admin import AdminTva
from autonomie.views.admin import AdminMain
from autonomie.views.admin import AdminPaymentMode
from autonomie.views.admin import AdminWorkUnit
from autonomie.views.admin import AdminExpense
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
        appstruct = {'tvas':[{'name':"19,6%", 'value':1960, "default":1},
                {'name':"7%", "value":700, "default":0}]}
        view = AdminTva(self.get_csrf_request())
        view.submit_success(appstruct)
        self.assertEqual(self.session.query(tva.Tva).count(), 2)
        appstruct = {'tvas':[{'name':"19,6%", 'value':1960, "default":1}]}
        view.submit_success(appstruct)
        self.assertEqual(self.session.query(tva.Tva).count(), 1)


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
