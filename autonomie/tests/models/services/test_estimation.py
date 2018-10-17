# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def test_get_common_invoice(estimation, user):
    from autonomie.models.services.estimation import EstimationInvoicingService
    common_invoice = EstimationInvoicingService._get_common_invoice(
        estimation,
        user,
    )
    for key in (
        'company',
        'customer',
        'project',
        'business_id',
        'business_type_id',
        'phase_id',
        'payment_conditions',
        'description',
        'address',
        'workplace',
        'mentions',
    ):
        assert getattr(common_invoice, key) == getattr(estimation, key)

    assert common_invoice.estimation == estimation
    assert common_invoice.status_person == user
    assert common_invoice.owner == user


def test_get_task_line():
    from autonomie.models.services.estimation import EstimationInvoicingService
    task_line = EstimationInvoicingService._get_task_line(
        100000, u"Description", tva=700
    )
    assert task_line.description == u"Description"
    assert task_line.cost == 100000
    assert task_line.tva == 700


def test_get_deposit_task_line():
    from autonomie.models.services.estimation import EstimationInvoicingService
    task_line = EstimationInvoicingService._get_deposit_task_line(
        100000, 700
    )
    assert task_line.description == u"Facture d'acompte"
    assert task_line.cost == 100000
    assert task_line.tva == 700


def test_get_deposit_task_lines(full_estimation, tva):
    from autonomie.models.services.estimation import EstimationInvoicingService
    task_lines = EstimationInvoicingService._get_deposit_task_lines(
        full_estimation
    )
    assert len(task_lines) == 2
    assert task_lines[0].cost + task_lines[1].cost == 2 * 1000000
    assert task_lines[0].tva == tva.value
    assert task_lines[1].tva == 700


def test_gen_deposit_invoice(full_estimation, user):
    from autonomie.models.services.estimation import EstimationInvoicingService
    deposit_invoice = EstimationInvoicingService.gen_deposit_invoice(
        full_estimation,
        user,
    )
    assert deposit_invoice.all_lines[0].cost \
        + deposit_invoice.all_lines[1].cost == 0.1 * full_estimation.total_ht()

    import datetime
    today = datetime.date.today()
    assert deposit_invoice.date == today


def test_get_intermediate_invoiceable_amounts(full_estimation, tva):
    from autonomie.models.services.estimation import EstimationInvoicingService
    amounts = EstimationInvoicingService._get_intermediate_invoiceable_amounts(
        full_estimation
    )
    assert 700 in amounts[0].keys()
    assert tva.value in amounts[0].keys()


def test_gen_intermediate_invoice(full_estimation, payment_line, user):
    from autonomie.models.services.estimation import EstimationInvoicingService
    invoice = EstimationInvoicingService.gen_intermediate_invoice(
        full_estimation, payment_line, user
    )

    assert invoice.total_ttc() == payment_line.amount


def test__get_all_intermediate_invoiceable_task_lines(
    full_estimation, estimation
):
    from autonomie.models.services.estimation import EstimationInvoicingService
    lines = EstimationInvoicingService.\
        _get_all_intermediate_invoiceable_task_lines(full_estimation)
    assert len(lines) == 4  # 2 pour l'acompte + 2 pour le premier paiement


def test_gen_sold_invoice(full_estimation, user):
    from autonomie.models.services.estimation import EstimationInvoicingService
    invoice = EstimationInvoicingService.gen_sold_invoice(
        full_estimation, user
    )
    lines = invoice.all_lines
    for index in range(2):
        assert lines[index].cost == full_estimation.all_lines[index].cost
        assert lines[index].tva == full_estimation.all_lines[index].tva

    assert len(lines) == 6
    assert len(invoice.discounts) == 1


def test_all_invoices(full_estimation, payment_line, user):
    from autonomie.models.services.estimation import EstimationInvoicingService
    deposit_invoice = EstimationInvoicingService.gen_deposit_invoice(
        full_estimation, user
    )
    intermediate_invoice = EstimationInvoicingService.gen_intermediate_invoice(
        full_estimation, payment_line, user
    )
    sold_invoice = EstimationInvoicingService.gen_sold_invoice(
        full_estimation, user
    )
    assert deposit_invoice.total_ht() + intermediate_invoice.total_ht() + \
        sold_invoice.total_ht() == full_estimation.total_ht()


def test_gen_invoice_ref450(full_estimation, user):
    from autonomie.models.services.estimation import EstimationInvoicingService
    sold_invoice = EstimationInvoicingService.gen_sold_invoice(
        full_estimation, user
    )

    for line in full_estimation.all_lines:
        print(line.product_id)
        print(line)

    for line in sold_invoice.all_lines:
        assert line.product_id is not None
