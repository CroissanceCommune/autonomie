# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest
from autonomie.tests.tools import DummyForm

@pytest.fixture(scope="module")
def groups(dbsession):
    from autonomie.models.user.group import Group
    groups = []
    for i in 'contractor', 'admin', 'manager':
        group = Group(name=i, label=i)
        dbsession.add(group)
        groups.append(group)
    dbsession.flush()
    return groups


class TestLoginAddView():
    def test_before(self, get_csrf_request_with_db, user):
        from autonomie.views.user.login import LoginAddView
        req = get_csrf_request_with_db()
        req.context = user

        view = LoginAddView(req)
        form = DummyForm()
        view.before(form)
        assert form.appstruct['login'] == user.email
        assert form.appstruct['user_id'] == user.id
        assert form.appstruct['groups'] == []

    def test_before_groups(
        self, config, get_csrf_request_with_db, user
    ):
        from autonomie.views.user.login import LoginAddView
        req = get_csrf_request_with_db()
        req.context = user
        req.session['user_form'] = {'defaults': {'groups': ['contractor']}}

        view = LoginAddView(req)
        form = DummyForm()
        view.before(form)
        assert form.appstruct['login'] == user.email
        assert form.appstruct['user_id'] == user.id
        assert form.appstruct['groups'] == ['contractor']

    def test_submit_success(
        self, config, get_csrf_request_with_db, user, groups,
    ):
        from autonomie.views.user.login import LoginAddView
        from autonomie.models.user.login import Login

        config.add_route('/users/{id}', '/users/{id}')
        req = get_csrf_request_with_db()
        req.context = user

        appstruct = {
            'pwd_hash': 'password',
            'login': 'test1@email.fr',
            'groups': ['contractor'],
        }

        view = LoginAddView(req)
        result = view.submit_success(appstruct)
        new_login = Login.query().filter_by(login='test1@email.fr').one()
        assert result.code == 302
        assert result.location == '/users/{0}'.format(user.id)

        assert new_login.groups == ['contractor']
        assert new_login.auth('password')

    def test_submit_success_next_step(
        self, config, get_csrf_request_with_db, user, groups,
    ):
        from autonomie.views.user.login import LoginAddView
        from autonomie.models.user.login import Login

        config.add_route('/path1/{id}', '/path1/{id}')
        config.add_route('/path2/{id}', '/path2/{id}')
        req = get_csrf_request_with_db()
        req.context = user
        req.session['user_form'] = {
            'callback_urls': ['/path1/{id}', '/path2/{id}']
        }

        appstruct = {
            'pwd_hash': 'password',
            'login': 'test1@email.fr'
        }

        view = LoginAddView(req)
        result = view.submit_success(appstruct)
        new_login = Login.query().filter_by(login='test1@email.fr').one()
        assert result.code == 302
        assert result.location == '/path2/{0}'.format(user.id)
        assert req.session['user_form']['callback_urls'] == ['/path1/{id}']

        assert new_login.auth('password')


class TestLoginEditView():

    def test_before(self, get_csrf_request_with_db, user, groups, login):
        from autonomie.views.user.login import LoginEditView
        req = get_csrf_request_with_db()
        req.context = login

        view = LoginEditView(req)
        form = DummyForm()
        view.before(form)
        assert form.appstruct['login'] == login.login
        assert form.appstruct['user_id'] == user.id

    def test_submit_success(
        self, config, get_csrf_request_with_db, user, groups, login
    ):
        from autonomie.views.user.login import LoginEditView
        config.add_route('/users/{id}/login', '/users/{id}/login')

        req = get_csrf_request_with_db()
        req.context = login

        appstruct = {
            'pwd_hash': 'new_password',
            'login': 'test1@email.fr'
        }
        view = LoginEditView(req)
        result = view.submit_success(appstruct)
        assert result.code == 302
        assert result.location == '/users/{0}/login'.format(user.id)
        assert login.login == 'test1@email.fr'

        assert login.auth('new_password')

    def test_submit_success_no_password(
        self, config, get_csrf_request_with_db, user, groups, login
    ):
        from autonomie.views.user.login import LoginEditView
        config.add_route('/users/{id}/login', '/users/{id}/login')

        req = get_csrf_request_with_db()
        req.context = login

        appstruct = {
            'pwd_hash': '',
            'login': 'test1@email.fr'
        }
        view = LoginEditView(req)
        result = view.submit_success(appstruct)
        assert result.code == 302
        assert result.location == '/users/{0}/login'.format(user.id)
        assert login.login == 'test1@email.fr'

        assert login.auth('pwd')


class TestLoginPasswordView:
    def test_submit_success(
        self, config, get_csrf_request_with_db, login
    ):
        from autonomie.views.user.login import LoginPasswordView
        config.add_route('/users/{id}/login', '/users/{id}/login')

        req = get_csrf_request_with_db()
        req.context = login

        appstruct = {
            'pwd_hash': 'new_password',
        }
        view = LoginPasswordView(req)
        result = view.submit_success(appstruct)
        assert result.code == 302
        assert result.location == '/users/{0}/login'.format(login.user_id)
        assert login.auth('new_password')

    def test_submit_success_unchanged(
        self, config, get_csrf_request_with_db, login
    ):
        from autonomie.views.user.login import LoginPasswordView
        config.add_route('/users/{id}/login', '/users/{id}/login')

        req = get_csrf_request_with_db()
        req.context = login

        appstruct = {
            'pwd_hash': '',
        }
        view = LoginPasswordView(req)
        result = view.submit_success(appstruct)
        assert result.code == 302
        assert result.location == '/users/{0}/login'.format(login.user_id)
        # Not changed
        assert login.auth('pwd')


class TestUserLoginEditView:
    def test_submit_success(
        self, config, get_csrf_request_with_db, user, groups, login
    ):
        from autonomie.views.user.login import UserLoginEditView
        config.add_route('/users/{id}/login', '/users/{id}/login')

        req = get_csrf_request_with_db()
        req.context = user

        appstruct = {
            'pwd_hash': 'new_password',
            'login': 'test1@email.fr'
        }
        view = UserLoginEditView(req)
        result = view.submit_success(appstruct)
        assert result.code == 302
        assert result.location == '/users/{0}/login'.format(login.user_id)
        assert login.login == 'test1@email.fr'


class TestLoginDisableView:
    def test_disable(self, config, login, get_csrf_request_with_db):
        from autonomie.views.user.login import LoginDisableView
        config.add_route('/users/{id}/login', '/users/{id}/login')
        req = get_csrf_request_with_db()
        req.context = login
        view = LoginDisableView(req)
        result = view()
        assert result.code == 302
        assert result.location == '/users/{0}/login'.format(login.user_id)
        assert not login.active
        # Now we reactivate again
        view()
        assert login.active


class TestLoginDeleteView:
    def test_delete(self, config, user, groups, login, get_csrf_request_with_db):
        from autonomie.views.user.login import LoginDeleteView
        from autonomie.models.user.login import Login
        config.add_route('/users/{id}', '/users/{id}')
        req = get_csrf_request_with_db()
        req.context = login

        login_id = login.id
        view = LoginDeleteView(req)
        result = view()
        assert result.code == 302
        assert result.location == '/users/{0}'.format(user.id)
        req.dbsession.flush()
        assert Login.get(login_id) is None
