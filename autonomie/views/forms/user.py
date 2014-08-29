# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
#

"""
    User account handling form schemas
"""
import colander
import logging

from deform import widget as deform_widget
from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.user import (
    User,
    SITUATION_OPTIONS,
)
from autonomie.models.company import Company
from autonomie.views.forms import main
from autonomie.views.forms.lists import BaseListsSchema

log = logging.getLogger(__name__)


MANAGER_ROLES = (
    (2, u'Membre de la coopérative'),
)


ADMIN_ROLES = (
    (1, u'Administrateur'),
    (2, u'Membre de la coopérative'),
)


def get_unique_login_validator(user_id=None):
    """
    Return a unique login validator

        user_id

            The id of the current user in case we edit an account (the unicity
            should be checked on all the other accounts)
    """
    def unique_login(node, value):
        """
        Test login unicity against database
        """
        if not User.unique_login(value, user_id):
            message = u"Le login '{0}' n'est pas disponible.".format(
                                                            value)
            raise colander.Invalid(node, message)
    return unique_login


def auth(form, value):
    """
        Check the login/password content
    """
    log.debug(u" * Authenticating")
    login = value.get('login')
    log.debug(u"   +  Login {0}".format(login))
    password = value.get('password')
    result = User.query().filter_by(login=login).first()
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
    user_id = kw['request'].context.id

    return get_unique_login_validator(user_id)


def get_companies_choices():
    """
        Return companies choices for autocomplete
    """
    return [comp.name for comp in Company.query([Company.name]).all()]


@colander.deferred
def deferred_company_input(node, kw):
    """
        Deferred company autocomplete input widget
    """
    companies = get_companies_choices()
    wid = deform_widget.AutocompleteInputWidget(values=companies,
            template="autonomie:deform_templates/autocomple_input.pt")
    return wid


@colander.deferred
def deferred_primary_group_widget(node, kw):
    """
        Return the primary group widget regarding the current user
    """
    user = kw['request'].user
    if user.is_admin():
        roles = ADMIN_ROLES
    elif user.is_manager():
        roles = MANAGER_ROLES
    else:
        roles = []
    return deform_widget.RadioChoiceWidget(values=roles)


@colander.deferred
def deferred_primary_group_validator(node, kw):
    """
        return the validator for primary group configuration
        regarding the current user
    """
    user = kw['request'].user
    if user.is_admin():
        roles = ADMIN_ROLES
    elif user.is_manager():
        roles = MANAGER_ROLES
    else:
        roles = []
    return colander.OneOf([x[0] for x in roles])


@colander.deferred
def deferred_company_disable_description(node, kw):
    """
        Return the description for the company disabling checkbox
    """
    description = u"Entraîne automatiquement la désactivation des employés."
    for company in kw['request'].context.companies:
        if len(company.employees) > 1:
            description += u"Attention : Au moins l'une de ses entreprises a \
plusieurs employés"
            break
    return description


@colander.deferred
def deferred_company_disable_default(node, kw):
    """
        return False is one of the user's companies have some employees
    """
    for company in kw['request'].context.companies:
        if len(company.employees) > 1:
            return False
    return True


class CompanySchema(colander.SequenceSchema):
    company = colander.SchemaNode(
        colander.String(),
        title=u"Nom de l'entreprise",
        widget=deferred_company_input)


SITUATION_SEARCH_OPTIONS = (
    ('', u"Sélectionner un statut",),
) + SITUATION_OPTIONS


class UserDisableSchema(colander.MappingSchema):
    disable = colander.SchemaNode(
        colander.Boolean(),
        default=True,
        title=u"Désactiver cet utilisateur",
        description=u"""Désactiver un utilisateur l'empêche de se
connecter mais permet de conserver l'intégralité
des informations concernant son activité.""")
    companies = colander.SchemaNode(
        colander.Boolean(),
        title=u"Désactiver ses entreprises",
        description=deferred_company_disable_description,
        default=deferred_company_disable_default)


class BaseAuthSchema(colander.MappingSchema):
    """
        Base auth schema (sufficient for json auth)
    """
    login = colander.SchemaNode(
        colander.String(),
        title="Identifiant",
    )
    password = colander.SchemaNode(
        colander.String(),
        widget=deform_widget.PasswordWidget(),
        title="Mot de passe",
    )


class AuthSchema(BaseAuthSchema):
    """
        Schema for authentication form
    """
    nextpage = colander.SchemaNode(
        colander.String(),
        widget=deform_widget.HiddenWidget())
    remember_me = colander.SchemaNode(
        colander.Boolean(),
        widget=deform_widget.CheckboxWidget(),
        title="Rester connecté",
    )


def get_auth_schema():
    """
        return the authentication form schema
    """
    return AuthSchema(title=u"Authentification", validator=auth)


def get_json_auth_schema():
    """
        return the auth form schema in case of json auth
    """
    return BaseAuthSchema(validator=auth)


def get_list_schema():
    """
    Return a schema for filtering the user list
    """
    schema = BaseListsSchema().clone()

    schema['search'].description = u"Nom, entreprise, activité"

    schema.add(colander.SchemaNode(
        colander.String(),
        name='disabled',
        missing="0",
        widget=deform_widget.HiddenWidget(),
        validator=colander.OneOf(('0', '1'))
        )
    )
    return schema


def get_userdatas_list_schema():
    """
    Return a list schema for user datas
    """
    schema = BaseListsSchema().clone()

    schema['search'].description = u"Nom, prénom, entreprise"

    schema.insert(0, colander.SchemaNode(
        colander.String(),
        name='situation_situation',
        widget=deform_widget.SelectWidget(values=SITUATION_SEARCH_OPTIONS),
        validator=colander.OneOf([s[0] for s in SITUATION_SEARCH_OPTIONS]),
        default='',
        missing='',
        )
    )

    schema.insert(
        0,
        main.user_node(
            roles=['manager', 'admin'],
            missing=-1,
            default=main.deferred_current_user_id,
            name='situation_follower_id',
            widget_options={
                'default_option': (-1, ''),
                'placeholder': u"Sélectionner un conseiller"},
        )
    )
    return schema


def get_account_schema():
    """
    Return the user account edition schema
    """
    return SQLAlchemySchemaNode(
        User,
        includes=('firstname', 'lastname', 'email',),
    )


def get_password_schema():
    """
    Return the schema for user password change
    """
    schema = SQLAlchemySchemaNode(
        User,
        includes=('login', 'pwd',),
        title=u'Modification de mot de passe',
        validator=auth,
    )

    schema.insert(
        1,
        colander.SchemaNode(
            colander.String(),
            widget=deform_widget.PasswordWidget(),
            name='password',
            title=u'Mot de passe actuel',
            default=u'',
        )
    )

    schema['login'].widget = deform_widget.HiddenWidget()
    # Remove login validation
    schema['login'].validator = None

    return schema


def get_user_schema(edit=False, permanent=True):
    """
    Return the schema for adding/editing users

        edit

            Is this an edit form

        permanent

            Is this form related to permanent edition (managers or admins)
    """
    if permanent:
        schema = SQLAlchemySchemaNode(User, excludes=('compte_tiers',))
    else:
        schema = SQLAlchemySchemaNode(User)

    if permanent:
        schema.insert(
            0,
            colander.SchemaNode(
                colander.Integer(),
                name='primary_group',
                validator=deferred_primary_group_validator,
                widget=deferred_primary_group_widget,
                title=u"Rôle de l'utilisateur",
            )
        )

    schema.add(
        CompanySchema(
            name='companies',
            title=u"Entreprise(s)",
            widget=deform_widget.SequenceWidget(
                add_subitem_text_template=u"Ajouter une entreprise"
            )
        )
    )

    if edit:
        schema['login'].validator = deferred_login_validator
        schema['pwd'].missing = colander.drop
    else:
        schema['login'].validator = get_unique_login_validator()

    return schema
