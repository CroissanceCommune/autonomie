# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest


@pytest.fixture
def invoice_base_config(dbsession):
    from autonomie.models.config import Config
    Config.set('invoice_number_template', '{SEQYEAR}')


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
def mk_task_line(dbsession, unity, tva, product, task_line_group):
    from autonomie.models.task import TaskLine

    def make(
        cost, description=u"description", unity_label=unity.label, quantity=1,
        tva_value=tva.value, group=task_line_group, product=product,
    ):
        line = TaskLine(
            cost=cost,
            quantity=quantity,
            unity=unity_label,
            tva=tva_value,
            product_id=product.id,
            group=group,
        )
        dbsession.add(line)
        dbsession.flush()
        return line
    return make


@pytest.fixture
def task_line(mk_task_line, tva, product):
    # TTC = 120 €
    return mk_task_line(cost=10000000, tva_value=tva.value, product=product)


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
        amount=15000000,
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
    discount_line, payment_line, payment_line2, mk_task_line, mk_tva, mk_product
):
    tva = mk_tva(name="7%", value=700, default=False)
    product = mk_product(name='product7', tva=tva)
    # TTC  : 100 + 20/100 * 100 + 100 + 7%*100 - 12  + 12 €
    # accompte : 10/100
    # payments : 1er paiement de 150 + solde
    task_line_group.lines = [
        task_line,
        mk_task_line(cost=10000000, tva_value=700, product=product)
    ]
    estimation.deposit = 10
    estimation.line_groups = [task_line_group]
    estimation.discounts = [discount_line]
    estimation.payment_lines = [payment_line, payment_line2]
    estimation.workplace = u'workplace'
    estimation.mentions = [mention]
    estimation.expenses_ht = 1000000
    estimation = dbsession.merge(estimation)
    estimation.manualDeliverables = 1
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
def business(dbsession, full_estimation, default_business_type):
    from autonomie.models.project.business import Business

    business = Business(name="business", business_type=default_business_type)
    business.estimations = [full_estimation]
    dbsession.add(business)
    dbsession.flush()
    full_estimation.business_type_id = default_business_type.id
    full_estimation.businesses = [business]
    dbsession.merge(full_estimation)
    return business
