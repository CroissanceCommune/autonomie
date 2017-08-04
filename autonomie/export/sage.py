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
from autonomie.utils.strings import format_amount
from sqla_inspect.csv import CsvExporter


SAGE_COMPATIBLE_ENCODING = 'cp1252'


class SageCsvWriter(CsvExporter):
    """
        Write Sage csv files
        :param datas: The datas to export list of dict
        :param headers: The translation tuple between input and output column
        names
    """
    extension = "txt"
    delimiter = ";"
    headers = ()
    amount_precision = 2

    def __init__(self, *args):
        CsvExporter.__init__(self, encoding=SAGE_COMPATIBLE_ENCODING)

    def format_debit(self, debit):
        """
            Format the debit entry to get a clean float in our export
            12000 => 120,00
        """
        if debit == '':
            return 0
        else:
            return format_amount(
                debit,
                grouping=False,
                precision=self.amount_precision
            )

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
    amount_precision = 5
    headers = (
        {'name': 'num_facture', 'label': "Numéro de pièce", },
        {'name': 'code_journal', 'label': "Code Journal"},
        {'name': 'date', 'label': "Date de pièce"},
        {'name': 'compte_cg', 'label': "N° compte général"},
        {'name': 'num_facture', 'label': "Numéro de facture"},
        {'name': 'compte_tiers', 'label': "Numéro de compte tiers"},
        {'name': 'code_tva', 'label': "Code taxe"},
        {'name': 'libelle', 'label': "Libellé d'écriture"},
        {'name': 'echeance', 'label': "Date d'échéance"},
        {'name': 'debit', 'label': "Montant débit"},
        {'name': 'credit', 'label': "Montant crédit"},
        {'name': 'type_', 'label': "Type de ligne"},
        {'name': 'num_analytique', 'label': "Numéro analytique"},
    )


class SageExpenseCsvWriter(SageCsvWriter):
    """
    Expense CsvWriter
    """
    headers = (
        {'name': 'num_autonomie', 'label': "Numéro de pièce"},
        {'name': 'code_journal', 'label': "Code Journal"},
        {'name': 'date', 'label': "Date de pièce"},
        {'name': 'compte_cg', 'label': "N° compte général"},
        {'name': 'num_feuille', 'label': "Numéro de note de frais"},
        {'name': 'compte_tiers', 'label': "Numéro de compte tiers"},
        {'name': 'code_tva', 'label': "Code taxe"},
        {'name': 'libelle', 'label': "Libellé d'écriture"},
        {'name': 'debit', 'label': "Montant débit"},
        {'name': 'credit', 'label': "Montant crédit"},
        {'name': 'type_', 'label': "Type de ligne"},
        {'name': 'num_analytique', 'label': "Numéro analytique"},
        {'name': 'num_autonomie', 'label': "Référence"},
    )


class SagePaymentCsvWriter(SageCsvWriter):
    """
    Payment csv writer
    """
    amount_precision = 5
    headers = (
        {'name': 'reference', 'label': "Référence"},
        {'name': 'code_journal', 'label': "Code Journal"},
        {'name': 'date', 'label': "Date de pièce"},
        {'name': 'compte_cg', 'label': "N° compte général"},
        {'name': 'mode', "label": "Mode de règlement"},
        {'name': 'compte_tiers', 'label': "Numéro de compte tiers"},
        {'name': 'code_taxe', 'label': "Code taxe"},
        {'name': 'libelle', 'label': "Libellé d'écriture"},
        {'name': 'debit', 'label': "Montant débit"},
        {'name': 'credit', 'label': "Montant crédit"},
        {'name': 'type_', 'label': "Type de ligne"},
        {'name': 'num_analytique', 'label': "Numéro analytique"},
    )


class SageExpensePaymentCsvWriter(SageCsvWriter):
    headers = (
        {'name': 'reference', 'label': "Référence"},
        {'name': 'code_journal', 'label': "Code Journal"},
        {'name': 'date', 'label': "Date de pièce"},
        {'name': 'compte_cg', 'label': "N° compte général"},
        {'name': 'mode', "label": "Mode de règlement"},
        {'name': 'compte_tiers', 'label': "Numéro de compte tiers"},
        {'name': 'code_taxe', 'label': "Code taxe"},
        {'name': 'libelle', 'label': "Libellé d'écriture"},
        {'name': 'debit', 'label': "Montant débit"},
        {'name': 'credit', 'label': "Montant crédit"},
        {'name': 'type_', 'label': "Type de ligne"},
        {'name': 'num_analytique', 'label': "Numéro analytique"},
    )
