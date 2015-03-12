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
import colander
import deform
from copy import deepcopy
from mock import MagicMock

from autonomie.forms.task import deferred_total_validator
from autonomie.forms.task import deferred_payment_mode_validator

DBDATAS = dict(
    estimation=dict(
        name=u"Nom du devis",
        course="0",
        display_units="1",
        expenses=1500,
        expenses_ht=150,
        deposit=20,
        exclusions="Ne sera pas fait selon la règle",
        paymentDisplay="ALL",
        payment_conditions="Payer à l'heure",
        phase_id=485,
        taskDate="10-12-2012",
        description="Devis pour le customer test",
        manualDeliverables=1,
        statusComment=u"Aucun commentaire",
        customer_id=15,
        address="address"),
    invoice=dict(
        name=u"Nom de la facture",
        course="0",
        display_units="1",
        expenses=2000,
        expenses_ht=150,
        payment_conditions="Payer à l'heure",
        phase_id=415,
        taskDate="15-12-2012",
        financial_year=2012,
        description="Facture pour le customer test",
        statusComment=u"Aucun commentaire",
        customer_id=15,
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
DATAS = {'common': dict(
    name=u"Nom du devis",
    phase_id=485,
    customer_id=15,
    address="address",
    taskDate="10-12-2012",
    description="Devis pour le customer test",
    course="0",
    display_units="1",),
    'lines': dict(
        expenses=1500,
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
    'payments':dict(
        paymentDisplay='ALL',
        deposit=20,
        payment_times=-1,
        payment_lines=[
    {'description':"Début", "paymentDate":"12-12-2012", "amount":15000},
    {'description':"Milieu", "paymentDate":"13-12-2012","amount":15000},
    {'description':"Fin", "paymentDate":"14-12-2012","amount":150},
    ],
        payment_conditions="Payer à l'heure",
    ),
    "communication":dict(statusComment=u"Aucun commentaire"),
                    }
INV_DATAS = {'common': dict(
    name=u"Nom de la facture",
    phase_id=415,
    customer_id=15,
    address="address",
    taskDate="15-12-2012",
    financial_year=2012,
    description="Facture pour le customer test",
    course="0",
    display_units="1",),
    'lines':dict(
        expenses=2000,
        expenses_ht=150,
        lines=[
            {'description':'text1',
             'cost':10000,
             'unity':'days',
             'quantity':12,
             'tva':1960},
            {'description':'text2',
             'cost':20000,
             'unity':'month',
             'quantity':12,
             'tva':700},
            ],
        discounts=[
            {'description':'remise1',
             'amount':1000,
             'tva':1960},
            {'description':'remise2',
             'amount':1000,
             'tva':700},
    ],),
    'payments':dict(payment_conditions="Payer à l'heure"),
    "communication":dict(statusComment=u"Aucun commentaire"),
    }



class TestMatchTools:
    def test_estimation_dbdatas_to_appstruct(self):
        from autonomie.forms.task import EstimationMatch
        e = EstimationMatch()
        result = e.toschema(DBDATAS, {})
        for field, group in e.matching_map:
            assert DBDATAS['estimation'][field] == result[group][field]

    def test_estimationlines_dbdatas_to_appstruct(self):
        from autonomie.forms.task import TaskLinesMatch
        e = TaskLinesMatch()
        result = e.toschema(DBDATAS, {})
        from copy import deepcopy
        lines = deepcopy(DBDATAS['lines'])
        lines = sorted(lines, key=lambda row:int(row['rowIndex']))
        for line in lines:
            del(line['rowIndex'])
        for i, line in enumerate(lines):
            assert result['lines']['lines'][i] == line

    def test_discountlines_dbdatas_to_appstruct(self):
        from autonomie.forms.task import DiscountLinesMatch
        d = DiscountLinesMatch()
        result = d.toschema(DBDATAS, {})
        from copy import deepcopy
        lines = deepcopy(DBDATAS['discounts'])
        for i, line in enumerate(lines):
            assert result['lines']['discounts'][i] == line

    def test_paymentlines_dbdatas_to_appstruct(self):
        from autonomie.forms.task import PaymentLinesMatch
        p = PaymentLinesMatch()
        result = p.toschema(DBDATAS, {})
        lines = deepcopy(DBDATAS['payment_lines'])
        lines = sorted(lines, key=lambda row:int(row['rowIndex']))
        for line in lines:
            del(line['rowIndex'])
        for i,line in enumerate(lines):
            assert result['payments']['payment_lines'][i] == line

    def test_invoice_dbdatas_to_appstruct(self):
        from autonomie.forms.task import InvoiceMatch
        e = InvoiceMatch()
        result = e.toschema(DBDATAS, {})
        for field, group in e.matching_map:
            assert DBDATAS['invoice'][field] == result[group][field]

    def test_appstruct_to_estimationdbdatas(self):
        from autonomie.forms.task import EstimationMatch
        datas_ = deepcopy(DATAS)
        e = EstimationMatch()
        result = e.todb(datas_, {})
        dbdatas_ = deepcopy(DBDATAS)
        del(dbdatas_['estimation']['manualDeliverables'])
        assert result['estimation'] == dbdatas_['estimation']

    def test_appstruct_to_estimationlinesdbdatas(self):
        from autonomie.forms.task import TaskLinesMatch
        datas_ = deepcopy(DATAS)
        e = TaskLinesMatch()
        result = e.todb(datas_, {})
        assert result['lines'] == DBDATAS['lines']

    def test_appstruct_to_discountlines_dbdatas(self):
        from autonomie.forms.task import DiscountLinesMatch
        datas_ = deepcopy(DATAS)
        d = DiscountLinesMatch()
        result = d.todb(datas_, {})
        assert result['discounts'] == DBDATAS['discounts']

    def test_appstruct_to_paymentlinesdbdatas(self):
        from autonomie.forms.task import PaymentLinesMatch
        p = PaymentLinesMatch()
        datas_ = deepcopy(DATAS)
        result = p.todb(datas_, {})
        assert result['payment_lines'] == DBDATAS['payment_lines']

    def test_appstruct_to_invoicedbdatas(self):
        from autonomie.forms.task import InvoiceMatch
        e = InvoiceMatch()
        datas_ = deepcopy(INV_DATAS)
        result = e.todb(datas_, {})
        assert result['invoice'] == DBDATAS['invoice']

class TestTaskForms:
    def task(self):
        return MagicMock(topay=lambda :7940, __name__='invoice',
                project=self.project())

    def project(self):
        return MagicMock(customers=self.customers(), id=1, __name__='project')

    def customers(self):
        return [MagicMock(id=1), MagicMock(id=2)]

    def request(self):
        task = self.task()
        return MagicMock(context=task)

    def test_paymentform_schema_ok(self, dbsession):
        from autonomie.forms.task import PaymentSchema
        schema = PaymentSchema().bind(request=self.request())
        form = deform.Form(schema)
        ok_values = [(u'action', u'payment'), (u'_charset_', u'UTF-8'),
                     (u'__formid__', u'deform'), (u'amount', u'79.4'),
                     (u'mode', u'par chèque'), (u'submit', u'paid')]
        form.validate(ok_values)

    def test_total_validator(self):
        c = colander.SchemaNode(colander.Integer())
        validator = deferred_total_validator("nutt", {'request':self.request()})
        with pytest.raises(colander.Invalid):
            validator(c, 7941)
        validator(c, 0)
        validator(c, 7940)

    def test_mode_validator(self, dbsession):
        c = colander.SchemaNode(colander.String())
        validator = deferred_payment_mode_validator("nutt", {'request':self.request()})
        with pytest.raises(colander.Invalid):
            validator(c, u'pièce en chocolat')

    def test_customer_validator(self):
        from autonomie.forms.task import deferred_customer_validator
        func = deferred_customer_validator("nutt", {'request':self.request()})
        with pytest.raises(colander.Invalid):
            func("nutt", 0)
        with pytest.raises(colander.Invalid):
            func("nutt", 15)
        func("nutt", 1)
