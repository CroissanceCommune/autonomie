# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest


def test_parser():
    from autonomie.compute.parser import NumericStringParser
    parser = NumericStringParser()
    assert parser.eval("2 * 4 / 100.0") == 0.08
    assert int(parser.eval("100.0 / 3")) == 33
    with pytest.raises(Exception):
        parser.eval("__import__('os').remove('/tmp/titi')")

