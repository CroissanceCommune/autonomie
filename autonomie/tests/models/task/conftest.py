# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest


@pytest.fixture
def tva(dbsession):
    from autonomie.models.tva import Tva
    tva = Tva(value=2000, name='20%')
    dbsession.add(tva)
    dbsession.flush()
    return tva


@pytest.fixture
def product(tva, dbsession):
    from autonomie.models.tva import Product
    product = Product(name='product', compte_cg='122', tva_id=tva.id)
    dbsession.add(product)
    dbsession.flush()
    return product


@pytest.fixture
def product_without_tva(dbsession):
    from autonomie.models.tva import Product
    product = Product(name='product', compte_cg='122')
    dbsession.add(product)
    dbsession.flush()
    return product


@pytest.fixture
def unity(dbsession):
    from autonomie.models.task.unity import WorkUnit
    print([w.label for w in WorkUnit.query()])
    unity = WorkUnit(label=u"Mètre")
    dbsession.add(unity)
    dbsession.flush()
    return unity


@pytest.fixture
def mention(dbsession):
    from autonomie.models.task.mentions import TaskMention
    mention = TaskMention(
        title=u"TaskMention tet",
        full_text=u"blabla",
        label=u"bla",
    )
    dbsession.add(mention)
    dbsession.flush()
    return mention


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
