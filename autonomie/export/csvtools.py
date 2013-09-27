# -*- coding: utf-8 -*-
# * File Name : csvtools.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 08-09-2010
# * Last Modified :
#
# * Project :
#
"""
    Csv exporter for sqlalchemy datas

    uses the sqlalchemy info attr to retrieve meta datas about the columns
"""
import csv
import cStringIO as StringIO
from autonomie.utils.sqla import get_columns
from autonomie.utils.ascii import (
        force_ascii,
        force_utf8,
        )


CSV_DELIMITER = ';'
CSV_QUOTECHAR = '"'


def get_column_label(column):
    """
        Return the label of a column
    """
    return column.info.get('label', column.name)


def should_be_exported(column):
    """
        Check if the column should be part of the export
        Default True
        Add info['options']['csv_exclude'] to avoid the export of the given
        field
    """
    return not column.info.get('options', {}).has_key('csv_exclude')


def collect_labels(model):
    """
        collect the column labels our dest file is supposed to provide
    """
    for column in get_columns(model):
        if should_be_exported(column):
            yield get_column_label(column)


def collect_keys(model):
    """
        Return the different column keys
    """
    for column in get_columns(model):
        if should_be_exported(column):
            yield column.name


class BaseCsvWriter(object):
    keys = []
    delimiter = CSV_DELIMITER
    quotechar = CSV_QUOTECHAR

    def __init__(self, datas=None):
        self._datas = []
        if datas is not None:
            for data in datas:
                self.add_row(data)

    @staticmethod
    def format_row(row):
        return row

    def add_row(self, row):
        """
            Add a row to our buffer
        """
        self._datas.append(self.format_row(row))

    def render(self):
        """
            Write to the dest buffer
        """
        f_buf = StringIO.StringIO()
        outfile = csv.DictWriter(f_buf,
                                 self.keys,
                                 delimiter=self.delimiter,
                                 quotechar=self.quotechar,
                                 quoting=csv.QUOTE_ALL)
        outfile.writeheader()
        outfile.writerows(self._datas)
        return f_buf


class SqlaToCsvWriter(BaseCsvWriter):
    """
        buffer for writing csv files
        fobj: the destination file object
        fieldnames: The fieldnames we have in our dest file
    """
    def __init__(self, model, datas):
        super(SqlaToCsvWriter).__init__(self)
        self.model = model
        self.keys = list(collect_keys(self.model))

    def format_row(self, row):
        """
            restrict the dictionnary to the current fieldnames
        """
        ret = {}
        for key, value in row.items():
            if key in self.keys:
                ret[key] = force_utf8(value)
        return ret


def write_csv_headers(request, filename):
    """
        write the headers of the csv file 'filename'
    """
    request.response.content_type = 'application/csv'
    request.response.headerlist.append(
            ('Content-Disposition',
                'attachment; filename={0}'.format(force_ascii(filename))))
    return request


def write_csv_to_request(request, filename, buf):
    """
        write a csv buffer to the current request
    """
    request = write_csv_headers(request, filename)
    request.response.write(buf.getvalue())
    return request
