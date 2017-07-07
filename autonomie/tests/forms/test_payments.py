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
import pytest
import colander


@pytest.fixture
def mode(dbsession):
    from autonomie.models.task.invoice import PaymentMode
    mode = PaymentMode(label=u"Chèque")
    dbsession.add(mode)
    dbsession.flush()
    return mode


@pytest.fixture
def bank(dbsession):
    from autonomie.models.task.invoice import BankAccount
    bank = BankAccount(label=u"banque", code_journal='bq', compte_cg='123')
    dbsession.add(bank)
    dbsession.flush()
    return bank


def test_mode_validator(mode):
    from autonomie.forms.payments import deferred_payment_mode_validator
    c = colander.SchemaNode(colander.String())
    validator = deferred_payment_mode_validator(None, {})

    validator(c, mode.label)
    with pytest.raises(colander.Invalid):
        validator(c, u'pièce en chocolat')


def test_bank_validator(bank):
    from autonomie.forms.payments import deferred_bank_validator
    c = colander.SchemaNode(colander.String())
    validator = deferred_bank_validator(None, {})
    validator(c, bank.id)
    with pytest.raises(colander.Invalid):
        validator(c, bank.id + 1)
