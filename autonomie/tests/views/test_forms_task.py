# -*- coding: utf-8 -*-
# * File Name : test_estimation.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 10-04-2012
# * Last Modified :
#
# * Project :
#
import colander
import deform
from copy import deepcopy
from mock import MagicMock

from autonomie.tests.base import BaseTestCase
from autonomie.views.forms.task import deferred_total_validator
from autonomie.views.forms.task import deferred_payment_mode_validator
from autonomie.views.forms.task import deferred_amount_default

DBDATAS = dict(estimation=dict(course="0",
                                displayedUnits="1",
                                expenses=1500,
                                expenses_ht=150,
                                deposit=20,
                                exclusions="Ne sera pas fait selon la règle",
                                paymentDisplay="ALL",
                                paymentConditions="Payer à l'heure",
                                phase_id=485,
                                taskDate="10-12-2012",
                                description="Devis pour le client test",
                                manualDeliverables=1,
                                statusComment=u"Aucun commentaire",
                                client_id=15,
                                address="address"),
                invoice=dict(course="0",
                                displayedUnits="1",
                                expenses=2000,
                                expenses_ht=150,
                                paymentConditions="Payer à l'heure",
                                phase_id=415,
                                taskDate="15-12-2012",
                                financial_year=2012,
                                description="Facture pour le client test",
                                statusComment=u"Aucun commentaire",
                                client_id=15,
                                address="address"
                                ),
                lines=[
                     {'description':'text1',
                     'cost':10000,
                     'unity':'days',
                     'quantity':12,
                     'tva':1960,
                     'rowIndex':1},
                     {'description':'text2',
                     'cost':20000,
                     'unity':'month',
                     'quantity':12,
                     'tva':700,
                     'rowIndex':2},
                     ],
                discounts=[
                          {'description':'remise1', 'amount':1000, 'tva':1960},
                          {'description':'remise2', 'amount':1000, 'tva':700},
                    ],
                payment_lines=[
                    {'description':"Début", "paymentDate":"12-12-2012",
                                            "amount":15000, "rowIndex":1},
                    {'description':"Milieu", "paymentDate":"13-12-2012",
                                           "amount":15000, "rowIndex":2},
                    {'description':"Fin", "paymentDate":"14-12-2012",
                                            "amount":150, "rowIndex":3},
                    ]
                )
DATAS = {'common': dict(phase_id=485,
                        client_id=15,
                        address="address",
                        taskDate="10-12-2012",
                        description="Devis pour le client test",
                        course="0",
                        displayedUnits="1",),
        'lines':dict(expenses=1500,
                     expenses_ht=150,
                     lines=[
       {'description':'text1', 'cost':10000, 'unity':'days', 'quantity':12, 'tva':1960},
       {'description':'text2', 'cost':20000, 'unity':'month', 'quantity':12, 'tva':700},
                            ],
                     discounts=[
      {'description':'remise1', 'amount':1000, 'tva':1960},
      {'description':'remise2', 'amount':1000, 'tva':700},
                     ],),
        'notes':dict(exclusions="Ne sera pas fait selon la règle"),
        'payments':dict(paymentDisplay='ALL',
                        deposit=20,
                        payment_times=-1,
                        payment_lines=[
        {'description':"Début", "paymentDate":"12-12-2012", "amount":15000},
        {'description':"Milieu", "paymentDate":"13-12-2012","amount":15000},
        {'description':"Fin", "paymentDate":"14-12-2012","amount":150},
        ],
        paymentConditions="Payer à l'heure",
        ),
        "communication":dict(statusComment=u"Aucun commentaire"),
                        }
INV_DATAS = {'common': dict(phase_id=415,
                        client_id=15,
                        address="address",
                        taskDate="15-12-2012",
                        financial_year=2012,
                        description="Facture pour le client test",
                        course="0",
                        displayedUnits="1",),
        'lines':dict(expenses=2000,
                     expenses_ht=150,
                     lines=[
       {'description':'text1', 'cost':10000, 'unity':'days', 'quantity':12, 'tva':1960},
       {'description':'text2', 'cost':20000, 'unity':'month', 'quantity':12, 'tva':700},
                            ],
                     discounts=[
      {'description':'remise1', 'amount':1000, 'tva':1960},
      {'description':'remise2', 'amount':1000, 'tva':700},
                     ],),
        'payments':dict(paymentConditions="Payer à l'heure"),
        "communication":dict(statusComment=u"Aucun commentaire"),
        }

def get_full_estimation_model(datas):
    """
        Returns a simulated database model
    """
    est = MagicMock(**datas['estimation'])
    est.lines = [MagicMock(**line)for line in datas['lines']]
    est.payment_lines = [MagicMock(**line)for line in datas['payment_lines']]
    est.discounts = [MagicMock(**line)for line in datas['discounts']]
    return est

def get_full_invoice_model(datas):
    """
        Returns a simulated invoice database model
    """
    inv = MagicMock(**datas['invoice'])
    inv.lines = [MagicMock(**line)for line in datas['lines']]
    inv.discounts = [MagicMock(**line)for line in datas['discounts']]
    return inv

class TestMatchTools(BaseTestCase):
    def test_estimation_dbdatas_to_appstruct(self):
        from autonomie.views.forms.task import EstimationMatch
        e = EstimationMatch()
        result = e.toschema(DBDATAS, {})
        for field, group in e.matching_map:
            self.assertEqual(DBDATAS['estimation'][field], result[group][field])

    def test_estimationlines_dbdatas_to_appstruct(self):
        from autonomie.views.forms.task import TaskLinesMatch
        e = TaskLinesMatch()
        result = e.toschema(DBDATAS, {})
        from copy import deepcopy
        lines = deepcopy(DBDATAS['lines'])
        lines = sorted(lines, key=lambda row:int(row['rowIndex']))
        for line in lines:
            del(line['rowIndex'])
        for i, line in enumerate(lines):
            self.assertEqual(result['lines']['lines'][i], line)

    def test_discountlines_dbdatas_to_appstruct(self):
        from autonomie.views.forms.task import DiscountLinesMatch
        d = DiscountLinesMatch()
        result = d.toschema(DBDATAS, {})
        from copy import deepcopy
        lines = deepcopy(DBDATAS['discounts'])
        for i, line in enumerate(lines):
            self.assertEqual(result['lines']['discounts'][i], line)

    def test_paymentlines_dbdatas_to_appstruct(self):
        from autonomie.views.forms.task import PaymentLinesMatch
        p = PaymentLinesMatch()
        result = p.toschema(DBDATAS, {})
        lines = deepcopy(DBDATAS['payment_lines'])
        lines = sorted(lines, key=lambda row:int(row['rowIndex']))
        for line in lines:
            del(line['rowIndex'])
        for i,line in enumerate(lines):
            self.assertEqual(result['payments']['payment_lines'][i], line)

    def test_invoice_dbdatas_to_appstruct(self):
        from autonomie.views.forms.task import InvoiceMatch
        e = InvoiceMatch()
        result = e.toschema(DBDATAS, {})
        for field, group in e.matching_map:
            self.assertEqual(DBDATAS['invoice'][field], result[group][field])

    def test_appstruct_to_estimationdbdatas(self):
        from autonomie.views.forms.task import EstimationMatch
        datas_ = deepcopy(DATAS)
        e = EstimationMatch()
        result = e.todb(datas_, {})
        dbdatas_ = deepcopy(DBDATAS)
        del(dbdatas_['estimation']['manualDeliverables'])
        self.assertEqual(result['estimation'], dbdatas_['estimation'])

    def test_appstruct_to_estimationlinesdbdatas(self):
        from autonomie.views.forms.task import TaskLinesMatch
        datas_ = deepcopy(DATAS)
        e = TaskLinesMatch()
        result = e.todb(datas_, {})
        self.assertEqual(result['lines'], DBDATAS['lines'])

    def test_appstruct_to_discountlines_dbdatas(self):
        from autonomie.views.forms.task import DiscountLinesMatch
        datas_ = deepcopy(DATAS)
        d = DiscountLinesMatch()
        result = d.todb(datas_, {})
        self.assertEqual(result['discounts'], DBDATAS['discounts'])

    def test_appstruct_to_paymentlinesdbdatas(self):
        from autonomie.views.forms.task import PaymentLinesMatch
        p = PaymentLinesMatch()
        datas_ = deepcopy(DATAS)
        result = p.todb(datas_, {})
        self.assertEqual(result['payment_lines'], DBDATAS['payment_lines'])

    def test_appstruct_to_invoicedbdatas(self):
        from autonomie.views.forms.task import InvoiceMatch
        e = InvoiceMatch()
        datas_ = deepcopy(INV_DATAS)
        result = e.todb(datas_, {})
        self.assertEqual(result['invoice'], DBDATAS['invoice'])

class TestTaskForms(BaseTestCase):
    def task(self):
        return MagicMock(topay=lambda :7940, __name__='invoice',
                project=self.project())

    def project(self):
        return MagicMock(clients=self.clients(), id=1, __name__='project')

    def clients(self):
        return [MagicMock(id=1), MagicMock(id=2)]

    def request(self):
        task = self.task()
        return MagicMock(context=task)

    def test_paymentform_schema_ok(self):
        from autonomie.views.forms.task import PaymentSchema
        schema = PaymentSchema().bind(request=self.request())
        form = deform.Form(schema)
        ok_values = [(u'action', u'payment'), (u'_charset_', u'UTF-8'),
                     (u'__formid__', u'deform'), (u'amount', u'79.4'),
                     (u'mode', u'par chèque'), (u'submit', u'paid')]
        form.validate(ok_values)

    def test_total_validator(self):
        c = colander.SchemaNode(colander.Integer())
        validator = deferred_total_validator("nutt", {'request':self.request()})
        self.assertRaises(colander.Invalid, validator, c, 7941)
        validator(c, 0)
        validator(c, 7940)

    def test_mode_validator(self):
        c = colander.SchemaNode(colander.String())
        validator = deferred_payment_mode_validator("nutt", {'request':self.request()})
        self.assertRaises(colander.Invalid, validator, c, u'pièce en chocolat')

    def test_client_validator(self):
        from autonomie.views.forms.task import deferred_client_validator
        func = deferred_client_validator("nutt", {'request':self.request()})
        self.assertRaises(colander.Invalid, func, "nutt", 0)
        self.assertRaises(colander.Invalid, func, "nutt", 15)
        self.assertNotRaises(func, "nutt", 1)
