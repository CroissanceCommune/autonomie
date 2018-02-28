# -*- coding: utf-8 -*-
from autonomie.tests.tools import Dummy


def test_add_user_submit_success(config, get_csrf_request_with_db):
    from autonomie.views.user.user import UserAddView
    from autonomie.models.user.user import User

    config.add_route('/users/{id}', '/users/{id}')

    appstruct = {
        "lastname": u"Lastname 1",
        "firstname": u"Firstname 1",
        "email": u"a@example.com",
        "civilite": u"Monsieur",
    }

    view = UserAddView(get_csrf_request_with_db())
    result = view.submit_success(appstruct)
    item = User.query().filter_by(lastname=u"Lastname 1").first()
    assert result.location == u"/users/%s" % item.id


def test_add_user_submit_sucess_redirect_login(
    config, get_csrf_request_with_db
):
    from autonomie.views.user.user import UserAddView
    from autonomie.models.user.user import User

    config.add_route('/users/{id}', '/users/{id}')
    config.add_route('/users/{id}/login', '/users/{id}/login')

    view = UserAddView(get_csrf_request_with_db())

    appstruct = {
        "lastname": u"Lastname 1",
        "firstname": u"Firstname 1",
        "email": u"a@example.com",
        "civilite": u"Monsieur",
        "add_login": "1"
    }
    result = view.submit_success(appstruct)
    item = User.query().filter_by(lastname=u"Lastname 1").first()
    assert result.location == u"/users/%s/login?action=add" % item.id


def test_add_user_submit_success_confirm(
    user, config, get_csrf_request_with_db
):
    from autonomie.views.user.user import UserAddView

    config.add_route('/users', '/users')
    config.add_route('/users/{id}', '/users/{id}')

    appstruct = {
        "lastname": user.lastname,
        "firstname": u"Firstname 1",
        "email": u"a@example.com",
        "civilite": u"Monsieur",
    }
    req = get_csrf_request_with_db()
    req.matched_route = Dummy(name="/users")
    view = UserAddView(req)
    result = view.submit_success(appstruct)
    assert 'confirmation_message' in result
    assert 'form' in result


def test_edit_user_submit_success(
    user, config, get_csrf_request_with_db, dbsession
):
    from autonomie.models.user.user import User
    from autonomie.views.user.user import UserEditView

    config.add_route('/users', '/users')
    config.add_route('/users/{id}', '/users/{id}')

    appstruct = {
        "lastname": user.lastname,
        "firstname": u"new firstname",
        "email": u"newadress@example.com",
        "civilite": u"Monsieur",
    }
    req = get_csrf_request_with_db()
    req.context = user
    req.matched_route = Dummy(name="/users/{id}", id=user.id)
    req.matchdict = {'id': user.id}
    view = UserEditView(req)
    view.submit_success(appstruct)

    user = dbsession.query(User).filter_by(id=user.id).first()
    assert user.firstname == u"new firstname"
    assert user.lastname == user.lastname
    assert user.email == u"newadress@example.com"


def test_user_delete(
    user, config, get_csrf_request_with_db
):
    from autonomie.views.user.user import UserDeleteView
    config.add_route('/users', '/users')
    req = get_csrf_request_with_db()
    req.context = user

    view = UserDeleteView(req)
    result = view.__call__()
    assert result.code == 302
    assert result.location == '/users'
