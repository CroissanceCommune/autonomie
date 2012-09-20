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
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import has_permission

from deform import Form
from deform import ValidationFailure

from autonomie.models.model import User
from autonomie.models.model import Company
from autonomie.utils.forms import merge_session_with_post
from autonomie.utils.widgets import ViewLink
from autonomie.utils.widgets import SearchForm
from autonomie.utils.widgets import PopUp
from autonomie.utils.views import submit_btn
from autonomie.utils.views import cancel_btn
from autonomie.views.forms import get_password_change_schema
from autonomie.views.forms import get_user_schema
from autonomie.views.forms import get_user_del_schema
from autonomie.views.render_api import format_account

from .base import ListView

log = logging.getLogger(__name__)

@view_config(route_name='account', renderer='account.mako',
        permission='view')
def account(request):
    """
        Account handling page
    """
    avatar = request.user
    pwdformschema = get_password_change_schema()
    pwdform = Form(pwdformschema, buttons=(submit_btn,))
    html_form = pwdform.render({'login':avatar.login})
    if "submit" in request.params:
        controls = request.params.items()
        try:
            datas = pwdform.validate(controls)
        except ValidationFailure, e:
            html_form = e.render()
        else:
            log.info(u"# User {0} has changed his password #".format(
                                                    avatar.login))
            dbsession = request.dbsession()
            new_pass = datas['pwd']
            avatar.set_password(new_pass)
            dbsession.merge(avatar)
            dbsession.flush()
            request.session.flash(u"Votre mot de passe a bien été modifié",
                                                                    'main')

    return dict(title="Mon compte",
                html_form=html_form,
                account=avatar
                )

class UserView(ListView):
    """
        User related views
    """
    columns = dict(lastname=User.lastname,
                    email=User.email)
    default_sort = 'lastname'
    default_direction = 'asc'

    def __init__(self, request):
        ListView.__init__(self, request)
        self._set_actionmenu()

    def _set_actionmenu(self):
        """
            set the action menu
        """
        self.actionmenu.add(ViewLink(u"Annuaire", "view", path="users"))
        if self.context.__name__ == 'user':
            self.actionmenu.add(ViewLink(u"Voir", "view", path="user",
                                                           id=self.context.id))
            self.actionmenu.add(ViewLink(u"Éditer", "edit", path="user",
                               id=self.context.id, _query=dict(action="edit")))
            if self.context.enabled():
                self.actionmenu.add(ViewLink(u"Désactiver", "manage",
                            path="user", id=self.context.id,
                                            _query=dict(action="disable")))
            else:
                message = u"Êtes-vous sûr de vouloir supprimer ce compte ? \
Cette action n'est pas réversible."
                self.actionmenu.add(ViewLink(u"Supprimer", "manage",
                                            confirm=message,
                                            path="user",
                                            id=self.context.id,
                                            _query=dict(action="delete")))

    def _get_user_form(self, edit=False):
        """
            Return the user add form
        """
        schema = get_user_schema(self.request, edit)
        return Form(schema, buttons=(submit_btn,))

    def _get_add_popup(self):
        """
            return the add user popup
        """
        form = self._get_user_form()
        return PopUp('add', u"Ajouter un compte", form.render())

    @view_config(route_name='users', renderer='users.mako',
            permission='view')
    def directory(self):
        """
            User directory
        """
        search, sort, direction, current_page, items_per_page = \
                                                self._get_pagination_args()
        query = self._get_users()
        if search:
            query = self._filter_search(query, search)
        users = query.order_by(sort + " " + direction).all()

        records = self._get_pagination(users, current_page, items_per_page)
        ret_dict = dict(title=u"Annuaire des utilisateurs",
                        users=records,
                        action_menu=self.actionmenu)
        if has_permission('add', self.request.context, self.request):
            popup = self._get_add_popup()
            ret_dict['popups'] = {popup.name:popup}
            self.actionmenu.add(popup.open_btn())
        self.actionmenu.add(SearchForm(u"Nom ou entreprise"))
        return ret_dict

    @staticmethod
    def _get_users():
        """
            return the user query
        """
        return User.query(ordered=False).outerjoin(User.companies)

    @staticmethod
    def _filter_search(query, search):
        """
            Return a filtered query
        """
        return query.filter( or_(User.lastname.like("%"+search+"%"),
                        User.firstname.like("%"+search+"%"),
                     User.companies.any(Company.name.like("%"+search+"%"))))

    @view_config(route_name='users', renderer='user_edit.mako',
                        request_method='POST', permission='add')
    @view_config(route_name='user', renderer='user_edit.mako',
                        request_param='action=edit', permission='edit')
    def user_edit(self):
        """
            Add / Edit a user
        """
        log.debug(u"# In UserView.user_edit #")
        if self.request.context.__name__ == 'user':
            user = self.request.context
            edit = True
            title = u"Édition de {0} {1}".format(user.lastname, user.firstname)
            validate_msg = u"Le compte a bien été édité"
        else:
            user = User()
            edit = False
            title = u"Ajout d'un nouveau compte"
            validate_msg = u"Le compte a bien été ajouté"

        form = self._get_user_form(edit=edit)
        if 'submit' in self.request.params:
            datas = self.request.params.items()
            log.debug(u" + Submitted datas")
            log.debug(datas)
            try:
                app_datas = form.validate(datas)
            except ValidationFailure, errform:
                html_form = errform.render()
            else:
                # Validation OK
                # Création/édition du compte de l'utilisateur
                # Création (ou non) de la/des entreprise(s)
                # Création du lien entre les deux
                merge_session_with_post(user, app_datas['user'])
                if app_datas.has_key('password'):
                    if app_datas['password']['pwd']:
                        user.set_password(app_datas['password']['pwd'])
                #avoid creating duplicate companies at this level
                if app_datas.has_key('companies'):
                    companies = set(app_datas.get('companies'))
                    user.companies = []
                    for company_name in companies:
                        company = Company.query().filter(
                               Company.name==company_name).first()
                        if not company:
                            log.info(u" + Adding company : %s" % company_name)
                            company = Company()
                            company.name = company_name
                            company.goal = u"Entreprise de {0}".format(
                                                         format_account(user))
                            company = self.dbsession.merge(company)
                            self.dbsession.flush()
                        user.companies.append(company)
                log.info(u" + Adding/Editing user : {0}" .format(
                                                         format_account(user)))
                user = self.dbsession.merge(user)
                self.dbsession.flush()
                self.session.flash(validate_msg, queue="main")
                return HTTPFound(self.request.route_path("user", id=user.id))
        else:
            html_form = form.render({'user':user.appstruct(),
                        'companies': [comp.name for comp in user.companies]})
        return dict(title=title,
                    html_form=html_form,
                    action_menu=self.actionmenu)

    @view_config(route_name='user', renderer='user.mako', permission='view')
    def user_view(self):
        """
            User view
        """
        return dict(title=u"{0}".format(format_account(self.context)),
                    user=self.context,
                    action_menu=self.actionmenu)

    @view_config(route_name='user', renderer='user_edit.mako',
                        request_param='action=disable', permission='edit')
    def disable_user(self):
        """
            disable a user and its enteprises
        """
        log.debug(u"Disabling a user")
        schema = get_user_del_schema(self.context)
        form = Form(schema, buttons=(submit_btn, cancel_btn,))
        if "cancel" in self.request.params:
            user_view = self.request.route_path("user", id=self.context.id)
            return HTTPFound(user_view)
        elif "submit" in self.request.params:
            controls = self.request.params.items()
            try:
                datas = form.validate(controls)
            except ValidationFailure, err:
                html_form = err.render()
            else:
                log.debug(datas)
                if datas.get('companies', False):
                    self._disable_companies()
                if datas.get('disable', False):
                    self._disable_user(self.context)
                return HTTPFound(self.request.route_path("users"))
        html_form = form.render()
        title = u"Désactivation du compte {0}".format(
                                                 format_account(self.context))
        return dict(title=title,
                    html_form=html_form,
                    action_menu=self.actionmenu)

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
            self.session.flash(message, queue="main")

    def _disable_companies(self):
        """
            disable all companies related to this user
        """
        for company in self.context.companies:
            company.disable()
            self.dbsession.merge(company)
            message = u"L'entreprise '{0}' a bien été désactivée.".format(
                                                company.name)
            self.session.flash(message, queue="main")
            for employee in company.employees:
                self._disable_user(employee)

    @view_config(route_name='user', request_param='action=delete', \
                                                    permission='manage')
    def delete(self):
        """
            disable a user and its enteprises
        """
        message = u"Le compte '{0}' a bien été supprimé".format(
                                            format_account(self.context))
        err_msg = u"Erreur à la suppression du compte de '{0}'".format(
                                                format_account(self.context))
        log.debug(u"# Deleting a user #")
        try:
            self.dbsession.delete(self.context)
            self.dbsession.flush()
            self.session.flash(message, 'main')
        except:
            log.exception(u"Erreur à la suppression du compte")
            self.session.flash(err_msg, 'error')
        return HTTPFound(self.request.route_path("users"))
