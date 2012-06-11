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
from autonomie.utils.forms import get_mail_input
from autonomie.utils.forms import deferred_edit_widget

log = logging.getLogger(__name__)
@colander.deferred
def unique_login(node, value):
    """
        Test login unicity against database
    """
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
    if not kw.get('edit'):
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

def _edit_form(node, kw):
    """
        Modify the user form removing the password node if edit is True
        in the binding parameters
    """
    pass
#    if kw.get('edit'):
#        del node['password']

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

ROLES = (("-10", 'Administrateur'), ("-14", 'Membre de la coopérative'),
        ("-11", 'Entrepreneur'),)

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
    firstname = colander.SchemaNode(colander.String(),
                           title="Prénom" )
    lastname = colander.SchemaNode(colander.String(),
                            title="Nom")
    login = colander.SchemaNode(colander.String(),
                            title="Login",
                            validator=deferred_login_validator,
                            widget=deferred_edit_widget)
    email = get_mail_input(missing=u"")
    primary_group = colander.SchemaNode(colander.String(),
                        title=u"Rôle de l'utilisateur",
                        validator=colander.OneOf([x[0] for x in ROLES]),
                        widget=widget.RadioChoiceWidget(values=ROLES),
                        default="-11")

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

class FUser(colander.MappingSchema):
    """
        Schema for user add
    """
    user = FAccount(title=u"Utilisateur")
    companies = CompanySchema(title=u"Entreprise(s)",
                widget=widget.SequenceWidget(min_len=1,
                add_subitem_text_template=u"Ajouter une entreprise"))
    password = FPassword(validator=auth,
                         after_bind=_check_pwd,
                         title=u"Mot de passe")

userSchema = FUser(after_bind=_edit_form)

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
