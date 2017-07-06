# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import datetime
import colander
import pytest


def test_validate_estimation_base_fail(estimation, request_with_config):
    from autonomie.forms.tasks.estimation import validate_estimation
    with pytest.raises(colander.Invalid):
        validate_estimation(estimation, request_with_config)


def test_validate_full_estimation(
    dbsession,
    estimation,
    request_with_config,
    task_line_group,
    task_line,
    payment_line
):

    from autonomie.forms.tasks.estimation import validate_estimation
    estimation.date = datetime.date.today()
    estimation.description = u"Description"
    estimation.paymentDisplay = u"SUMMARY"
    estimation.deposit = 5
    estimation.signed_status = "signed"
    task_line_group.task_id = estimation.id
    payment_line.task_id = estimation.id
    estimation.line_groups = [task_line_group]
    estimation.payment_lines = [payment_line]
    validate_estimation(estimation, request_with_config)
