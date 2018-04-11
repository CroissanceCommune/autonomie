# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def test_admin_activities_get_edited_elements(config, dbsession,
                                              get_csrf_request_with_db):
    from autonomie.views.admin.accompagnement import BaseAdminAccompagnement
    obj = BaseAdminAccompagnement(get_csrf_request_with_db())
    datas = {
        'tests': [
            {'id': 5},
            {'id': 4},
            {},
        ]
    }
    res = obj.get_edited_elements(datas, 'tests')
    assert set(res.keys()) == set([5, 4])
