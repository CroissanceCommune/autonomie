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
from copy import deepcopy
from mock import MagicMock
from .base import BaseTestCase
DBDATAS = dict(estimation=dict(course="0",
                                displayedUnits="1",
                                discountHT=2000,
                                tva=1960,
                                expenses=1500,
                                deposit=20,
                                exclusions="Ne sera pas fait selon la règle",
                                paymentDisplay="ALL",
                                paymentConditions="Payer à l'heure",
                                phase_id=485,
                                taskDate="10-12-2012",
                                description="Devis pour le client test",
                                manualDeliverables=1,
                                statusComment=u"Aucun commentaire"),
                lines=[
                     {'description':'text1',
                     'cost':1000,
                     'unity':'days',
                     'quantity':12,
                     'rowIndex':1},
                     {'description':'text2',
                     'cost':20000,
                     'unity':'month',
                     'quantity':12,
                     'rowIndex':2},
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
DBDATAS2 = dict(estimation=dict(course="0",
                                displayedUnits="1",
                                discountHT=0,
                                tva=0,
                                expenses=0,
                                deposit=0,
                                exclusions="Ne sera pas fait selon la règle",
                                paymentDisplay="ALL",
                                paymentConditions="Payer à l'heure",
                                phase_id=485,
                                taskDate="10-12-2012",
                                description="Devis pour le client test",
                                statusComment=u"Aucun commentaire",
                                manualDeliverables=0),
                lines=[
                     {'description':'text1',
                     'cost':1000,
                     'unity':'days',
                     'quantity':1,
                     'rowIndex':1},
                     ],
                payment_lines=[
                    {'description':"Début", "paymentDate":"12-12-2012",
                                            "amount":15, "rowIndex":1},
                    {'description':"Milieu", "paymentDate":"13-12-2012",
                                           "amount":15, "rowIndex":2},
                    {'description':"Fin", "paymentDate":"14-12-2012",
                                            "amount":1, "rowIndex":3},
                    ]
                )
DATAS = {'common': dict(phase_id=485,
                        taskDate="10-12-2012",
                        description="Devis pour le client test",
                        course="0",
                        displayedUnits="1",),
        'lines':dict(discountHT=2000,
                     tva=1960,
                     expenses=1500,
                     lines=[
       {'description':'text1', 'cost':1000, 'unity':'days', 'quantity':12,},
       {'description':'text2', 'cost':20000, 'unity':'month', 'quantity':12},
                            ]
                     ),
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

def get_full_estimation_model(datas):
    """
        Returns a simulated database model
    """
    est = MagicMock(**datas['estimation'])
    estlines = [MagicMock(**line)for line in datas['lines']]
    estpayments = [MagicMock(**line)for line in datas['payment_lines']]
    est.lines = estlines
    est.payment_lines = estpayments
    return est

class TestEstimationMatchTools(BaseTestCase):
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
        print result
        self.assertEqual(result['lines'], DBDATAS['lines'])

    def test_appstruct_to_paymentlinesdbdatas(self):
        from autonomie.views.forms.task import PaymentLinesMatch
        p = PaymentLinesMatch()
        datas_ = deepcopy(DATAS)
        result = p.todb(datas_, {})
        self.assertEqual(result['payment_lines'], DBDATAS['payment_lines'])
