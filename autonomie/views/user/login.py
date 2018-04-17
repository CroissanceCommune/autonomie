# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging

from pyramid.httpexceptions import HTTPFound

from autonomie.utils.strings import format_account
from autonomie.forms.user.login import (
    get_add_edit_schema,
    get_password_schema,
)
from autonomie.views import (
    BaseFormView,
    DisableView,
    DeleteView,
)
from autonomie.views.user.routes import (
    USER_ITEM_URL,
    USER_LOGIN_URL,
    USER_LOGIN_EDIT_URL,
    USER_LOGIN_SET_PASSWORD_URL,
    LOGIN_ITEM_URL,
    LOGIN_EDIT_URL,
    LOGIN_SET_PASSWORD_URL,
)
from autonomie.views.user.tools import UserFormConfigState


logger = logging.getLogger(__name__)


class LoginAddView(BaseFormView):
    """
    View handling login add
    """
    title = u"Ajouter des identifiants"
    schema = get_add_edit_schema()

    def __init__(self, *args, **kwargs):
        BaseFormView.__init__(self, *args, **kwargs)
        self.form_config = UserFormConfigState(self.session)

    def before(self, form):
        logger.debug(u"In the login form, defaults {0}".format(
            self.form_config.get_defaults())
        )
        form.set_appstruct(
            {
                'login': self.context.email,
                'user_id': self.context.id,
                'groups': self.form_config.get_default('groups', [])
            }
        )

    def submit_success(self, appstruct):
        password = appstruct.pop('pwd_hash', None)
        model = self.schema.objectify(appstruct)
        groups = appstruct.pop('groups', None)
        if groups:
            model.groups = groups

        model.user_id = self.context.id
        model.set_password(password)
        self.dbsession.add(model)
        self.dbsession.flush()
        print(model.login)

        next_step = self.form_config.get_next_step()
        if next_step is not None:
            redirect = self.request.route_path(
                next_step,
                id=self.context.id,
            )
        else:
            redirect = self.request.route_path(
                USER_ITEM_URL,
                id=self.context.id,
            )
        logger.debug(u"  + Login  with id {0} added".format(model.id))
        return HTTPFound(redirect)


class LoginEditView(BaseFormView):
    schema = get_add_edit_schema(edit=True)

    @property
    def title(self):
        return u"Modification des identifiants de {0}".format(
            format_account(self.context.user)
        )

    def before(self, form):
        form.set_appstruct(
            {
                'login': self.current().login,
                'groups': self.current().groups,
                'user_id': self.current().user_id,
            }
        )

    def current(self):
        return self.context

    def submit_success(self, appstruct):
        password = appstruct.pop('pwd_hash', None)
        model = self.schema.objectify(appstruct, self.current())
        groups = appstruct.pop('groups', None)
        if groups is not None:
            model.groups = groups
        if password:
            model.set_password(password)
        self.dbsession.merge(model)
        self.dbsession.flush()
        redirect = self.request.route_path(
            USER_LOGIN_URL,
            id=self.current().user_id,
        )
        logger.debug(u"  + Login  with id {0} modified".format(model.id))
        return HTTPFound(redirect)


class LoginPasswordView(LoginEditView):
    """
    Changer mon mot de passe
    """
    title = u"Modification de mot de passe"
    schema = get_password_schema()


class UserLoginEditView(LoginEditView):
    schema = get_add_edit_schema(edit=True)

    def current(self):
        return self.context.login

    @property
    def title(self):
        return u"Modification des identifiants de {0}".format(
            format_account(self.context)
        )


class UserLoginPasswordView(UserLoginEditView):
    title = u"Modification de mot de passe"
    schema = get_password_schema()


class LoginDisableView(DisableView):

    def on_disable(self):
        for company in self.context.user.companies:
            active_employees = [
                emp
                for emp in company.employees
                if hasattr(emp, 'login') and emp.login.active and
                emp.id != self.context.user.id
            ]
            if company.active and not active_employees:
                company.disable()
                self.request.dbsession.merge(company)

    def redirect(self):
        return HTTPFound(
            self.request.route_path(
                USER_LOGIN_URL,
                id=self.context.user_id,
            )
        )


class LoginDeleteView(DeleteView):
    delete_msg = u"Les identifiants ont bien été supprimés"

    def redirect(self):
        return HTTPFound(
            self.request.route_path(USER_ITEM_URL, id=self.context.user_id)
        )


def login_view(context, request):
    """
    Return the login view datas
    """
    return dict(login=context.login, title=u"Identifiants rattachés au compte")


def add_routes(config):
    for route in (LOGIN_ITEM_URL, LOGIN_EDIT_URL, LOGIN_SET_PASSWORD_URL):
        config.add_route(route, route, traverse="/logins/{id}")

    for route in (
        USER_LOGIN_URL,
        USER_LOGIN_EDIT_URL,
        USER_LOGIN_SET_PASSWORD_URL
    ):
        config.add_route(route, route, traverse="/users/{id}")


def add_views(config):
    config.add_view(
        login_view,
        route_name=USER_LOGIN_URL,
        permission="view.login",
        renderer="/user/login.mako",
        layout='user',
    )
    config.add_view(
        LoginAddView,
        route_name=USER_LOGIN_URL,
        request_param="action=add",
        permission="add.login",
        renderer="/base/formpage.mako",
        layout='default',
    )
    config.add_view(
        UserLoginEditView,
        route_name=USER_LOGIN_EDIT_URL,
        permission="edit.login",
        renderer="/user/edit.mako",
        layout='user',
    )
    config.add_view(
        LoginEditView,
        route_name=LOGIN_EDIT_URL,
        permission="edit.login",
        renderer="/base/formpage.mako",
    )
    config.add_view(
        LoginDisableView,
        route_name=LOGIN_ITEM_URL,
        request_param="action=activate",
        permission="disable.login",
        layout='user'
    )
    config.add_view(
        LoginDeleteView,
        route_name=LOGIN_ITEM_URL,
        request_param="action=delete",
        permission="delete.login",
    )
    config.add_view(
        LoginPasswordView,
        route_name=LOGIN_SET_PASSWORD_URL,
        permission="set_password.login",
        renderer="/base/formpage.mako",
        layout='default',
    )
    config.add_view(
        UserLoginPasswordView,
        route_name=USER_LOGIN_SET_PASSWORD_URL,
        permission="set_password.login",
        renderer="/user/edit.mako",
        layout='user',
    )


def includeme(config):
    add_routes(config)
    add_views(config)
