# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
def invoice(
    dbsession,
    tva,
    unity,
    project,
    customer,
    company,
    user,
    phase,
):
    from autonomie.models.task.invoice import Invoice
    invoice = Invoice(
        company=company,
        project=project,
        customer=customer,
        phase=phase,
        user=user,
    )
    dbsession.add(invoice)
    dbsession.flush()
    return invoice


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
    invoice.payment_conditions = u"Test"
    invoice.description = u"Description"
    invoice = dbsession.merge(invoice)
    dbsession.flush()
    return invoice


@pytest.fixture
def full_cancelinvoice(
    dbsession, cancelinvoice, full_invoice, task_line_group, task_line, user,
    mention, discount_line
):
    # TTC  : -1 * (120 - 12  + 12 €)
    cancelinvoice.invoice_id = full_invoice.id
    task_line.cost = -1 * task_line.cost
    task_line_group.lines = [task_line]
    cancelinvoice.line_groups = [task_line_group]
    cancelinvoice.discounts = [discount_line]
    cancelinvoice.workplace = u'workplace'
    cancelinvoice.mentions = [mention]
    cancelinvoice.expenses_ht = 1000000
    cancelinvoice.payment_conditions = u"Test"
    cancelinvoice.description = u"Description"
    cancelinvoice = dbsession.merge(cancelinvoice)
    dbsession.flush()
    return cancelinvoice
