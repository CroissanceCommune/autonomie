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
from autonomie.utils.sqla import get_columns


CSV_DELIMITER = ','
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


class SqlaToCsvWriter:
    """
        buffer for writing csv files
        fobj: the destination file object
        fieldnames: The fieldnames we have in our dest file
    """
    def __init__(self, buf_f, model):
        self.buf_f = buf_f
        self.model = model
        self.fieldnames = list(collect_keys(self.model)) #collect_labels(self.model)
        self.keys = list(collect_keys(self.model))
        self.outfile = csv.DictWriter(self.buf_f,
                                      self.fieldnames,
                                      delimiter=CSV_DELIMITER,
                                      quotechar=CSV_QUOTECHAR,
                                      quoting=csv.QUOTE_ALL)
        self._datas = []


    def write_header(self):
        """
            Write the csv headers
        """
        self.outfile.writeheader()

    def subdict(self, dic):
        """
            restrict the dictionnary to the current fieldnames
        """
        ret = {}
        for key, value in dic.items():
            if key in self.keys:
                if isinstance(value, unicode):
                    value = value.encode('utf-8')
                ret[key] = value
        return ret

    def add_row(self, row):
        """
            Add a row to our buffer
        """
        self._datas.append(self.subdict(row))

    def has(self, row):
        """
            Is the row in our datas ?
        """
        return row in self._datas

    def save(self):
        """
            Write to the dest buffer
        """
        self.write_header()
        self.outfile.writerows(self._datas)
