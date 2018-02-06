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
import functools

from colanderalchemy import SQLAlchemySchemaNode

from autonomie_base.consts import CIVILITE_OPTIONS

from autonomie.models.user.user import User
from autonomie.models.company import Company
from autonomie.models.expense.types import ExpenseKmType
from autonomie import forms

logger = log = logging.getLogger(__name__)


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


def set_widgets(schema):
    """
    Customize form widgets

    :param obj schema: The colander Schema to edit
    """
    customize = functools.partial(forms.customize_field, schema)
    if 'vehicle' in schema:
        customize(
            'vehicle',
            widget=forms.get_deferred_select(
                ExpenseKmType,
                keys=(
                    lambda a: u"%s-%s" % (a.label, a.code),
                    lambda a: u"%s (%s)" % (a.label, a.code)
                ),
                filters=[('active', True)]
            )
        )

    customize(
        'civilite',
        widget=forms.get_select(CIVILITE_OPTIONS),
        validator=forms.get_select_validator(CIVILITE_OPTIONS)
    )

    customize('email', validator=forms.mail_validator())

    return schema


def remove_admin_list_fields(schema, kw):
    """
    Remove admin specific filter fields

    :param obj schema: The colander Schema
    :param dict kw: The bind parameters
    """
    if not kw['request'].has_permission('admin_users'):
        del schema['active']


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

    schema.add(
        colander.SchemaNode(
            colander.String(),
            name='active',
            widget=deform.widget.SelectWidget(
                values=(
                    ('Y', u"Seulement les comptes actifs"),
                    ('N', u"Seulement les comptes désactivés"),
                    ('', u"Afficher tous les comptes"),
                )
            ),
            default='Y',
            missing=colander.drop,
            title=""
        )
    )
    schema.after_bind = remove_admin_list_fields
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


def get_add_edit_schema(edit=False):
    """
    Return a user add schema
    """
    schema = SQLAlchemySchemaNode(
        User,
        includes=(
            'civilite',
            'firstname',
            'lastname',
            'email',
        ),
    )
    if not edit:
        schema.add(
            colander.SchemaNode(
                colander.Boolean(),
                name='add_login',
                title=u"Créer des identifiants pour ce compte ?",
                description=u"Les identifiants permettront au titulaire de ce "
                u"compte de se connecter",
            )
        )
    set_widgets(schema)
    return schema


def get_edit_accounting_schema():
    """
    Return a schema for user accounting datas edition
    """
    schema = SQLAlchemySchemaNode(
        User,
        includes=(
            'vehicle',
            'compte_tiers',
        ),
    )
    set_widgets(schema)
    return schema
