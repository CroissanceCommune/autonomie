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
from .base import BaseTestCase
dbdatas = dict(estimation=dict(course="0",
                                displayedUnits="1",
                                discountHT="20",
                                tva="1960",
                                expenses="150",
                                deposit="20",
                                exclusions="Ne sera pas fait selon la règle",
                                paymentDisplay="1",
                                paymentConditions="Payer à l'heure",
                                IDPhase="485",
                                taskDate="10-12-2012",
                                description="Devis pour le client test"),
                estimation_lines=[
                     {'description':'text2',
                     'cost':'20',
                     'unity':'month',
                     'quantity':'12',
                     'rowIndex':'2'},
                     {'description':'text1',
                     'cost':'10',
                     'unity':'days',
                     'quantity':'12',
                     'rowIndex':'1'},
                     ],
                payment_lines=[
                    {'description':"Début", "paymentDate":"12-12-2012",
                                            "amount":"150", "rowIndex":1},
                    {'description':"Milieu", "paymentDate":"13-12-2012",
                                           "amount":"150", "rowIndex":2},
                    {'description':"Fin", "paymentDate":"14-12-2012",
                                            "amount":"150", "rowIndex":3},
                    ]
                )
datas = {'common': dict(IDPhase="485",
                        taskDate="10-12-2012",
                        description="Devis pour le client test",
                        course="0",
                        displayedUnits="1",),
        'lines':dict(discountHT='20',
                     tva="1960",
                     expenses="150",),
        'notes':dict(exclusions="Ne sera pas fait selon la règle"),
        'payments':dict(paymentDisplay='1',
                        deposit='20',),
        'comments':dict(paymentConditions="Payer à l'heure"),
                        }

class Test(BaseTestCase):
    def test_merge_estimation_in_session(self):
        from autonomie.views.forms.estimation import EstimationMatch
        e = EstimationMatch()
        result = e.toschema(dbdatas, {})
        for field, group in e.matching_map:
            self.assertEqual(dbdatas['estimation'][field], result[group][field])

    def test_merge_estimationlines_in_session(self):
        from autonomie.views.forms.estimation import EstimationLinesMatch
        e = EstimationLinesMatch()
        result = e.toschema(dbdatas, {})
        from copy import deepcopy
        lines = deepcopy(dbdatas['estimation_lines'])
        lines = sorted(lines, key=lambda row:int(row['rowIndex']))
        for line in lines:
            del(line['rowIndex'])
        for i, line in enumerate(lines):
            self.assertEqual(result['lines']['lines'][i], line)

    def test_merge_paymentlines_in_session(self):
        from autonomie.views.forms.estimation import PaymentLinesMatch
        p = PaymentLinesMatch()
        result = p.toschema(dbdatas, {})
        print result
        from copy import deepcopy
        lines = deepcopy(dbdatas['payment_lines'])
        lines = sorted(lines, key=lambda row:int(row['rowIndex']))
        for line in lines:
            del(line['rowIndex'])
        for i,line in enumerate(lines):
            self.assertEqual(result['payments']['payment_lines'][i], line)
