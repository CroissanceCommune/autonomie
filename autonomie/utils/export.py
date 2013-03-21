# -*- coding: utf-8 -*-
# * File Name : export.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 13-03-2013
# * Last Modified :
#
# * Project :
#
"""
    Data export module
"""

import openpyxl
import cStringIO as StringIO

from autonomie.utils.string import force_ascii
from autonomie.utils.math import integer_to_amount

LETTERS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',)


class ExcelExpense(object):
    """
        Wrapper for excel export of an expense object
    """
    expense_columns = [('Date', 'date', None),
                        ('Code analytique', 'code', None),
                        ('Description', 'description', None),
                        ('HT', 'ht', integer_to_amount),
                        ('TVA', 'tva', integer_to_amount)]
    expensekm_columns = [('Date', 'date', None),
                         ('Code analytique', 'code', None),
                         ('Prestation', 'description', None),
                         ('Départ', 'start', None),
                         ('Arrivée', 'end', None),
                         ('Kms', 'km', integer_to_amount)]
    def __init__(self, expensesheet):
        self.book = openpyxl.workbook.Workbook()
        self.worksheet = self.book.worksheets[0]
        self.model = expensesheet
        self.index = 1

    def write_user(self):
        """
            write the username in the header
        """
        user = self.model.user
        title = u"Notes de frais de %s %s" % (user.lastname, user.firstname)
        self.worksheet.merge_cells('B1:E1')
        self.worksheet.cell('A1').value = u"Nom de l'entrepreneur"
        self.worksheet.cell('B1').value = title
        self.index = 2

    def write_period(self):
        """
            write the period in the header
        """
        period = "01/{0}/{1}".format(self.model.month,
                self.model.year)
        self.worksheet.cell('A2').value = u"Période de la demande"
        self.worksheet.merge_cells('B2:E2')
        self.worksheet.cell('B2').value = period
        self.index = 3

    def write_table(self, columns, lines):
        """
            write a table with headers and content
            :param columns: list of (label, model attribute, formatter) where
                formatter could be None
            :params lines: list of models to be written
        """
        for column, letter in zip(columns, LETTERS):
            cellname = "{0}{1}".format(letter, self.index)
            self.worksheet.cell(cellname).value = column[0]
        self.index += 1
        for line in lines:
            for column, letter in zip(columns, LETTERS):
                cellname = "{0}{1}".format(letter, self.index)
                val = getattr(line, column[1])
                if column[2] is not None:
                    val = column[2](val)
                self.worksheet.cell(cellname).value = val
            self.index += 1
        self.index += 1

    def write_expense_table(self, category):
        """
            write expenses tables for the given category
        """
        lines = [line for line in self.model.lines
                            if line.category == category]
        columns = self.expense_columns
        self.write_table(columns, lines)
        kmlines = [lin for lin in self.model.kmlines
                            if lin.category == category]
        columns = self.expensekm_columns
        self.write_table(columns, kmlines)

    def write_internal_expenses(self):
        """
            write the internal expense table to the current worksheet
        """
        self.write_expense_table('1')

    def write_activity_expenses(self):
        """
            write the activity expense table to the current worksheet
        """
        self.write_expense_table('2')

    def render(self):
        """
            Return the current excel export as a String buffer (StringIO)
        """
        self.write_user()
        self.write_period()
        self.write_internal_expenses()
        self.write_activity_expenses()
        result = StringIO.StringIO()
        self.book.save(result)
        return result


def write_excel_headers(request, filename):
    """
        write the headers of the excel file 'filename'
    """
    request.response.content_type = 'application/vnd.ms-excel'
    request.response.headerlist.append(
            ('Content-Disposition',
                'attachment; filename={0}'.format(force_ascii(filename))))
    return request


def write_excel(request, filename, factory):
    """
        write an excel stylesheet to the current request
        :param filename: the filename to output the document to
        :param factory: the Excel factory that should be used to wrap the
            request context the factory should provide a render method
            returning a file like object
    """
    request = write_excel_headers(request, filename)
    result = factory(request.context).render()
    request.response.write(result.getvalue())
    return request
