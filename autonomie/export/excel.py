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
    Data export module
"""

import itertools
import logging
from openpyxl.styles import (
    Color,
    fills,
    Style,
    NumberFormat,
    PatternFill,
    Font,
)

from string import ascii_uppercase


from sqla_inspect.excel import XlsWriter
from autonomie.compute.math_utils import integer_to_amount
from autonomie.models.treasury import ExpenseType
from autonomie.models.treasury import ExpenseKmType
from autonomie.models.treasury import ExpenseTelType
from autonomie.export.utils import write_file_to_request


log = logging.getLogger(__name__)

Color.LightCyan = "FFE0FFFF"
Color.LightCoral = "FFF08080"
Color.LightGreen = "FF90EE90"
Color.Crimson = "FFDC143C"
Color.header = "FFD9EDF7"
Color.footer = "FFFCF8E3"

EXCEL_NUMBER_FORMAT = '0.00'

TITLE_STYLE = Style(font=Font(size=24, bold=True))
HEADER_STYLE = Style(
    font=Font(bold=True),
    fill=PatternFill(
        fill_type=fills.FILL_SOLID,
        start_color=Color(rgb=Color.header)
    )
)
BOLD_CELL = Style(
    font=Font(bold=True)
)
NUMBER_CELL = Style(
    number_format=NumberFormat(format_code=EXCEL_NUMBER_FORMAT)
)
FOOTER_CELL = Style(
    font=Font(bold=True),
    fill=PatternFill(
        fill_type=fills.FILL_SOLID,
        start_color=Color(rgb=Color.footer)
    ),
    number_format=NumberFormat(format_code=EXCEL_NUMBER_FORMAT)
)
LARGE_FOOTER_CELL = Style(
    font=Font(bold=True, size=16),
    fill=PatternFill(
        fill_type=fills.FILL_SOLID,
        start_color=Color(rgb=Color.footer)
    ),
    number_format=NumberFormat(format_code=EXCEL_NUMBER_FORMAT)
)


# A, B, C, ..., AA, AB, AC, ..., ZZ
ASCII_UPPERCASE = list(ascii_uppercase) + list(
    ''.join(duple)
    for duple in itertools.combinations_with_replacement(ascii_uppercase, 2)
    )


class Column(object):
    """
    A column object
    """
    def __init__(self, label, letter=None, last_letter=None):
        self.label = label
        self.code = ""
        self.ht = 0
        self.force_visible = False
        self.additional_cell_nb = None
        self.style = None
        self.set_letter(letter, last_letter)

    def set_letter(self, start, end=None):
        self.start = start
        self.end = end or start

    @property
    def start_letter(self):
        return self.start

    @property
    def end_letter(self):
        return self.end

    def reset_ht(self):
        self.ht = 0


class StaticColumn(Column):
    """
    A static column object representing static datas representation
    """
    static = True
    def __init__(
        self,
        label,
        key,
        formatter=None,
        style=None,
        nb_col=None,
        letter=None,
        last_letter=None
    ):
        Column.__init__(self, label, letter, last_letter)
        self.key = key
        self.formatter = formatter
        self.style = style
        self.additional_cell_nb = nb_col

    def get_val(self, line):
        val = getattr(line, self.key, "")
        if self.formatter is not None:
            val = self.formatter(val)
        return val



class TypedColumn(Column):
    static = False
    def __init__(
        self,
        type_object,
        label=None,
        letter=None,
        last_letter=None
    ):
        if label is None:
            label = type_object.label

        Column.__init__(self, label)
        self.id = type_object.id
        self.code = type_object.code
        self.set_letter(letter, last_letter)

    def get_val(self, line):
        if hasattr(line, 'ht'):
            val = integer_to_amount(line.ht)
        else:
            val = integer_to_amount(line.total)
        # Le total_ht s'affiche en bas de page en mode calculée
        self.ht += integer_to_amount(line.total_ht)
        return val


EXPENSEKM_COLUMNS = [
    StaticColumn(
        key='date',
        label=u'Date',
        letter='A',
    ),
    StaticColumn(
        key='vehicle',
        label=u'Type de véhicule',
        letter='B',
        last_letter='C'
    ),
    StaticColumn(
        key='start',
        label=u'Lieu de départ',
        letter='D',
        last_letter='E',
    ),
    StaticColumn(
        key='end',
        label=u"Lieu d'arrivée",
        letter='F',
        last_letter='G',
    ),
    StaticColumn(
        key='description',
        label=u'Description/Mission',
        letter='H',
        last_letter='J',
    ),
    StaticColumn(
        formatter= integer_to_amount,
        key='km',
        label=u'Nombre de kms',
        letter='K',
    ),
    StaticColumn(
        formatter=integer_to_amount,
        key='total',
        label=u'Indemnités',
        letter='L',
        style=NUMBER_CELL,
    )
]


class XlsExpense(XlsWriter):
    """
        Xls exporter of an expensesheet object

        Provide two sheets : the expenses and the kilometric datas
    """
    title = "NDF"

    def __init__(self, expensesheet):
        XlsWriter.__init__(self)
        self.model = expensesheet
        self.columns = self.get_columns()
        self.index = 2

    def get_merged_cells(self, start, end):
        """
            returned merged cells of the current line index
        """
        cell_gap = '{1}{0}:{2}{0}'.format(self.index, start, end)
        self.worksheet.merge_cells(cell_gap)
        cell = self.worksheet.cell('{1}{0}'.format(self.index, start))
        return cell

    def get_tel_column(self):
        """
        Return the columns associated to telephonic expenses
        """
        teltype = ExpenseTelType.query().first()
        col = None
        if teltype:
            # Tel expenses should be visible
            col = TypedColumn(teltype, label=u"Téléphonie")
            if teltype.initialize:
                col.force_visible = True
        return col

    def get_km_column(self):
        """
        Return the columns associated to km expenses
        """
        kmtype = ExpenseKmType.query().first()
        col = None
        if kmtype:
            col = TypedColumn(
                kmtype,
                label=u"Frais de déplacement",
            )
        return col

    def get_disabled_types_columns(self):
        """
        """
        types = []
        for line in self.model.lines:
            type_ = line.type_object
            if not type_.active and type_.type != 'expensetel':
                if type_.id not in types:
                    types.append(type_.id)
                    yield TypedColumn(
                        type_,
                        label="%s (ce type de frais n'existe plus)" % (
                            type_.label
                        )
                    )

    def get_columns(self):
        """
            Retrieve all columns and define a global column attribute
            :param internal: are we asking columns for internal expenses
        """
        columns = []
        # Add the two first columns
        columns.append(StaticColumn(label='Date', key='date'))
        columns.append(
            StaticColumn(
                label='Description',
                key='description',
                nb_col=3
            )
        )

        # Telephonic fees are only available as internal expenses
        tel_column = self.get_tel_column()
        if tel_column is not None:
            columns.append(tel_column)

        km_column = self.get_km_column()
        if km_column:
            columns.append(km_column)
            kmtype_code = km_column.code
        else:
            kmtype_code = None

        commontypes = ExpenseType.query()\
                .filter(ExpenseType.type=="expense")\
                .filter(ExpenseType.active==True)
        for type_ in commontypes:
            # Here's a hack to allow to group km fee types and displacement fees
            if kmtype_code is not None and \
               type_.code != kmtype_code:
                columns.append(TypedColumn(type_))

        columns.extend(self.get_disabled_types_columns())

        # Add the last columns
        columns.append(
            StaticColumn(
                label='Tva',
                key='tva',
                formatter=integer_to_amount
            )
        )
        columns.append(
            StaticColumn(
                label="Total",
                key="total",
                formatter=integer_to_amount,
                style=NUMBER_CELL,
            )
        )

        # We set the appropriate letter to each column
        index = 0
        for col in columns:
            letter = ASCII_UPPERCASE[index]
            additional_cell_nb = col.additional_cell_nb
            if additional_cell_nb:
                last_letter = ASCII_UPPERCASE[index + additional_cell_nb]
                index += additional_cell_nb + 1
            else:
                last_letter = letter
                index += 1
            col.set_letter(letter, last_letter)
        return columns

    def write_code(self):
        """
            write the company code in the header
        """
        code = self.model.company.code_compta
        if not code:
            code = u"Code non renseigné"
        cell = self.get_merged_cells('A', 'D')
        cell.value = u"Code analytique de l'entreprise"
        cell = self.get_merged_cells('E', 'J')
        cell.value = code
        self.index += 1

    def write_user(self):
        """
            write the username in the header
        """
        user = self.model.user
        title = u"%s %s" % (user.lastname, user.firstname)
        cell = self.get_merged_cells('A', 'D')
        cell.value = u"Nom de l'entrepreneur"
        cell = self.get_merged_cells('E', 'J')
        cell.value = title
        self.index += 1

    def write_period(self):
        """
            write the period in the header
        """
        period = "01/{0}/{1}".format(self.model.month,
                self.model.year)
        cell = self.get_merged_cells('A', 'D')
        cell.value = u"Période de la demande"
        cell = self.get_merged_cells('E', 'J')
        cell.value = period
        self.index += 2

    def get_column_cell(self, column):
        """
            Return the cell corresponding to a given column
        """
        letter = column.start_letter
        last_letter = column.end_letter
        return self.get_merged_cells(letter, last_letter)

    def write_table_header(self, columns):
        """
            Write the table's header and its subheader
        """
        for column in columns:
            cell = self.get_column_cell(column)
            cell.style = HEADER_STYLE
            cell.value = column.label
        self.index += 1
        for column in columns:
            cell = self.get_column_cell(column)
            cell.style = BOLD_CELL
            cell.value = column.code
        self.index += 1

    def get_formatted_cell_val(self, line, column):
        """
        For a given expense line, check if a value should be provided in the
        given column
        """
        val = ""

        if line.type_object is not None and column.static:
            val = column.get_val(line)

        return val

    def get_cell_val(self, line, column, by_id=True):
        """
        For a given expense line, check if a value should be provided in the
        given column

        :param obj line: a expense line object
        :param dict column: a dict describing a column
        :param bool by_id: Should the match be done by id
        :return: a value if the the given line is form the type of column ''
        """
        val = ""
        # Première passe, on essaye de retrouver le type de frais par id
        if by_id:
            if column.id == line.type_object.id:
                val = column.get_val(line)

        # Deuxième passe, on essaye de retrouver le type de frais par code
        else:
            if column.code == line.type_object.code:
                val = column.get_val(line)

        return val

    def set_col_width(self, col_letter, width, force=False):
        """
        Set the width of a given column

        :param str col_letter: the letter for the column
        :param int width: The width of the given column
        :param bool force: force the display of the column
        """
        col_dim = self.worksheet.column_dimensions.get(col_letter)
        if col_dim:
            if col_dim.width in (-1, None,) or force:
                if width == 0:
                    col_dim.hidden = True
                else:
                    col_dim.width = width
                    col_dim.hidden = False

    def write_table(self, columns, lines):
        """
        write a table with headers and content
        :param columns: list of dict
        :params lines: list of models to be written
        """
        self.write_table_header(columns)
        for line in lines:
            got_value = False

            for column in columns:
                cell = self.get_column_cell(column)

                if column.static:
                    # On récupère les valeurs pour les colonnes fixes
                    value = self.get_formatted_cell_val(
                        line,
                        column,
                    )
                else:
                    # On récupère les valeurs pour les colonnes spécifiques à
                    # chaque type de données

                    # Première passe on essaye de remplir les colonnes pour la
                    # ligne de frais données en fonction de l'id du type de
                    # frais associé
                    value = self.get_cell_val(line, column, by_id=True)
                    if value:
                        got_value = True

                cell.value = value
                if column.style:
                    cell.style = column.style

            # Deuxième passe, on a rempli aucune case pour cette ligne on va
            # essayer de remplir les colonnes en recherchant le type de frais
            # par code
            if not got_value:
                print("On fait une deuxième passe")
                print(got_value)
                print(value)
                for column in columns:
                    cell = self.get_column_cell(column)

                    if not column.static and not got_value:
                        value = self.get_cell_val(
                            line,
                            column,
                            by_id=False,
                        )
                        if value:
                            print("On a une valeur")
                            print(column)
                            got_value = True

                        cell.value = value

                        if column.style:
                            cell.style = column.style

            self.index += 1

        for column in columns:
            cell = self.get_column_cell(column)
            cell.style = FOOTER_CELL

            if not column.static:
                value = column.ht
                cell.value = value

                if value == 0 and not column.force_visible:
                    col_width = 0
                else:
                    col_width = 13
                self.set_col_width(column.start_letter, col_width)

            elif column.key == 'description':
                cell.value = "Totaux"

            elif column.key == 'tva':
                cell.value = integer_to_amount(
                    sum(
                        [
                            getattr(line, 'total_tva', 0) for line in lines
                        ]
                    )
                )

            elif column.key == 'total':
                cell.value = integer_to_amount(
                    sum(
                        [line.total for line in lines]
                    )
                )

        self.index += 4

    def write_expense_table(self, category):
        """
        write expenses tables for the given category
        """
        lines = [line for line in self.model.lines
                            if line.category == category]
        kmlines = [lin for lin in self.model.kmlines
                            if lin.category == category]
        lines.extend(kmlines)
        self.write_table(self.columns, lines)
        self.index += 2

        for column in self.columns:
            column.reset_ht()

    def write_full_line(self, txt, start="A", end="J"):
        """
        Write a full line, merging cells
        """
        cell = self.get_merged_cells(start, end)
        cell.value = txt
        self.index += 1
        return cell

    def write_internal_expenses(self):
        """
        write the internal expense table to the current worksheet
        """
        txt = u"ACHATS (frais direct de fonctionnement, < à 30% du salaire \
brut par mois)"
        cell = self.write_full_line(txt)
        self.set_color(cell, Color.Crimson)
        self.write_expense_table('1')

    def write_activity_expenses(self):
        """
        write the activity expense table to the current worksheet
        """
        txt = u"FRAIS (frais concernant directement votre l'activite aupres \
de vos clients)"
        cell = self.write_full_line(txt)
        self.set_color(cell, Color.Crimson)
        self.write_expense_table('2')

    def write_total(self):
        """
            write the final total
        """
        cell = self.get_merged_cells('A', 'D')
        cell.value = u"Total des frais professionnel à payer"
        cell.style = LARGE_FOOTER_CELL
        cell = self.get_merged_cells('E', 'E')
        cell.value = integer_to_amount(self.model.total)
        cell.style = LARGE_FOOTER_CELL
        self.index += 2

    def write_accord(self):
        """
            Write the endline
        """
        cell = self.get_merged_cells('B', 'E')
        cell.value = u"Accord après vérification"
        self.index += 1
        self.worksheet.merge_cells(
            start_row=self.index,
            end_row=self.index + 4,
            start_column=1,
            end_column=4,
        )

    def write_km_book(self):
        """
            Write the km book associated to this expenses
        """
        self.index = 3
        user = self.model.user
        title = u"Tableau de bord kilométrique de {0} {1}".\
                format(user.lastname, user.firstname)
        cell = self.write_full_line(title)
        cell.style = TITLE_STYLE

        # index has already been increased
        row_dim = self.worksheet.row_dimensions.get(self.index -1 )
        row_dim.height = 30
        self.index += 2

        self.write_table(EXPENSEKM_COLUMNS, self.model.kmlines)

    def render(self):
        """
            Return the current excel export as a String buffer (StringIO)
        """
        cell = self.write_full_line(u"Feuille de notes de frais")

        cell.style = TITLE_STYLE
        # index has already been increased
        row_dim = self.worksheet.row_dimensions.get(self.index -1 )
        row_dim.height = 30
        self.index += 2


        self.write_code()
        self.write_user()
        self.write_period()
        self.write_internal_expenses()
        self.write_activity_expenses()
        self.write_total()
        self.write_accord()

#        # We set a width to all columns that have no width set (-1)
#        for let in ASCII_UPPERCASE:
#            self.set_col_width(let, 13)
#
        self.worksheet = self.book.create_sheet()
        self.worksheet.title = u"Journal de bord"
        self.write_km_book()

        for let in ASCII_UPPERCASE:
            col_dim = self.worksheet.column_dimensions.get(let)
            if col_dim:
                col_dim.width = 13

        return self.save_book()


def make_excel_view(filename_builder, factory):
    """
        Build an excel view of a model
        :param filename_builder: a callable that take the request as arg and
            return a filename
        :param factory: the Xls factory that should be used to wrap the
            request context the factory should provide a render method
            returning a file like object
    """
    def _view(request):
        """
            the dynamically built view object
        """
        filename = filename_builder(request)
        result = factory(request.context).render()
        request = write_file_to_request(request, filename, result)
        return request.response
    return _view
