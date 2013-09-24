# -*- coding: utf-8 -*-
# * File Name : sage.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 20-09-2013
# * Last Modified :
#
# * Project :
#
"""
    Sage exports tools
"""

from autonomie.views.render_api import format_amount
from autonomie.utils.ascii import force_utf8
from autonomie.export.csvtools import BaseCsvWriter

class SageCsvWriter(BaseCsvWriter):
    """
        Write Sage csv files
    """
    headers = (
            ('code_journal', "Code Journal"),
            ('date', "Date de pièce"),
            ('compte_cg', "N° compte général"),
            ('num_facture', "Numéro de facture"),
            ('compte_tiers', "Numéro de compte tiers"),
            ('code_tva', "Code taxe"),
            ('libelle', "Libellé d’écriture"),
            ('echeance', "Date d’échéance"),
            ('debit', "Montant débit"),
            ('credit', "Montant crédit"),
            ('num_analytique', "Numéro analytique"),)

    @property
    def keys(self):
        return [val for key, val in self.headers]

    def format_row(self, row):
        """
            Format the row to fit our export
        """
        res_dict = {}
        for key, name in self.headers:
            val = row.get(key, '')
            if hasattr(self, "format_%s" % key):
                val = getattr(self, "format_%s" % key)(val)
            res_dict[name] = force_utf8(val)
        return res_dict

    @staticmethod
    def format_debit(debit):
        """
            Format the debit entry to get a clean float in our export
            12000 => 120,00
        """
        if debit == '':
            return 0
        else:
            return format_amount(debit)

    def format_credit(self, credit):
        """
            format the credit entry to get a clean float
        """
        return self.format_debit(credit)
