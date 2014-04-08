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

"""
    Sage exports tools
"""
from autonomie.views.render_api import format_amount
from autonomie.utils.ascii import force_utf8
from autonomie.export.csvtools import BaseCsvWriter


class SageCsvWriter(BaseCsvWriter):
    """
        Write Sage csv files
        :param datas: The datas to export list of dict
        :param headers: The translation tuple between input and output column
        names
    """
    delimiter = ";"
    headers = ()

    def __init__(self):
        super(SageCsvWriter, self).__init__()

    @property
    def keys(self):
        """
        Return the keys configured in our headers
        Those keys corresponds to the datas keys we ha
        """
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
            return format_amount(debit, grouping=False)

    def format_credit(self, credit):
        """
            format the credit entry to get a clean float
        """
        return self.format_debit(credit)


class SageInvoiceCsvWriter(SageCsvWriter):
    """
    Sage invoice csv writer
    Add the handling of the invoice prefix in invoice number formatting
    """
    headers = (
            ('num_facture', "Numéro de pièce",),
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
            ('type_', "Type de ligne"),
            ('num_analytique', "Numéro analytique"),)

    def set_prefix(self, prefix):
        """
        Set the prefix of the current CAE
        """
        self.prefix = prefix

    def format_num_facture(self, number):
        """
            format the invoice official Number to add a prefix
        """
        return "%s%s" % (self.prefix, number)


class SageExpenseCsvWriter(SageCsvWriter):
    """
    Expense CsvWriter
    """
    headers = (
            ('num_feuille', "Numéro de pièce",),
            ('code_journal', "Code Journal"),
            ('date', "Date de pièce"),
            ('compte_cg', "N° compte général"),
            ('num_feuille', "Numéro de note de frais",),
            ('compte_tiers', "Numéro de compte tiers"),
            ('code_tva', "Code taxe"),
            ('libelle', "Libellé d’écriture"),
            ('debit', "Montant débit"),
            ('credit', "Montant crédit"),
            ('type_', "Type de ligne"),
            ('num_analytique', "Numéro analytique"),)
