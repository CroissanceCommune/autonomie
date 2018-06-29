from mock import Mock
import cStringIO as StringIO

from autonomie.export.sage import SageCsvWriter
from autonomie.models.config import Config


def test_sage_csv_writer(dbsession):
    class TestCSVWriter(SageCsvWriter):
        headers = (
            {'name': 'libelle', 'label': 'test libelle'},
        )

    def mk_test_csv_writer():
        request = Mock()
        request.config = Config
        w = TestCSVWriter(request=request, context=None)
        w.set_datas([
            {'libelle': '123456789'},
        ])
        return w

    # default (no conf)
    buf = mk_test_csv_writer().render(StringIO.StringIO())
    buf.readline()  # header
    assert buf.readline().strip() == '"123456789"'

    # zero
    Config.set('accounting_label_maxlength', '0')
    buf = mk_test_csv_writer().render(StringIO.StringIO())
    buf.readline()  # header
    assert buf.readline().strip() == '"123456789"'

    # lower than size
    Config.set('accounting_label_maxlength', '1')
    buf = mk_test_csv_writer().render(StringIO.StringIO())
    buf.readline()  # header
    assert buf.readline().strip() == '"1"'

    # bigger than size
    Config.set('accounting_label_maxlength', '11')
    buf = mk_test_csv_writer().render(StringIO.StringIO())
    buf.readline()  # header
    assert buf.readline().strip() == '"123456789"'
