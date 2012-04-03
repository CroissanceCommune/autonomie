# -*- coding: utf-8 -*-
# * File Name : forms.py
#
# * Copyright (C) 2012 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 28-01-2012
# * Last Modified : lun. 02 avril 2012 11:50:15 CEST
#
# * Project : autonomie
#
"""
    Colander schemas for form handling
"""
import colander
import logging
from deform import widget
from deform_bootstrap.widget import ChosenSingleWidget

from autonomie.utils.widgets import DisabledInput
from autonomie.models import DBSESSION
from autonomie.models.model import User
from autonomie.models.model import Client

log = logging.getLogger(__name__)

#FIXME : add length validators for strings
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

@colander.deferred
def unique_ccode(node, value):
    """
        Test customer code unicity
    """
    #Test unicity
    db = DBSESSION()
    result = db.query(Client).filter_by(code=value).first()
    if result:
        message = u"Le code '{0}' n'est pas disponible.".format(
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
def deferred_edit_widget(node, kw):
    """
        Dynamic assigned widget
    """
    if kw.get('edit'):
        wid = DisabledInput()
    else:
        wid = widget.TextInputWidget()
    return wid

@colander.deferred
def deferred_autocomplete_widget(node, kw):
    """
        Dynamically assign a autocomplete single select widget
    """
    choices = kw.get('choices')
    if choices:
        wid = ChosenSingleWidget(values=choices)
    else:
        wid = widget.TextInputWidget()
    return wid

@colander.deferred
def deferred_pwd_validator(node, kw):
    if kw.get('check'):
        return auth
    else:
        return None

def _edit_form(node, kw):
    if kw.get('edit'):
        del node['password']

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
    account_firstname = colander.SchemaNode(colander.String(),
                           title="Prénom" )
    account_lastname = colander.SchemaNode(colander.String(),
                            title="Nom")
    account_email = colander.SchemaNode(colander.String(),
                            title="Adresse e-mail",
                            validator=colander.Email()
                            )
    login = colander.SchemaNode(colander.String(),
                            title="Login",
                            validator=deferred_login_validator,
                            widget=deferred_edit_widget)

class FPassword(colander.MappingSchema):
    """
        Password modification form
    """
    login = colander.SchemaNode(colander.String(),
                                       widget=widget.HiddenWidget())
    password = colander.SchemaNode(colander.String(),
                                         widget=widget.PasswordWidget(),
                                            title="Mot de passe actuel")
    pwd = colander.SchemaNode(colander.String(),
                        widget = widget.CheckedPasswordWidget(),
                        title="Nouveau mot de passe")

pwdSchema = FPassword(validator=auth, after_bind=_check_pwd)

class FUser(colander.MappingSchema):
    """
        Schema for user add
    """
    user = FAccount()
    password = pwdSchema

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

class ClientSchema(colander.MappingSchema):
    """
        Schema for customer insertion
    """
    id = colander.SchemaNode(colander.String(),
                                widget=deferred_edit_widget,
                                title=u'Code',
                                validator=colander.Length(4))
    name = colander.SchemaNode(colander.String(),
                            title=u"Nom de l'entreprise",
                            validator=colander.Length(max=255))
    contactLastName = colander.SchemaNode(colander.String(),
                            title=u'Nom du contact principal',
                            validator=colander.Length(max=255))
    contactFirstName = colander.SchemaNode(colander.String(),
                        title=u"Prénom du contact principal",
                        missing=u"",
                        validator=colander.Length(max=255))
    email = colander.SchemaNode(colander.String(),
         title=u'E-mail',
         missing=u'',
         validator=colander.Email(u"Veuillez entrer une adresse email valide"))
    phone = colander.SchemaNode(colander.String(),
                                title=u'Téléphone',
                                missing=u'',
                                validator=colander.Length(max=50))
    address = colander.SchemaNode(colander.String(),
                    title=u'Adresse',
                    missing=u'',
                    validator=colander.Length(max=255))
    zipCode = colander.SchemaNode(colander.String(),
                    title=u'Code postal',
                    missing=u'',
                    validator=colander.Length(max=20))
    city = colander.SchemaNode(colander.String(),
                    title=u'Ville',
                    missing=u'',
                    validator=colander.Length(max=255))
    country = colander.SchemaNode(colander.String(),
                title=u"Pays",
                missing=u'France',
                validator=colander.Length(max=255)
                )
    intraTVA = colander.SchemaNode(colander.String(),
                    title=u"TVA intracommunautaire",
                    validator=colander.Length(max=50),
                    missing=u'')
    comments = colander.SchemaNode(colander.String(),
            widget=widget.TextAreaWidget(cols=80, rows=4),
            title=u'Commentaires',
            missing=u'')

#TODO : deform : bug #86 https://github.com/Pylons/deform/issues/86
timeinput = widget.DateInputWidget
#timeinput.options = {'dateFormat':'dd / mm / yy', "altFormat": "yy-mm-dd",
#                     "altfield"}
class ProjectSchema(colander.MappingSchema):
    """
        Schema for project
    """
    name = colander.SchemaNode(colander.String(),
            title=u"Nom du projet",
            validator=colander.Length(max=150), css_class='floatted')
    code = colander.SchemaNode(colander.String(),
            title=u"Code du projet",
            widget=deferred_edit_widget,
            validator=colander.Length(4))
    type = colander.SchemaNode(colander.String(),
            title="Type de projet",
            validator=colander.Length(max=150),
            missing=u'')
    definition = colander.SchemaNode(colander.String(),
                         widget=widget.TextAreaWidget(cols=80, rows=4),
                         title=u'Définition',
                         missing=u'')
    startingDate = colander.SchemaNode(colander.Date(),
                                        title=u"Date de début",
                                        missing=u"",
                                        widget=timeinput())
    endingDate = colander.SchemaNode(colander.Date(),
                                        title=u"Date de fin",
                                    missing=u"",
                                    widget=timeinput())
    code_client = colander.SchemaNode(colander.String(),
                                        title=u"Client",
                                        widget=deferred_autocomplete_widget)

class EstimationLineSchema(colander.Schema):
    """
        Estimation line edition form
    """
    description = colander.SchemaNode(colander.String(),
                                    title=u'Description',
                                    missing=u'')
    cost = colander.SchemaNode(colander.Integer(),
                                    title=u'Coût/unité')
    quantity = colander.SchemaNode(colander.Float(),
                                    title=u'Quantité',
                                    default=1.0)

class EstimationLineSequence(colander.SequenceSchema):
    estimationline = EstimationLineSchema()

#TODO : tva, needs mysql migration to be set at line level
# TODO : TVA values need crud configuration
TVAS = (('N.A', -1,),
        ("0%", 0,),
        ("5.5%", 550,),
        ("7%", 700,),
        ("19.6%",1960,),)
class EstimationSchema(colander.MappingSchema):
    """
        Estimation edition form
    """
    #TODO : change displayedUnits to boolean
#    displayedUnits = colander.SchemaNode(colander.Integer(4),
#                            default=0,
#                            title=u""
#                            widget=widget.CheckboxChoiceWidget(values = ((u"Afficher les unités dans le pdf ?", 1,)))
#                            )
    tva = colander.SchemaNode(
                       colander.Integer(),
                       title=u"TVA",
                       widget=widget.SelectWidget(values=TVAS))

    discountHT = colander.SchemaNode(
                    colander.Integer(),
                    title=u"Remise commerciale (du HT)")
    estimationlines = EstimationLineSequence()
