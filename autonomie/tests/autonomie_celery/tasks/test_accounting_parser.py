# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os
import datetime


def test_get_file_path_from_pool():
    from autonomie_celery.tasks.accounting_parser import (
        _get_file_path_from_pool
    )
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'datas')
    result = _get_file_path_from_pool(path)
    assert os.path.basename(result).startswith('2017_09_21_balance')
    result = _get_file_path_from_pool(os.path.join(path, 'unnexistingdir'))
    assert result is None


def test_parser(content):
    from autonomie_celery.tasks.accounting_parser import (
        _get_file_path_from_pool,
        Parser,
    )
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'datas')
    filepath = _get_file_path_from_pool(path)
    parser = Parser(filepath)
    file_datas = parser._get_datas_from_file_path()
    assert file_datas['date'] == datetime.date(2017, 9, 21)
    assert file_datas['extension'] in ('csv', 'slk')  # We don't know which

    # csv file is utf-8, slk file is cp1252 (default encoding used by the
    # parser)
    if file_datas['extension'] == 'csv':
        parser.encoding = 'utf-8'
    num_operations = len(file(filepath, 'rb').read().strip().splitlines())
    assert len(parser._fill_db(file_datas)[0].operations) == num_operations

    if file_datas['extension'] == 'csv':
        parser.file_path = u"%s.slk" % parser.file_path[:-4]
        file_datas['extension'] = 'slk'

    elif file_datas['extension'] == 'slk':
        parser.file_path = u"%s.csv" % parser.file_path[:-4]
        file_datas['extension'] = 'csv'

    assert len(parser._fill_db(file_datas)[0].operations) == num_operations

