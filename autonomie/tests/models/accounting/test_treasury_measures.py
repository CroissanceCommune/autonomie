# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;

def test_treasury_measure_type():
    from autonomie.models.accounting.treasury_measures import TreasuryMeasureType

    type_ = TreasuryMeasureType(label=u"Test", account_prefix="11,22,33")
    assert type_.match("1122334455")
    assert not type_.match("1222334455")
    assert type_.match("3322334455")

    type_ = TreasuryMeasureType(label=u"Test", account_prefix="11,-112")
    assert type_.match("11111")
    assert not type_.match("112111")
    type_ = TreasuryMeasureType(label=u"Test", account_prefix="11,")
    assert type_.match("11111")
    assert not type_.match("12")
