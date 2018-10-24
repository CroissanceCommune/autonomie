# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import cStringIO

from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import (
    Style,
    TextProperties,
    TableCellProperties,
)
from odf.namespaces import (
    OFFICENS,
    TABLENS,
)
from odf.table import (
    TableCell,
    TableRow,
    Table,
)
from odf.text import P
from pyexcel_io import service as converter
from zope.interface import (
    implements,
)

from autonomie.interfaces import IExporter


TITLE_STYLE = Style(name="title", family="table-cell")
TITLE_STYLE.addElement(TextProperties(fontweight="bold", fontsize=16))
HEADER_STYLE = Style(name="header", family="table-cell")
HEADER_STYLE.addElement(TextProperties(fontweight="bold"))
HEADER_STYLE.addElement(TableCellProperties(backgroundcolor="#D9EDF7"))
HIGHLIGHT_STYLE = Style(name="highlight", family="table-cell")
HIGHLIGHT_STYLE.addElement(TextProperties(fontweight="bold"))
HIGHLIGHT_STYLE.addElement(TableCellProperties(backgroundcolor="#efffef"))


logger = logging.getLogger(__name__)


class OdsExporter:
    implements(IExporter)
    title = u"Export"

    def __init__(self):
        self.book = OpenDocumentSpreadsheet()
        self.book.automaticstyles.addElement(TITLE_STYLE)
        self.book.automaticstyles.addElement(HEADER_STYLE)
        self.book.automaticstyles.addElement(HIGHLIGHT_STYLE)
        self.sheet = Table(name=self.title)
        self.book.spreadsheet.addElement(self.sheet)

    def add_title(self, title, width):
        row = TableRow()
        cell = TableCell(stylename="title")
        cell.setAttrNS(TABLENS, "number-columns-spanned", width)
        cell.addElement(P(text=title))
        row.addElement(cell)
        self.sheet.addElement(row)

    def add_breakline(self):
        self._add_row(['\n'])

    def _get_cell(self, label, stylename=None):
        """
        Build a TableCell and adapt the format to the provided label format

        :param label: The data to write (int/float/bool/date/str/unicode)
        :param str stylename: One of the stylenames added in the __init__
        :returns: A TableCell instance
        """
        if stylename is not None:
            cell_to_be_written = TableCell(stylename=stylename)
        else:
            cell_to_be_written = TableCell()
        cell_type = type(label)
        cell_odf_type = converter.ODS_WRITE_FORMAT_COVERSION.get(
            cell_type,
            "string"
        )
        cell_to_be_written.setAttrNS(OFFICENS, "value-type", cell_odf_type)
        cell_odf_value_token = converter.VALUE_TOKEN.get(
            cell_odf_type,
            "value",
        )
        converter_func = converter.ODS_VALUE_CONVERTERS.get(
            cell_odf_type,
            None
        )
        if converter_func:
            label = converter_func(label)
        if cell_odf_type != 'string':
            cell_to_be_written.setAttrNS(OFFICENS, cell_odf_value_token, label)
            cell_to_be_written.addElement(P(text=label))
        else:
            lines = label.split('\n')
            for line in lines:
                cell_to_be_written.addElement(P(text=line))
        return cell_to_be_written

    def _add_row(self, labels, cell_style_name=None):
        row = TableRow()
        for label in labels:
            cell = self._get_cell(label, cell_style_name)
            row.addElement(cell)
        self.sheet.addElement(row)

    def add_headers(self, datas):
        self._add_row(datas, "header")

    def add_row(self, datas):
        self._add_row(datas)

    def add_highlighted_row(self, datas):
        self._add_row(datas, "highlight")

    def render(self, f_buf=None):
        if f_buf is None:
            f_buf = cStringIO.StringIO()
        self.book.write(f_buf)
        return f_buf
