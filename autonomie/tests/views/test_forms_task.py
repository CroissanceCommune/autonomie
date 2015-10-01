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
from mock import MagicMock


from autonomie.forms.task import (
    dbdatas_to_appstruct,
    get_lines_block_appstruct,
    appstruct_to_dbdatas,
    add_order_to_lines,
    set_manualDeliverables,
    add_payment_block_appstruct,
    TASK_MATCHING_MAP,
)
from autonomie.forms.invoices import (
    deferred_total_validator,
    deferred_payment_mode_validator,
)


EST_DBDATAS = dict(
    name=u"Nom du devis",
    course="0",
    display_units="1",
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
    address="address",
)

INV_DBDATAS = dict(
    name=u"Nom de la facture",
    course="0",
    display_units="1",
    expenses_ht=150,
    payment_conditions="Payer à l'heure",
    phase_id=415,
    taskDate="15-12-2012",
    financial_year=2012,
    description="Facture pour le customer test",
    statusComment=u"Aucun commentaire",
    customer_id=15,
    address="address"
)

LINES_DBDATAS = dict(
    lines=[
        {
            'description': 'text1',
            'cost': 10000,
            'unity': 'days',
            'quantity': 12,
            'tva': 1960,
            'order': 1},
        {
            'description': 'text2',
            'cost': 20000,
            'unity': 'month',
            'quantity': 12,
            'tva': 700,
            'order': 2},
        ],
    groups=[
        {
            'description': u'description',
            'title': u'Title',
            'lines': [
                {
                    'description': 'text1',
                    'cost': 10000,
                    'unity': 'days',
                    'quantity': 12,
                    'tva': 1960,
                    'order': 1
                },
            ]
        }
    ],
    discounts=[
        {'description': 'remise1', 'amount': 1000, 'tva': 1960},
        {'description': 'remise2', 'amount': 1000, 'tva': 700},
    ],
    payment_lines=[
        {'description': "Début", "paymentDate": "12-12-2012",
         "amount": 15000, "order": 1},
        {'description': "Milieu", "paymentDate": "13-12-2012",
         "amount": 15000, "order": 2},
        {'description': "Fin", "paymentDate": "14-12-2012",
         "amount": 150, "order": 3},
        ]
)
DATAS = {
    'common': dict(
        name=u"Nom du devis",
        phase_id=485,
        customer_id=15,
        address="address",
        taskDate="10-12-2012",
        description="Devis pour le customer test",
        course="0",
        display_units="1",
    ),
    'lines': dict(
        expenses_ht=150,
        lines=[
            {
                'description': 'text1',
                'cost': 10000,
                'unity': 'days',
                'quantity': 12,
                'tva': 1960
            },
            {
                'description': 'text2',
                'cost': 20000,
                'unity': 'month',
                'quantity': 12,
                'tva': 700
            },
        ],
        groups=[
            {
                'description': u'description',
                'title': u'Title',
                'lines': [
                    {
                        'description': 'text1',
                        'cost': 10000,
                        'unity': 'days',
                        'quantity': 12,
                        'tva': 1960,
                    },
                ]
            }
        ],
        discounts=[
            {
                'description': 'remise1',
                'amount': 1000,
                'tva': 1960,
            },
            {
                'description': 'remise2',
                'amount': 1000,
                'tva': 700,
            },
        ],
    ),
    'notes': dict(exclusions="Ne sera pas fait selon la règle"),
    'payments': dict(
        paymentDisplay='ALL',
        deposit=20,
        payment_times=-1,
        payment_lines=[
            {
                'description': "Début",
                "paymentDate": "12-12-2012",
                "amount": 15000,
            },
            {
                'description': "Milieu",
                "paymentDate": "13-12-2012",
                "amount": 15000,
            },
            {
                'description': "Fin",
                "paymentDate": "14-12-2012",
                "amount": 150,
            },
        ],
        payment_conditions="Payer à l'heure",
    ),
    "communication": dict(
        statusComment=u"Aucun commentaire"
    ),
}


def test_dbdatas_to_appstruct():
    for dbdatas in (EST_DBDATAS, INV_DBDATAS,):
        result = dbdatas_to_appstruct(dbdatas)
        for field, group in TASK_MATCHING_MAP:
            if field in dbdatas:
                assert dbdatas[field] == result[group][field]


def test_get_lines_block_appstruct():
    result = get_lines_block_appstruct({}, LINES_DBDATAS)
    for key in ('lines', 'groups', "discounts"):
        assert key in result['lines']
        assert result['lines'][key] == LINES_DBDATAS.get(key)


def test_appstruct_to_dbdatas():
    result = appstruct_to_dbdatas(DATAS)
    for key, group in TASK_MATCHING_MAP:
        if group in DATAS:
            if key in DATAS[group]:
                assert DATAS[group][key] == result['task'][key]

    datas = {'common': {'address': colander.null}}
    result = appstruct_to_dbdatas(datas)
    assert 'address' not in result['task']

    datas = {'common': {'address': None}}
    result = appstruct_to_dbdatas(datas)
    assert 'address' not in result['task']


def test_add_order_to_lines():
    lines = {'lines': [{'id': 2}, {'id': 1}]}
    appstruct = dict(lines=lines)
    res = add_order_to_lines(appstruct)
    assert res['lines']['lines'][0]['id'] == 2
    assert res['lines']['lines'][0]['order'] == 1

    groups = [
        {
            'gid': 2,
            'lines': [{'id': 2}, {'id': 1}],
        },
        {
            'gid': 1,
            'lines': [{'id': 3}, {'id': 4}],
        },
    ]
    appstruct = {'lines': dict(groups=groups)}
    res = add_order_to_lines(appstruct)
    assert res['lines']['groups'][1]['gid'] == 1
    assert res['lines']['groups'][1]['order'] == 2
    assert res['lines']['groups'][1]['lines'][0] == {'id': 3, 'order': 1}

    payment_lines = [{'id': 2}, {'id': 1}, {'id': 3}]
    appstruct = dict(payments={'payment_lines': payment_lines})
    res = add_order_to_lines(appstruct)
    assert res['payments']['payment_lines'][0]['id'] == 2
    assert res['payments']['payment_lines'][0]['order'] == 1
    assert res['payments']['payment_lines'][2]['order'] == 3


def test_set_manualDeliverables():
    appstruct = {'payments': {'payment_times': 5}}
    res = set_manualDeliverables(appstruct, {})
    assert res['task']['manualDeliverables'] == 0
    appstruct = {'payments': {'payment_times': -1}}
    res = set_manualDeliverables(appstruct, {})
    assert res['task']['manualDeliverables'] == 1


def test_set_payment_times():
    dbdatas = {
        'manualDeliverables': 0,
        'payment_lines': range(5),
        'paymentDisplay': 1,
        'deposit': 0,
    }

    res = add_payment_block_appstruct({}, dbdatas)
    assert res['payments']['payment_times'] == 5
    dbdatas['manualDeliverables'] = 1
    res = add_payment_block_appstruct({}, dbdatas)
    assert res['payments']['payment_times'] == -1


class TestTaskForms:
    def task(self):
        return MagicMock(topay=lambda: 7940, __name__='invoice',
                         project=self.project())

    def project(self):
        return MagicMock(customers=self.customers(), id=1, __name__='project')

    def customers(self):
        return [MagicMock(id=1), MagicMock(id=2)]

    def request(self):
        task = self.task()
        return MagicMock(context=task)

    def test_paymentform_schema_ok(self, dbsession):
        from autonomie.forms.invoices import PaymentSchema
        schema = PaymentSchema().bind(request=self.request())
        form = deform.Form(schema)
        ok_values = [(u'action', u'payment'), (u'_charset_', u'UTF-8'),
                     (u'__formid__', u'deform'),
                     (u'remittance_amount', u'79.4'),
                     (u'amount', u'79.4'),
                     (u"__start__", "date:mapping"),
                     (u'date', '2015-08-07'),
                     (u"__end__", "date:mapping"),
                     ('bank_id', ''),
                     (u'mode', u'par chèque'), (u'submit', u'paid')]
        form.validate(ok_values)

    def test_total_validator(self):
        c = colander.SchemaNode(colander.Integer())
        validator = deferred_total_validator("nutt",
                                             {'request': self.request()})
        with pytest.raises(colander.Invalid):
            validator(c, 7941)
        validator(c, 0)
        validator(c, 7940)

    def test_mode_validator(self, dbsession):
        c = colander.SchemaNode(colander.String())
        validator = deferred_payment_mode_validator("nutt",
                                                    {'request': self.request()})
        with pytest.raises(colander.Invalid):
            validator(c, u'pièce en chocolat')

    def test_customer_validator(self):
        from autonomie.forms.task import deferred_customer_validator
        func = deferred_customer_validator("nutt", {'request': self.request()})
        with pytest.raises(colander.Invalid):
            func("nutt", 0)
        with pytest.raises(colander.Invalid):
            func("nutt", 15)
        func("nutt", 1)
