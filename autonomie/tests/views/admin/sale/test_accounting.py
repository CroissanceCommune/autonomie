# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest

from autonomie.models.config import (
    get_config,
)
pytest.mark.usefixtures("config")


def test_config_cae_success(config, dbsession, get_csrf_request_with_db):
    from autonomie.views.admin.sale.accounting import (
        SaleAccountingConfigView,
        ACCOUNTING_URL,
    )

    SaleAccountingConfigView.back_link = ACCOUNTING_URL

    appstruct = {
        'compte_cg_contribution': "00000668",
        'compte_rrr': "000009558"
    }
    view = SaleAccountingConfigView(get_csrf_request_with_db())
    view.submit_success(appstruct)
    config = get_config()
    for key, value in appstruct.items():
        assert config[key] == value
