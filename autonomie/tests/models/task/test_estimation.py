# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import datetime


def test_estimation_set_numbers(full_estimation):
    full_estimation.date = datetime.date(1969, 7, 1)
    full_estimation.set_numbers(5, 18)
    assert full_estimation.internal_number == u"Company 1969-07 D5"
    assert full_estimation.name == u"Devis 18"
    assert full_estimation.project_index == 18


def test_duplicate_estimation(full_estimation):
    newestimation = full_estimation.duplicate(
        full_estimation.owner,
        project=full_estimation.project,
        phase=full_estimation.phase,
        customer=full_estimation.customer,
    )
    for key in "customer", "address", "expenses_ht", "workplace":
        assert getattr(newestimation, key) == getattr(full_estimation, key)
    assert newestimation.status == 'draft'
    assert newestimation.project == full_estimation.project
    assert newestimation.status_person == full_estimation.owner
    assert newestimation.internal_number.startswith("Company {0:%Y-%m}".format(
        datetime.date.today()
    ))
    assert newestimation.phase == full_estimation.phase
    assert newestimation.mentions == full_estimation.mentions
    assert len(full_estimation.default_line_group.lines) == len(
        newestimation.default_line_group.lines
    )
    assert len(full_estimation.payment_lines) == len(
        newestimation.payment_lines
    )
    assert len(full_estimation.discounts) == len(newestimation.discounts)


def test_duplicate_payment_line(payment_line):
    newline = payment_line.duplicate()
    for i in ('order', 'description', 'amount'):
        assert getattr(newline, i) == getattr(payment_line, i)

    today = datetime.date.today()
    assert newline.date == today
