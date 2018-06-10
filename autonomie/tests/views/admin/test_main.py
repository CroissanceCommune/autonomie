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


@pytest.fixture
def file_type(dbsession):
    from autonomie.models.files import FileType
    f = FileType(label=u"Label")
    dbsession.add(f)
    dbsession.flush()
    return f


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


def test_admin_contact_success(config, get_csrf_request_with_db, dbsession):
    from autonomie.views.admin.main.contact import (
        AdminContactView,
        MAIN_CONTACT_ROUTE,
    )
    config.add_route(MAIN_CONTACT_ROUTE, MAIN_CONTACT_ROUTE)
    appstruct = {'cae_admin_mail': 'admin@cae.fr'}
    view = AdminContactView(get_csrf_request_with_db())
    view.submit_success(appstruct)
    assert get_config()['cae_admin_mail'] == u'admin@cae.fr'


def test_file_type_add(config, get_csrf_request_with_db, dbsession):
    from autonomie.views.admin.main.file_types import (
        FileTypeAddView,
    )
    from autonomie.models.files import FileType
    appstruct = {
        'label': u"Label",
    }
    view = FileTypeAddView(
        get_csrf_request_with_db()
    )
    view.submit_success(appstruct)
    element = FileType.get_by_label("Label")
    assert element is not None


def test_file_type_edit(config, get_csrf_request_with_db, dbsession, file_type):
    from autonomie.views.admin.main.file_types import (
        FileTypeEditView,
    )
    appstruct = {
        'label': u"New label",
    }
    req = get_csrf_request_with_db()
    req.context = file_type
    view = FileTypeEditView(req)
    view.submit_success(appstruct)
    assert req.context.label == u"New label"


def test_file_type_disable(config, get_csrf_request_with_db, dbsession,
                           file_type):
    from autonomie.views.admin.main.file_types import (
        FileTypeDisableView,
    )
    req = get_csrf_request_with_db()
    req.context = file_type
    view = FileTypeDisableView(req)
    view()
    assert not file_type.active


def test_file_type_delete(config, get_csrf_request_with_db, dbsession,
                          file_type):
    from autonomie.views.admin.main.file_types import (
        FileTypeDeleteView,
    )
    from autonomie.models.files import FileType
    fid = file_type.id
    req = get_csrf_request_with_db()
    req.context = file_type
    view = FileTypeDeleteView(req)
    view()
    dbsession.flush()

    assert FileType.get(fid) is None
