# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import datetime

from mock import MagicMock
import pytest


@pytest.fixture
def product_without_tva(dbsession):
    from autonomie.models.tva import Product
    product = Product(name='product', compte_cg='122')
    dbsession.add(product)
    dbsession.flush()
    return product


@pytest.fixture
def task_line_group(dbsession):
    from autonomie.models.task.task import TaskLineGroup
    group = TaskLineGroup(
        order=1,
        title=u"Group title",
        description=u"Group description",
    )
    dbsession.add(group)
    dbsession.flush()
    return group


@pytest.fixture
def task_line(dbsession, unity, tva, product, task_line_group):
    from autonomie.models.task.task import TaskLine
    # TTC = 120 €
    line = TaskLine(
        cost=10000000,
        quantity=1,
        unity=unity.label,
        tva=tva.value,
        product_id=product.id,
        group=task_line_group,
    )
    dbsession.add(line)
    dbsession.flush()
    return line


@pytest.fixture
def discount_line(dbsession, tva):
    from autonomie.models.task.task import DiscountLine
    discount = DiscountLine(
        description="Discount", amount=1000000, tva=tva.value
    )
    dbsession.add(discount)
    dbsession.flush()
    return discount


@pytest.fixture
def payment_line(dbsession):
    from autonomie.models.task.estimation import PaymentLine
    payment_line = PaymentLine(
        amount=2000000,
        description=u"Payment Line",
    )
    dbsession.add(payment_line)
    dbsession.flush()
    return payment_line


@pytest.fixture
def payment_line2(dbsession):
    from autonomie.models.task.estimation import PaymentLine
    payment_line = PaymentLine(
        amount=10000000,
        description=u"Payment Line 2",
    )
    dbsession.add(payment_line)
    dbsession.flush()
    return payment_line


@pytest.fixture
def estimation(
    dbsession,
    tva,
    unity,
    project,
    customer,
    company,
    user,
    phase,
):
    from autonomie.models.task.estimation import Estimation
    estimation = Estimation(
        company=company,
        project=project,
        customer=customer,
        phase=phase,
        user=user,
    )
    dbsession.add(estimation)
    dbsession.flush()
    return estimation


@pytest.fixture
def mk_invoice(
    dbsession,
    tva,
    unity,
    project,
    customer,
    company,
    user,
    phase,
):
    def _mk_invoice(date=None, company=company):
        from autonomie.models.task.invoice import Invoice
        invoice = Invoice(
            company=company,
            project=project,
            customer=customer,
            phase=phase,
            user=user,
            date=date,
        )
        dbsession.add(invoice)
        dbsession.flush()
        return invoice
    return _mk_invoice


@pytest.fixture
def invoice(mk_invoice):
    return mk_invoice()


@pytest.fixture
def cancelinvoice(
    dbsession,
    tva,
    unity,
    project,
    customer,
    company,
    user,
    phase,
):
    from autonomie.models.task.invoice import CancelInvoice
    cancelinvoice = CancelInvoice(
        company=company,
        project=project,
        customer=customer,
        phase=phase,
        user=user,
    )
    dbsession.add(cancelinvoice)
    dbsession.flush()
    return cancelinvoice


@pytest.fixture
def full_estimation(
    dbsession, estimation, task_line_group, task_line, user, mention,
    discount_line, payment_line, payment_line2
):
    # TTC  : 120 - 12  + 12 €
    task_line_group.lines = [task_line]
    estimation.deposit = 10
    estimation.line_groups = [task_line_group]
    estimation.discounts = [discount_line]
    estimation.payment_lines = [payment_line, payment_line2]
    estimation.workplace = u'workplace'
    estimation.mentions = [mention]
    estimation.expenses_ht = 1000000
    estimation = dbsession.merge(estimation)
    dbsession.flush()
    return estimation


@pytest.fixture
def full_invoice(
    dbsession, invoice, task_line_group, task_line, user, mention, discount_line
):
    # TTC  : 120 - 12  + 12 €
    task_line_group.lines = [task_line]
    invoice.line_groups = [task_line_group]
    invoice.discounts = [discount_line]
    invoice.workplace = u'workplace'
    invoice.mentions = [mention]
    invoice.expenses_ht = 1000000
    invoice = dbsession.merge(invoice)
    dbsession.flush()
    return invoice

@pytest.fixture
def invoice_20170707(mk_invoice):
    return mk_invoice(date=datetime.date(2017, 7, 7))

@pytest.fixture
def invoice_20170808(dbsession, mk_invoice):
    return mk_invoice(date=datetime.date(2017, 7, 7))

@pytest.fixture
def sale_product(dbsession):
    from autonomie.models.sale_product import SaleProduct
    s = SaleProduct(
        value=1.5,
        tva=2000,
        label=u"Produit du catalogue",
        description=u"Description du produit du catalogue",
        unity="m",
    )
    dbsession.add(s)
    dbsession.flush()
    return s


@pytest.fixture
def global_seq_1(dbsession, invoice):
    from autonomie.models.task.sequence_number import SequenceNumber
    s = SequenceNumber(
        sequence=SequenceNumber.SEQUENCE_INVOICE_GLOBAL,
        index=0,
        task_id=invoice.id,
    )
    dbsession.add(s)
    dbsession.flush()
    return s


@pytest.fixture
def set_seq_index(dbsession, mk_invoice, company):
    """ Initialize a year seq to a given index
    """
    from autonomie.models.task.sequence_number import SequenceNumber

    def _set_seq_index(index, year, month, sequence, company=company):
        s = SequenceNumber(
            sequence=sequence,
            index=index,
            task_id=mk_invoice(
                date=datetime.date(year, month, 1),
                company=company,
            ).id,
        )
        dbsession.add(s)
        dbsession.flush()
        return s

    return _set_seq_index


@pytest.fixture
def set_year_seq_index(dbsession, set_seq_index):
    """ Initialize a year seq to a given index
    """
    from autonomie.models.task.sequence_number import SequenceNumber

    def _set_year_seq_index(index, year):
        return set_seq_index(
            index=index,
            year=year,
            month=1,
            sequence=SequenceNumber.SEQUENCE_INVOICE_YEAR,
        )
    return _set_year_seq_index


@pytest.fixture
def set_month_seq_index(dbsession, set_seq_index):
    """ Initialize a month seq to a given index
    """
    from autonomie.models.task.sequence_number import SequenceNumber

    def _set_month_seq_index(index, year, month):
        return set_seq_index(
            index=index,
            month=month,
            year=year,
            sequence=SequenceNumber.SEQUENCE_INVOICE_MONTH,
        )
    return _set_month_seq_index


@pytest.fixture
def set_month_company_seq_index(dbsession, set_seq_index):
    """ Initialize a month seq to a given index for a given company
    """
    from autonomie.models.task.sequence_number import SequenceNumber

    def _set_month_company_seq_index(index, year, month, company):
        return set_seq_index(
            index=index,
            month=month,
            year=year,
            sequence=SequenceNumber.SEQUENCE_INVOICE_MONTH_COMPANY,
            company=company,
        )
    return _set_month_company_seq_index



@pytest.fixture
def DummySequence():
    ds = MagicMock()
    ds.get_next_index = MagicMock(return_value=12)
    return ds
