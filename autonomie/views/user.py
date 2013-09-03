# -*- coding: utf-8 -*-
# * File Name : user.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 08-06-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    User related views
"""
import logging

from sqlalchemy import or_
from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission
from pyramid.decorator import reify

from deform import Form

from autonomie.models.user import User
from autonomie.models.company import Company
from autonomie.utils.forms import merge_session_with_post
from autonomie.views.forms.utils import BaseFormView
from autonomie.utils.widgets import ViewLink
from autonomie.utils.widgets import SearchForm
from autonomie.utils.widgets import PopUp
from autonomie.utils.views import submit_btn
from autonomie.utils.views import cancel_btn
from autonomie.views.render_api import format_account
from autonomie.views.forms.user import (
        USERSCHEMA,
        UserListSchema,
        PASSWORDSCHEMA,
        UserDisableSchema,
        )

from .base import BaseListView

log = logging.getLogger(__name__)


def get_user_form(request):
    """
        Return the user add form
    """
    schema = USERSCHEMA.bind(request=request)
    return Form(schema, buttons=(submit_btn,))


class UserList(BaseListView):
    """
        List the users
        Allows to search for companies or user name
        Sorting is allowed on names and emails
    """
    title = u"Annuaire des utilisateurs"
    # The schema used to validate our search/filter form
    schema = UserListSchema()
    # The columns that allow sorting
    sort_columns = dict(name=User.lastname,
                        email=User.email)

    def query(self):
        """
            Return the main query for our list view
        """
        return User.query(ordered=False).outerjoin(User.companies)

    @staticmethod
    def filter_name_search(query, appstruct):
        """
            filter the query with the provided search argument
        """
        search = appstruct['search']
        if search:
            query = query.filter(
            or_(User.lastname.like("%" + search + "%"),
                User.firstname.like("%" + search + "%"),
                User.companies.any(Company.name.like("%" + search + "%"))))
        return query

    def populate_actionmenu(self, appstruct):
        """
            Add items to the action menu (directory link,
            add user link and popup for user with add permission ...)
        """
        populate_actionmenu(self.request)
        if has_permission('add', self.request.context, self.request):
            form = get_user_form(self.request)
            popup = PopUp("add", u'Ajouter un compte', form.render())
            self.request.popups = {popup.name: popup}
            self.request.actionmenu.add(popup.open_btn())
        searchform = SearchForm(u"Nom ou entreprise")
        searchform.set_defaults(appstruct)
        self.request.actionmenu.add(searchform)


class UserAccount(BaseFormView):
    """
        User account page providing password change
    """
    schema = PASSWORDSCHEMA
    title = u"Mon compte"

    def before(self, form):
        """
            Called before view execution
        """
        appstruct = {'login': self.request.user.login}
        form.set_appstruct(appstruct)

    def submit_success(self, appstruct):
        """
            Called on submission success
        """
        log.info(u"# User {0} has changed his password #".format(
                        self.request.user.login))
        new_pass = appstruct['pwd']
        self.request.user.set_password(new_pass)
        self.dbsession.merge(self.request.user)
        self.request.session.flash(u"Votre mot de passe a bien été modifié")


def user_view(request):
    """
        Return user view only datas
    """
    title = u"{0}".format(format_account(request.context))
    populate_actionmenu(request, request.context)
    return dict(title=title,
                user=request.context)


def user_delete(request):
    """
        disable a user and its enteprises
    """
    account = request.context
    try:
        log.debug(u"Deleting account : {0}".format(format_account(account)))
        request.dbsession.delete(account)
        request.dbsession.flush()
        message = u"Le compte '{0}' a bien été supprimé".format(
                                        format_account(account))
        request.session.flash(message)
    except:
        log.exception(u"Erreur à la suppression du compte")
        err_msg = u"Erreur à la suppression du compte de '{0}'".format(
                                            format_account(account))
        request.session.flash(err_msg, 'error')
    return HTTPFound(request.route_path("users"))


class UserDisable(BaseFormView):
    """
        Allows to disable user's and optionnaly its companies
    """
    schema = UserDisableSchema()
    buttons = (submit_btn, cancel_btn,)

    @reify
    def title(self):
        """
            title of the form
        """
        return u"Désactivation du compte {0}".format(
                                         format_account(self.request.context))

    def before(self, form):
        """
            Redirect if the cancel button was clicked
        """
        if "cancel" in self.request.POST:
            user_id = self.request.context.id
            raise HTTPFound(self.request.route_path("user", id=user_id))

    def submit_success(self, appstruct):
        """
            Disable users and companies
        """
        if appstruct.get('companies', False):
            self._disable_companies()
        if appstruct.get('disable', False):
            self._disable_user(self.request.context)
        return HTTPFound(self.request.route_path("users"))

    def _disable_user(self, user):
        """
            disable the current user
        """
        if user.enabled():
            user.disable()
            self.dbsession.merge(user)
            log.info(u"The user {0} has been disabled".format(
                                                        format_account(user)))
            message = u"L'utilisateur {0} a été désactivé.".format(
                                                        format_account(user))
            self.session.flash(message)

    def _disable_companies(self):
        """
            disable all companies related to the current user
        """
        for company in self.request.context.companies:
            company.disable()
            self.dbsession.merge(company)
            log.info(u"The company {0} has been disabled".format(company.name))
            message = u"L'entreprise '{0}' a bien été désactivée.".format(
                                                company.name)
            self.session.flash(message)
            for employee in company.employees:
                self._disable_user(employee)


class BaseUserForm(BaseFormView):
    """
        Base form view for user handling, provide common functions
    """
    schema = USERSCHEMA
    @staticmethod
    def get_user(user, appstruct):
        """
            Return the user object configured in the appstruct
        """
        user = merge_session_with_post(user, appstruct['user'])
        if 'password' in appstruct:
            if appstruct['password']['pwd']:
                user.set_password(appstruct['password']['pwd'])
        return user

    def get_company(self, name, user):
        """
            Return a company object, create a new one if needed
        """
        company = Company.query().filter(Company.name==name).first()
        #avoid creating duplicate companies
        if company is None:
            company = self.add_company(name, user)
        return company

    def add_company(self, name, user):
        """
            Add a company 'name' in the database
            ( set its goal by default )
        """
        log.info(u"Adding company : %s" % name)
        company = Company()
        company.name = name
        company.goal = u"Entreprise de {0}".format(format_account(user))
        company.contribution = self.request.config.get('contribution_cae')
        company = self.dbsession.merge(company)
        self.dbsession.flush()
        return company


class UserAdd(BaseUserForm):
    """
        User add form, automatically add companies if new one are specified
    """
    title = u"Ajout d'un nouveau compte"
    validate_msg = u"Le compte a bien été ajouté"

    def before(self, form):
        """
            populate the actionmenu before entering the view
        """
        populate_actionmenu(self.request)

    def submit_success(self, appstruct):
        """
            Add a user to the database
            Add its companies
            Add a relationship between companies and the new account
        """
        user = self.get_user(User(), appstruct)
        if 'companies' in appstruct:
            companies = set(appstruct.get('companies'))
            user.companies = []
            for company_name in companies:
                company = self.get_company(company_name, user)
                user.companies.append(company)
        log.info(u"Add user : {0}" .format(format_account(user)))
        user = self.dbsession.merge(user)
        self.dbsession.flush()
        self.session.flash(self.validate_msg)
        return HTTPFound(self.request.route_path("user", id=user.id))


class UserEdit(BaseUserForm):
    """
        User edition view
    """
    validate_msg = u"Le compte a bien été édité"

    @reify
    def title(self):
        """
            form title
        """
        return u"Édition de {0}".format(
                                        format_account(self.request.context))

    def before(self, form):
        """
            Set the context datas in the view attributes before view execution
        """
        user = self.request.context
        appstruct = {'user': user.appstruct(),
                     'companies': [comp.name for comp in  user.companies]}
        form.set_appstruct(appstruct)
        populate_actionmenu(self.request, self.request.context)

    def submit_success(self, appstruct):
        """
            Edit the database entry for the current user
        """
        user = self.get_user(self.request.context, appstruct)
        if 'companies' in appstruct:
            companies = set(appstruct.get('companies'))
            user.companies = []
            for company_name in companies:
                company = self.get_company(company_name, user)
                user.companies.append(company)
        log.info(u"Edit user : {0}" .format(format_account(user)))
        user = self.dbsession.merge(user)
        self.dbsession.flush()
        self.session.flash(self.validate_msg)
        return HTTPFound(self.request.route_path("user", id=user.id))


def populate_actionmenu(request, user=None):
    """
        populate the actionmenu
    """
    request.actionmenu.add(get_list_view_btn())
    if user:
        request.actionmenu.add(get_view_btn(user.id))
        if has_permission('edit', request.context, request):
            request.actionmenu.add(get_edit_btn(user.id))
            if user.enabled():
                request.actionmenu.add(get_disable_btn(user.id))
            else:
                request.actionmenu.add(get_del_btn(user.id))


def get_list_view_btn():
    """
        Return a link to the user list
    """
    return ViewLink(u"Annuaire", "view", path="users")

def get_view_btn(user_id):
    """
        Return a link for user view
    """
    return ViewLink(u"Voir", "view", path="user", id=user_id)

def get_edit_btn(user_id):
    """
        Return a link for user edition
    """
    return ViewLink(u"Éditer", "edit", path="user", id=user_id,
                                        _query=dict(action="edit"))

def get_disable_btn(user_id):
    """
        Return the button used to disable an account
    """
    return ViewLink(u"Désactiver", "manage", path="user", id=user_id,
                                        _query=dict(action="disable"))

def get_del_btn(user_id):
    """
        Return the button used to delete an account
    """
    message = u"Êtes-vous sûr de vouloir supprimer ce compte ? \
Cette action n'est pas réversible."
    return ViewLink(u"Supprimer", "manage", confirm=message, path="user",
                                     id=user_id, _query=dict(action="delete"))


def includeme(config):
    """
        Declare all the routes and views related to this model
    """
    config.add_route("users",
                    "/users")
    config.add_route("user",
                     "/users/{id:\d+}",
                     traverse="/users/{id}")
    config.add_route('account',
                    '/account')

    config.add_view(UserList,
                    route_name='users',
                    renderer='users.mako',
                    permission='view')
    config.add_view(user_view,
                    route_name='user',
                    renderer='user.mako',
                    permission='view')
    config.add_view(UserAdd,
                    route_name='users',
                    renderer='user_edit.mako',
                    request_method='POST',
                    permission='add')
    config.add_view(UserEdit,
                    route_name='user',
                    renderer='user_edit.mako',
                    request_param='action=edit',
                    permission='edit')
    config.add_view(UserDisable,
                    route_name='user',
                    renderer='user_edit.mako',
                    request_param='action=disable',
                    permission='edit')
    config.add_view(user_delete,
                    route_name='user',
                    request_param='action=delete',
                    permission='manage')
    config.add_view(UserAccount,
                    route_name='account',
                    renderer='account.mako',
                    permission='view')
