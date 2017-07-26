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
import deform

from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models import user
from autonomie.models.company import Company
from autonomie import forms

logger = log = logging.getLogger(__name__)


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
        if not user.User.unique_login(value, user_id):
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
    result = user.User.query().filter_by(login=login).first()
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
    wid = deform.widget.AutocompleteInputWidget(
        values=companies,
#        template="autonomie:deform_templates/autocomple_input.pt"
    )
    return wid


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
        widget=deform.widget.PasswordWidget(),
        title="Mot de passe",
    )


class AuthSchema(BaseAuthSchema):
    """
        Schema for authentication form
    """
    nextpage = colander.SchemaNode(
        colander.String(),
        widget=deform.widget.HiddenWidget(),
        missing=colander.drop,
    )
    remember_me = colander.SchemaNode(
        colander.Boolean(),
        widget=deform.widget.CheckboxWidget(),
        label=u"Rester connecté",
        title="",
        missing=False,
    )


def get_auth_schema():
    """
        return the authentication form schema
    """
    return AuthSchema(title=u"", validator=auth)


def get_json_auth_schema():
    """
        return the auth form schema in case of json auth
    """
    return BaseAuthSchema(validator=auth)


def get_list_schema():
    """
    Return a schema for filtering the user list
    """
    schema = forms.lists.BaseListsSchema().clone()

    schema['search'].description = u"Nom, entreprise, activité"

    schema.add(
        colander.SchemaNode(
            colander.Integer(),
            name='activity_id',
            missing=colander.drop,
            widget=forms.company.deferred_company_datas_select,
            validator=forms.company.deferred_company_datas_validator,
        )
    )

    schema.add(colander.SchemaNode(
        colander.String(),
        name='disabled',
        missing="0",
        default="0",
        widget=deform.widget.HiddenWidget(),
        validator=colander.OneOf(('0', '1'))
        )
    )
    return schema


@colander.deferred
def deferred_situation_select(node, kw):
    values = [('', u"Sélectionner un statut")]
    options = user.CaeSituationOption.query()
    for option in options:
        values.append((option.id, option.label))
    return deform.widget.SelectWidget(values=values)


@colander.deferred
def deferred_situation_id_validator(node, kw):
    return colander.OneOf(
        [option.id for option in user.CaeSituationOption.query()]
    )


def get_userdatas_list_schema():
    """
    Return a list schema for user datas
    """
    schema = forms.lists.BaseListsSchema().clone()

    schema['search'].description = u"Nom, prénom, entreprise"

    schema.insert(0, colander.SchemaNode(
        colander.Integer(),
        name='situation_situation',
        widget=deferred_situation_select,
        validator=deferred_situation_id_validator,
        missing=colander.drop,
    )
    )

    schema.insert(
        0,
        user.user_node(
            roles=['manager', 'admin'],
            missing=-1,
            default=forms.deferred_current_user_id,
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
        user.User,
        includes=('firstname', 'lastname', 'email',),
    )


def get_password_schema():
    """
    Return the schema for user password change
    """
    schema = SQLAlchemySchemaNode(
        user.User,
        includes=('login', 'pwd',),
        title=u'Modification de mot de passe',
        validator=auth,
    )

    schema.insert(
        1,
        colander.SchemaNode(
            colander.String(),
            widget=deform.widget.PasswordWidget(),
            name='password',
            title=u'Mot de passe actuel',
            default=u'',
        )
    )

    schema['login'].widget = deform.widget.HiddenWidget()
    # Remove login validation
    schema['login'].validator = None

    return schema


def get_groups(request):
    """
    Return the available groups as a list of 2-uples (id, label)
    """
    groups = user.Group.query().all()
    return [
        (group.name, group.label) for group in groups
        if request.has_permission(group.name)
    ]

@colander.deferred
def deferred_group_validator(node, kw):
    """
    Return a validator that checks that the validated datas matches the existing
    groups
    """
    request = kw['request']
    groups = get_groups(request)
    validator = colander.ContainsOnly([group[0] for group in groups])
    return colander.All(colander.Length(min=1), validator)


@colander.deferred
def deferred_group_widget(node, kw):
    """
    Return a widget for group selection
    """
    request = kw['request']
    groups = get_groups(request)
    return deform.widget.CheckboxChoiceWidget(values=groups)


def get_user_schema(edit=False, permanent=True):
    """
    Return the schema for adding/editing users

        edit

            Is this an edit form

        permanent

            Is this form related to permanent edition (managers or admins)
    """
    schema = SQLAlchemySchemaNode(user.User)

    schema.insert(
        0,
        colander.SchemaNode(
            colander.Set(),
            name="groups",
            validator=deferred_group_validator,
            widget=deferred_group_widget,
            title=u"Groupes de l'utilisateur",
        )
    )
    if permanent:
        schema.add(
            CompanySchema(
                name='companies',
                title=u"Entreprise(s)",
                widget=deform.widget.SequenceWidget(
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


def get_company_association_schema():
    """
    Return the schema used to associate a user to an existing company
    """
    schema = colander.Schema()
    schema.add(
        CompanySchema(
            name='companies',
            title=u"Entreprise(s)",
            widget=deform.widget.SequenceWidget(
                add_subitem_text_template=u"Ajouter une entreprise",
                min_len=1,
            ),
            description=u"Taper les premières lettres du nom \
d'une entreprise existante"
        )
    )
    return schema


def get_userdatas_schema():
    """
    Return the userdatas edition/add schema
    """
    schema = SQLAlchemySchemaNode(user.UserDatas, excludes=('name', '_acl'))
    return schema
