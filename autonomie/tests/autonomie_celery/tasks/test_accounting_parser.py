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
    assert result is not None
    result = _get_file_path_from_pool(os.path.join(path, 'unnexistingdir'))
    assert result is None


def test__get_parser_factory():
    from autonomie_celery.tasks.accounting_parser import (
        _get_parser_factory,
        AnalyticalBalanceParser,
        GeneralLedgerParser
    )

    assert _get_parser_factory("analytical_balance_2017_09_21_test.csv") == \
        AnalyticalBalanceParser
    assert _get_parser_factory("general_ledger_2017_09_grand_livre.csv") == \
        GeneralLedgerParser


class TestAccountingParser(object):
    def get_parser(self, extension='csv'):
        from autonomie_celery.tasks.accounting_parser import (
            AccountingDataParser,
        )
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'datas')
        filepath = os.path.join(
            path,
            'analytical_balance_2017_09_21_balance_analytique.%s' % (
                extension
            )
        )
        return AccountingDataParser(filepath)

    def test__collect_main_file_infos(self):
        parser = self.get_parser()
        assert parser._file_datas['extension'] == 'csv'
        assert parser._file_datas['md5sum'] == \
            '8ff373bbe9d80e132495b6dad047845b'
        assert parser._file_datas['basename'] == \
            'analytical_balance_2017_09_21_balance_analytique'

    def test__stream_datas(self):
        parser = self.get_parser()
        assert parser._stream_datas().next() == [
            u"0USER", u"USER1", u"218200", u"Transporté", u"5100", u" ", u"5100"
        ]
        parser = self.get_parser('slk')
        assert parser._stream_datas().next() == [
            u"0USER", u"USER1", u"218200", u"Transporté", u"5100", u" ", u"5100"
        ]


class TestAnalyticalBalanceParser(object):
    def get_parser(self):
        from autonomie_celery.tasks.accounting_parser import (
            AnalyticalBalanceParser,
        )
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'datas')
        filepath = os.path.join(
            path,
            'analytical_balance_2017_09_21_balance_analytique.csv'
        )
        return AnalyticalBalanceParser(filepath)

    def test__collect_specific_file_infos(self):
        parser = self.get_parser()
        assert parser._file_datas['date'] == datetime.date(2017, 9, 21)

    def test__build_operations(self, dbsession, company):
        parser = self.get_parser()
        num_lines = len(file(parser.file_path, 'rb').read().splitlines())

        operations, missed = parser._build_operations()
        assert len(operations) == num_lines

    def test__build_operation_upload_object(self, dbsession, company):
        parser = self.get_parser()
        assert parser._build_operation_upload_object().date == datetime.date(
            2017, 9, 21
        )


class TestGeneralLedgerParser(object):
    def get_parser(self):
        from autonomie_celery.tasks.accounting_parser import (
            GeneralLedgerParser,
        )
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'datas')
        filepath = os.path.join(
            path,
            'general_ledger_2017_09_grand_livre.csv'
        )
        return GeneralLedgerParser(filepath)

    def test__collect_specific_file_infos(self):
        parser = self.get_parser()
        assert parser._file_datas['date'] == datetime.date(2017, 9, 1)

    def test__build_operations(self, dbsession, company):
        parser = self.get_parser()
        num_lines = len(file(parser.file_path, 'rb').read().splitlines())

        operations, missed = parser._build_operations()
        assert len(operations) == num_lines

    def test__build_operation_upload_object(self, dbsession, company):
        parser = self.get_parser()
        assert parser._build_operation_upload_object().date == datetime.date(
            2017, 9, 1
        )
