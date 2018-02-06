# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Login related form schemas

1- Password change
2- Add/Edit Form
3- Group configuration
"""
import logging
import colander
import deform
from sqlalchemy.orm import load_only

from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.user.group import Group
from autonomie.models.user.login import Login


logger = logging.getLogger(__name__)


def _get_unique_login_validator(login_id=None):
    """
    Return a unique login validator

        login_id

            The id of the current user in case we edit an account (the unicity
            should be checked on all the other accounts)
    """
    def unique_login(node, value):
        """
        Test login unicity against database
        """
        if not Login.unique_login(value, login_id):
            message = u"Le login '{0}' n'est pas disponible.".format(
                                                            value)
            raise colander.Invalid(node, message)
    return unique_login


@colander.deferred
def _deferred_login_validator(node, kw):
    """
        Dynamically choose the validator user for validating the login
    """
    login_id = kw['request'].context.id
    return _get_unique_login_validator(login_id)


def get_auth_validator(current_login_object=None):
    """
    Build an authentication validator

    :param obj current_login_object: If a login instance is provided use it for
    authentication
    """
    def auth_validator(form, value):
        """
        Authentication validator

        :param obj form: The form object
        :param dict value: The submitted datas to validate
        :raises: colander.Invalid on invalid authentication
        """
        logger.debug(u" * Authenticating")
        if current_login_object is None:
            login = value.get('login')
            login_object = Login.find_by_login(login)
            logger.debug(u"   +  Login {0}".format(login))
        else:
            login_object = current_login_object
            logger.debug(u"   +  Login {0}".format(login_object.login))

        password = value.get('password')
        if not login_object or not login_object.auth(password):
            logger.error(u"    - Authentication : Error")
            message = u"Erreur d'authentification"
            exc = colander.Invalid(form, message)
            exc['password'] = message
            raise exc
        else:
            logger.debug(u"   + Authentication : OK")
    return auth_validator


@colander.deferred
def deferred_password_validator(node, kw):
    current_login = kw['request'].context
    return get_auth_validator(current_login)


def get_groups(request):
    """
    Collect groups

    :returns: available groups as a list of 2-uples (name, label)
    """
    groups = Group.query().options(load_only(Group.id, Group.label)).all()
    return [
        (group.name, group.label) for group in groups
        if request.has_permission(group.name)
    ]


@colander.deferred
def _deferred_group_validator(node, kw):
    """
    Build a validator for group name validation

    :param obj node: The form schema node
    :param dict kw: The form schema bind params

    :returns: A colander validator
    """
    request = kw['request']
    groups = get_groups(request)
    validator = colander.ContainsOnly([group[0] for group in groups])
    return colander.All(colander.Length(min=1), validator)


@colander.deferred
def _deferred_group_widget(node, kw):
    """
    Build a select widget for groups

    :param obj node: The form schema node
    :param dict kw: The form schema bind params

    :returns: A deform widget
    """
    request = kw['request']
    groups = get_groups(request)
    return deform.widget.Select2Widget(
        values=groups,
        multiple=True,
    )


def _get_unique_user_id_validator(user_id=None):
    """
    Build a unique user_id validator to ensure a user is linked to only one user
    :param int user_id: optionnal user_id (in case of edit)
    """
    def unique_user_id(node, value):
        if not Login.unique_user_id(value, user_id):
            message = u"Ce compte possède déjà des identifiants.".format(
                                                            value
            )
            raise colander.Invalid(node, message)
    return unique_user_id


@colander.deferred
def _deferred_user_id_validator(node, kw):
    """
        Dynamically choose the validator user for validating the login
    """
    context = kw['request'].context
    if isinstance(context, Login):
        user_id = kw['request'].context.user_id
    else:
        user_id = kw['request'].context.id
    return _get_unique_user_id_validator(user_id)


def set_widgets(schema):
    """
    Set common widgets on the schema object

    :param obj schema: a colander schema
    """
    if 'pwd_hash' in schema:
        schema['pwd_hash'].widget = deform.widget.CheckedPasswordWidget()

    if 'user_id' in schema:
        schema['user_id'].widget = deform.widget.HiddenWidget()
    return schema


def get_password_schema():
    """
    Return the schema for user password change

    :returns: a colander Schema
    """
    schema = SQLAlchemySchemaNode(
        Login,
        includes=('pwd_hash',),
        title=u'',
        validator=deferred_password_validator,
    )
    set_widgets(schema)

    schema.insert(
        0,
        colander.SchemaNode(
            colander.String(),
            widget=deform.widget.PasswordWidget(),
            name='password',
            title=u'Mot de passe actuel',
            default=u'',
        )
    )

    schema['pwd_hash'].title = u"Nouveau mot de passe"

    return schema


def get_add_edit_schema(edit=False):
    """
    Add a form schema for login add/edit

    :returns: A colander form schema
    """
    schema = SQLAlchemySchemaNode(Login)
    set_widgets(schema)

    schema.add(
        colander.SchemaNode(
            colander.Set(),
            name="groups",
            validator=_deferred_group_validator,
            widget=_deferred_group_widget,
            title=u"Groupes de l'utilisateur",
        )
    )

    if edit:
        schema['login'].validator = _deferred_login_validator
        schema['pwd_hash'].missing = colander.drop
        schema['user_id'].validator = _deferred_user_id_validator
    else:
        schema['user_id'].validator = _get_unique_user_id_validator()
        schema['login'].validator = _get_unique_login_validator()
    return schema


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
    return AuthSchema(title=u"", validator=get_auth_validator())


def get_json_auth_schema():
    """
        return the auth form schema in case of json auth
    """
    return BaseAuthSchema(validator=get_auth_validator())
