# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os
import pytest

from autonomie.tests.conftest import DATASDIR
from autonomie.models.config import (
    get_config,
)
pytest.mark.usefixtures("config")


def test_site_config_success(config, get_csrf_request_with_db, dbsession):
    from autonomie.views.admin.main.site import (
        AdminSiteView,
        MAIN_SITE_ROUTE,
    )
    from autonomie.models.config import ConfigFiles
    config.add_route(MAIN_SITE_ROUTE, MAIN_SITE_ROUTE)
    image = file(os.path.join(DATASDIR, 'entete5_1.png'), 'r')
    datas = image.read()
    size = len(datas)
    image.seek(0)
    appstruct = {
        'welcome': 'testvalue',
        'logo': {'fp': image, 'mimetype': 'image/png', 'uid': '1',
                 'name': 'F.png', 'filename': 'F.png', 'data': image,
                 'size': size}
    }
    view = AdminSiteView(get_csrf_request_with_db())
    view.submit_success(appstruct)
    dbsession.flush()
    assert get_config()['welcome'] == u'testvalue'
    assert ConfigFiles.get('logo.png').name == 'F.png'
    assert ConfigFiles.get('logo.png').getvalue() == datas
