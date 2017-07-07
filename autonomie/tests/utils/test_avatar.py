# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def test_avatar(dbsession, config, get_csrf_request, user):
    from autonomie.utils.avatar import get_avatar
    config.testing_securitypolicy(userid="login")
    request = get_csrf_request()
    request.dbsession = dbsession
    avatar = get_avatar(request)
    assert avatar.lastname == "Lastname"
