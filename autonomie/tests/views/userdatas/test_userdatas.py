# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def test_userdatas_add_entry_point(config, get_csrf_request_with_db):
    from autonomie.views.userdatas.userdatas import userdatas_add_entry_point
    config.add_route('/users', '/users')

    req = get_csrf_request_with_db()
    res = userdatas_add_entry_point(None, req)

    assert res.location == '/users?action=add'

    assert req.session['user_form']['callback_urls'] == \
        ['/users/{id}/userdatas/add']
    assert req.session['user_form']['defaults']['primary_group'] == 'contractor'


def test_userdatas_add_view(config, user, get_csrf_request_with_db):
    from autonomie.views.userdatas.userdatas import userdatas_add_view
    from autonomie.models.user.userdatas import UserDatas
    config.add_route('/users/{id}/userdatas/edit', '/users/{id}/userdatas/edit')
    req = get_csrf_request_with_db()
    req.context = user

    result = userdatas_add_view(user, req)
    assert result.code == 302
    assert result.location == "/users/{0}/userdatas/edit".format(user.id)
    userdatas = UserDatas.query().filter_by(user_id=user.id).one()

    assert userdatas.coordonnees_civilite == user.civilite
    assert userdatas.coordonnees_lastname == user.lastname
    assert userdatas.coordonnees_firstname == user.firstname
    assert userdatas.coordonnees_email1 == user.email


def test_ensure_doctypes_rel(
    userdatas, social_doctypes, get_csrf_request_with_db
):
    from autonomie.views.userdatas.userdatas import ensure_doctypes_rel

    req = get_csrf_request_with_db()
    ensure_doctypes_rel(userdatas.id, req)

    assert len(userdatas.doctypes_registrations) == len(social_doctypes)


class TestUserDatasEditView:
    def _get_view(self, userdatas, get_csrf_request_with_db, post={}):
        from autonomie.views.userdatas.userdatas import UserDatasEditView
        req = get_csrf_request_with_db(
            current_route_path='/users',
            post=post
        )
        req.context = userdatas

        view = UserDatasEditView(req)
        return view

    def test_success(self, userdatas, get_csrf_request_with_db):
        view = self._get_view(
            userdatas,
            get_csrf_request_with_db,
            post={
                "submit": True,
                "coordoonnees_civilite": userdatas.coordonnees_civilite,
                "coordonnees_lastname": u"New nameéé",
                "coordonnees_firstname": userdatas.coordonnees_firstname,
                "coordonnees_email1": userdatas.coordonnees_email1,
                "coordonnees_email2": "second@mail.fr"
            }
        )
        res = view.__call__()
        assert res.code == 302
        assert userdatas.coordonnees_email2 == "second@mail.fr"
        assert userdatas.coordonnees_lastname == u"New nameéé"

    def test_error(self, userdatas, get_csrf_request_with_db):
        # Missing mandatory arguments
        view = self._get_view(
            userdatas,
            get_csrf_request_with_db,
            post={
                "submit": True,
                "coordonnees_lastname": u"New nameéé",
                "coordonnees_email2": "second@mail.fr"
            }
        )

        res = view.__call__()
        assert res['formerror'] == True


class TestUserUserDatasEditView:
    def _get_view(self, user, get_csrf_request_with_db, post={}):
        from autonomie.views.userdatas.userdatas import UserUserDatasEditView
        req = get_csrf_request_with_db(
            current_route_path='/users',
            post=post
        )
        req.context = user

        view = UserUserDatasEditView(req)
        return view

    def test_success(self, user, userdatas, get_csrf_request_with_db):
        view = self._get_view(
            user,
            get_csrf_request_with_db,
            post={
                "submit": True,
                "coordoonnees_civilite": userdatas.coordonnees_civilite,
                "coordonnees_lastname": u"New nameéé",
                "coordonnees_firstname": userdatas.coordonnees_firstname,
                "coordonnees_email1": userdatas.coordonnees_email1,
                "coordonnees_email2": "second@mail.fr"
            }
        )
        res = view.__call__()
        assert res.code == 302
        assert userdatas.coordonnees_email2 == "second@mail.fr"
        assert userdatas.coordonnees_lastname == u"New nameéé"

    def test_error(self, user, userdatas, get_csrf_request_with_db):
        # Missing mandatory arguments
        view = self._get_view(
            user,
            get_csrf_request_with_db,
            post={
                "submit": True,
                "coordonnees_lastname": u"New nameéé",
                "coordonnees_email2": "second@mail.fr"
            }
        )

        res = view.__call__()
        assert res['formerror'] == True


class TestUserDatasDeleteView:
    def test_success(self, config, user, userdatas, get_csrf_request_with_db):
        from autonomie.views.userdatas.userdatas import UserDatasDeleteView
        from autonomie.models.user.userdatas import UserDatas

        config.add_route('/users/{id}', '/users/{id}')
        req = get_csrf_request_with_db()
        req.context = userdatas

        udatas_id = userdatas.id

        view = UserDatasDeleteView(req)
        res = view.__call__()
        req.dbsession.flush()
        assert res.code == 302
        assert res.location == "/users/%s" % user.id

        assert UserDatas.get(udatas_id) is None


class TestUserDatasDocTypeView:
    def test_success(
        self, userdatas, get_csrf_request_with_db, social_doctypes
    ):
        from autonomie.views.userdatas.userdatas import (
            UserDatasDocTypeView,
        )

        req = get_csrf_request_with_db(
            current_route_path="/users",
            post={
                "submit": True,
                "node_0": {
                    "userdatas_id": str(userdatas.id),
                    "doctype_id": str(social_doctypes[0].id),
                    "status": "true"
                },
                "node_1": {
                    "userdatas_id": str(userdatas.id),
                    "doctype_id": str(social_doctypes[1].id),
                    "status": "false"
                },
            }
        )
        req.context = userdatas

        view = UserDatasDocTypeView(req)
        res = view.__call__()

        assert res.code == 302
        assert res.location == "/users"
        assert userdatas.doctypes_registrations[0].status is True
