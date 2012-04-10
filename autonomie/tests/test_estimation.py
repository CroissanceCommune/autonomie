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
from autonomie.views.forms.estimation import collect_indexes
from autonomie.views.forms.estimation import format_lines
from autonomie.views.forms.estimation import format_task
from autonomie.views.forms.estimation import format_estimation
from autonomie.views.forms.estimation import format_payment_conditions
from autonomie.views.forms.estimation import format_datas

origin = dict(
                      id_phase="485",
                      description="Devis pour le client test",
                      taskDate="10-12-2012",

                      course="0",
                      displayedUnits="1",

                      prestation_5="text2",
                      quantity_5="12",
                      unity_5="month",
                      price_5="20",
                      prestation_1="text1",
                      quantity_1="12",
                      unity_1="days",
                      price_1="10",

                      discountHT="20",
                      tva="1960",
                      expenses="150",
                      deposit="20",

                      exclusions="Ne sera pas fait selon la règle",
                      paymentDisplay="1",

                      payment_times="3",
                      description_1="Début",
                      paymentDate_1="12-12-2012",
                      amount_1="150",

                      description_2="Milieu",
                      paymentDate_2="13-12-2012",
                      amount_2="150",

                      description_3="Fin",
                      paymentDate_3="14-12-2012",
                      amount_3="150",

                      paymentConditions="Payer à l'heure",
                      )

expected = dict(estimation=dict(course="0",
                                displayedUnits="1",
                                discountHT="20",
                                tva="1960",
                                expenses="150",
                                deposit="20",
                                exclusions="Ne sera pas fait selon la règle",
                                paymentDisplay="1",
                                paymentConditions="Payer à l'heure",),
                task=dict(id_phase="485",
                          taskDate="10-12-2012",
                          description="Devis pour le client test"),
                estimation_lines=[
                     {'description':'text2',
                     'cost':'20',
                     'unity':'month',
                     'quantity':'12'},
                     {'description':'text1',
                     'cost':'10',
                     'unity':'days',
                     'quantity':'12'},
                     ],
                payment_conditions=[
                    {'description':"Début", "paymentDate":"12-12-2012",
                                            "amount":"150", "rowIndex":1},
                    {'description':"Milieu", "paymentDate":"13-12-2012",
                                           "amount":"150", "rowIndex":2},
                    {'description':"Fin", "paymentDate":"14-12-2012",
                                            "amount":"150", "rowIndex":3},
                    ]
                )


class Test(BaseTestCase):
    maxDiff =None
    def collect_indexes(self):
        keys = ["prestation_5", "prestation_2", "prestation_1", "prestation_10"]
        self.assertEqual(collect_indexes(keys, "prestation_"), [5,2,1,10])
        self.assertEqual(collect_indexes(keys, "prestation_"), [5,2,1,10])

    def test_format_lines(self):
        self.assertEqual(format_lines(origin), expected['estimation_lines'])

    def test_task(self):
        self.assertEqual(format_task(origin), expected['task'])

    def test_estimation(self):
        self.assertEqual(format_estimation(origin), expected['estimation'])

    def test_payment_conditions(self):
        self.assertEqual(format_payment_conditions(origin),
                                expected['payment_conditions'])

    def test_format_datas(self):
        formatted = format_datas(origin)
        self.assertEqual(formatted, expected)
