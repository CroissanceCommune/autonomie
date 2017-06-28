# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def test_avatar(dbsession, config, get_csrf_request):
    from autonomie.utils.avatar import get_avatar
    config.testing_securitypolicy(userid="user1_login")
    request = get_csrf_request()
    request.dbsession = dbsession
    avatar = get_avatar(request)
    assert avatar.lastname == "user1_lastname"
