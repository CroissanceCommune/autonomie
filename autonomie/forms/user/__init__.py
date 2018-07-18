# -*- coding:utf-8 -*-

import colander
import deform
from sqlalchemy import or_
from sqlalchemy.orm import load_only

from autonomie_base.models.base import DBSESSION
from autonomie import forms
from autonomie.utils.strings import (
    format_account,
)

from autonomie.models.user.user import User
from autonomie.models.user.login import Login
from autonomie.models.user.group import Group


def _filter_by_group(query, groups):
    """
    Collect users belonging to a given group

    :param list groups: List of groups as strings
    :returns: User belonging to this group
    """
    if groups:
        if len(groups) > 1:
            clauses = []
            for group in groups:
                clauses.append(Login.groups.contains(group))

            return query.filter(or_(*clauses))
        else:
            return query.filter(Login.groups.contains(groups))
    return query


def get_users_options(roles=None):
    """
    Return the list of active users from the database formatted as choices:
        [(user_id, user_label)...]

    :param role: roles of the users we want
        default:  all
        values : ('contractor', 'manager', 'admin'))
    """
    query = DBSESSION().query(User).options(
        load_only('id', 'firstname', 'lastname')
    )

    # Only User accounts with logins
    query = query.join(Login).filter(Login.active == True)

    query = query.order_by(User.lastname)

    if roles and not hasattr(roles, "__iter__"):
        roles = [roles]

    query = _filter_by_group(query, roles)
    return [(unicode(u.id), format_account(u)) for u in query]


def get_deferred_user_choice(roles=None, widget_options=None):
    """
    Return a colander deferred for users selection options
    """
    widget_options = widget_options or {}
    default_option = widget_options.pop("default_option", None)

    @colander.deferred
    def user_select(node, kw):
        """
            Return a user select widget
        """
        choices = get_users_options(roles)
        if default_option:
            choices.insert(0, default_option)
        return deform.widget.Select2Widget(
            values=choices,
            **widget_options
            )
    return user_select


def user_node(roles=None, multiple=False, **kw):
    """
    Return a schema node for user selection
    roles: allow to restrict the selection to the given roles
        (to select between admin, contractor and manager)
    """
    widget_options = kw.pop('widget_options', {})
    return colander.SchemaNode(
        colander.Set() if multiple else colander.Integer(),
        widget=get_deferred_user_choice(roles, widget_options),
        **kw
    )


contractor_filter_node_factory = forms.mk_filter_node_factory(
    user_node,
    empty_filter_msg=u'Tous les travailleurs',
    title=u'Travailleur',
)

conseiller_choice_node = forms.mk_choice_node_factory(
    user_node,
    resource_name=u"un conseiller",
    roles=['manager', 'admin'],
)

conseiller_filter_node_factory = forms.mk_filter_node_factory(
    user_node,
    empty_filter_msg='Tous les conseillers',
    roles=['manager', 'admin'],
)

participant_choice_node = forms.mk_choice_node_factory(
    user_node,
    resource_name=u"un participant",
    resource_name_plural=u"un ou plusieurs participant(s)",
)

participant_filter_node_factory = forms.mk_filter_node_factory(
    user_node,
    empty_filter_msg='Tous les participants',
)

contractor_choice_node_factory = forms.mk_choice_node_factory(
    user_node,
    resource_name="un entrepreneur",
    roles=['contractor'],
)

trainer_choice_node_factory = forms.mk_choice_node_factory(
    user_node,
    resource_name="un(e) Animateur/Animatrice",
    resource_name_plural="un(e) ou plusieurs Animateur/Animatrice(s)",
    roles=['trainer'],
)

trainer_filter_node_factory = forms.mk_filter_node_factory(
    user_node,
    empty_filter_msg=u"Tou(te)s les Animateur/Animatrice(s)",
    roles=['trainer'],
)


@colander.deferred
def deferred_user_groups_datas_select(node, kw):
    values = Group.query('id', 'label').all()
    values.insert(0, ('', "- Sélectionner un rôle"))
    return deform.widget.SelectWidget(
        values=values
    )


@colander.deferred
def deferred_user_groups_datas_validator(node, kw):
    ids = [entry[0] for entry in Group.query('id')]
    return colander.OneOf(ids)
