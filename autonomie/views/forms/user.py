# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 10-04-2012
# * Last Modified :
#
# * Project :
#
"""
    User account handling form schemas
"""
import colander
import logging

from deform import widget

from autonomie.models import DBSESSION
from autonomie.models.model import User
from autonomie.models.main import get_companies
from autonomie.views.forms.widgets import get_mail_input
from autonomie.views.forms.widgets import deferred_edit_widget

log = logging.getLogger(__name__)
def unique_login(node, value):
    """
        Test login unicity against database
    """
    log.debug(" + Testing login unicity")
    db = DBSESSION()
    result = db.query(User).filter_by(login=value).first()
    if result:
        message = u"Le login '{0}' n'est pas disponible.".format(
                                                            value)
        raise colander.Invalid(node, message)

def auth(form, value):
    """
        Check the login/password content
    """
    log.debug(u" * Authenticating")
    db = DBSESSION()
    login = value.get('login')
    log.debug(u"   +  Login {0}".format(login))
    password = value.get('password')
    result = db.query(User).filter_by(login=login).first()
    log.debug(result)
    if not result or not result.auth(password):
        log.debug(u"    - Authentication Error")
        message = u"Erreur d'authentification"
        exc = colander.Invalid(form, message)
        exc['password'] = message
        raise exc

@colander.deferred
def deferred_login_validator(node, kw):
    """
        Dynamically choose the validator user for validating the login
    """
    log.debug(" + Attaching a validator")
    if not kw.get('edit'):
        log.debug(" + attached")
        return unique_login
    return None

@colander.deferred
def deferred_pwd_validator(node, kw):
    """
        Returns auth func if check is True in the binding parameters
    """
    if kw.get('check'):
        return auth
    else:
        return None

def _check_pwd(node, kw):
    """
        modify the schema regarding if it's a self modify pass form
        or an admin modify pass form
    """
    if not kw.get('check'):
        node.validator = None
        del node['login']
        del node['password']
        node['pwd'].title = "Mot de passe"
        node['pwd'].missing = None

# Admins can do what they want
ADMIN_ROLES = [
         (u"3", u'Entrepreneur'),
         (u"1", u'Administrateur'),
         (u"2", u'Membre de la coopérative'),
        ]

# Managers can't set the admin status
MANAGER_ROLES = [(u"3", u'Entrepreneur'), (u"2", u'Membre de la coopérative'),]

@colander.deferred
def deferred_code_compta_title(node, kw):
    """
        deferred displaying last available compta code
    """
    if kw.get('code_compta'):
        return u"Le dernier code de comptabilité utilisé est {0}".format(
                                                        kw['code_compta'])
    else:
        return u"Aucun code de comptabilité n'a encore été attribué"

class FAccount(colander.MappingSchema):
    """
        Form Schema for an account creation
    """
    #account_id
    #account_pwd
    #account_lastpwd_change
    #account_status
    #account_expires
    #account_type
    #person_id
    #account_primary_group
    #account_challenge
    #account_response
    login = colander.SchemaNode(colander.String(),
                            title=u"Identifiant",
                            validator=deferred_login_validator,
                            widget=deferred_edit_widget)
    firstname = colander.SchemaNode(colander.String(),
                           title=u"Prénom" )
    lastname = colander.SchemaNode(colander.String(),
                            title=u"Nom")
    email = get_mail_input(missing=u"")
    code_compta = colander.SchemaNode(colander.String(),
                            title=u"Code compta",
                            description=deferred_code_compta_title,
                            missing="")
    primary_group = colander.SchemaNode(colander.String(),
                        title=u"Rôle de l'utilisateur",
                        validator=colander.OneOf([x[0] for x in ADMIN_ROLES]),
                        widget=widget.RadioChoiceWidget(values=ADMIN_ROLES),
                        default=u"3"
                        )

class FPassword(colander.MappingSchema):
    """
        Password modification form
    """
    login = colander.SchemaNode(colander.String(),
                                       widget=widget.HiddenWidget())
    password = colander.SchemaNode(colander.String(),
                                         widget=widget.PasswordWidget(),
                                            title="Mot de passe actuel",
                                            default=u'')
    pwd = colander.SchemaNode(colander.String(),
                        widget = widget.CheckedPasswordWidget(),
                        title="Nouveau mot de passe")

pwdSchema = FPassword(validator=auth,
                      after_bind=_check_pwd,
                      title=u'Modification de mot de passe')

@colander.deferred
def deferred_company_input(node, kw):
    """
        Deferred company list
    """
    companies = kw.get('companies')
    wid = widget.AutocompleteInputWidget(values=companies)
    return wid

class CompanySchema(colander.SequenceSchema):
    company = colander.SchemaNode(colander.String(),
                            title=u"Nom de l'entreprise",
                            widget=deferred_company_input,
                            )

class Password(colander.MappingSchema):
    """
        Schema for password set
    """
    pwd = colander.SchemaNode(colander.String(),
                validator=colander.Length(min=4),
                widget=widget.CheckedPasswordWidget(size=20),
                title=u"")

class FUser(colander.MappingSchema):
    """
        Schema for user add
    """
    user = FAccount(title=u"Utilisateur")
    companies = CompanySchema(title=u"Entreprise(s)",
                widget=widget.SequenceWidget(min_len=1,
                add_subitem_text_template=u"Ajouter une entreprise"))
    password = Password(title=u"Mot de passe")

#FPassword(validator=auth,
#                         after_bind=_check_pwd,
#                         title=u"Mot de passe")

def get_companies_choices(dbsession):
    """
        Return companies choices for autocomplete
    """
    return [comp.name for comp in get_companies(dbsession)]

def get_user_schema(request, edit):
    """
        Return the user schema
        user:the avatar of the user in the current session
    """
    schema = FUser().clone()
    user = request.user
    if user.is_admin():
        code = User.get_code_compta(request.dbsession())
        companies = get_companies_choices(request.dbsession())
        return schema.bind(edit=edit, companies=companies, code_compta=code)
    elif user.is_manager():
        companies = get_companies_choices(request.dbsession())
        code = User.get_code_compta(request.dbsession())
        # manager can't set admin rights
        roles = MANAGER_ROLES
        group = schema['user']['primary_group']
        group.validator = colander.OneOf([x[0] for x in roles])
        group.widget = widget.RadioChoiceWidget(values=roles)
        return schema.bind(edit=edit, companies=companies, code_compta=code)
    else:
        # Non admin users are limited
        del schema['user']['code_compta']
        del schema['user']['primary_group']
        del schema['companies']
        del schema['password']
        return schema.bind(edit=True)

class FAuth(colander.MappingSchema):
    """
        Schema for authentication form
    """
    login = colander.SchemaNode(colander.String(),
                                title="Identifiant")
    password = colander.SchemaNode(colander.String(),
                                   widget=widget.PasswordWidget(),
                                   title="Mot de passe")
    nextpage = colander.SchemaNode(colander.String(),
                               widget=widget.HiddenWidget())
authSchema = FAuth(title=u"Authentification", validator=auth)
