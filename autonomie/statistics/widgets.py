# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2014 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
"""
Statistics form widgets

Quatre type de données sont traitées pour l'instant

Date
Chaîne de caractères
Nombre (flottant ou entier)
Relation "options"
"""
import colander
from deform import widget as deform_widget

from autonomie.forms import (
    get_deferred_select,
    get_deferred_select_validator,
    get_select,
    get_select_validator,
)


STRING_OPTIONS = (
    ('', '- Tous -', ),
    ("has", u"Contient", ),
    ("sw", u"Commence par", ),
    ("ew", u"Se termine par", ),
    ("nhas", u"Ne contient pas", ),
    ("neq", u"N'est pas égal(e) à", ),
    ("eq", u"Est égal(e) à", ),
    ("nll", u"N'est pas renseigné(e)", ),
    ("nnll", u"Est renseigné(e)", ),
)


OPT_REL_OPTIONS = (
    ('', '- Tous -', ),
    ("ioo", u"Fait partie de", ),
    ("nioo", u"Ne fait pas partie de", ),
    ("nll", u"N'est pas renseigné(e)", ),
    ("nnll", u"Est renseigné(e)", ),
)


NUMERIC_OPTIONS = (
    ('', '- Tous -', ),
    ("lt", u"Est inférieur(e) à", ),
    ("gt", u"Est supérieur(e) à", ),
    ("lte", u"Est inférieur(e) ou égal(e)", ),
    ("gte", u"Est supérieur(e) ou égal(e)", ),
    ("bw", u"Fait partie de l'intervalle (limite inclue)", ),
    ("nbw", u"Ne fait pas partie de l'intervalle"),
    ("eq", u"Est égal(e) à",),
    ("neq", u"N'est pas égal(e) à", ),
    ("nll", u"N'est pas renseigné(e)", ),
    ("nnll", u"Est renseigné(e)", ),
)


DATE_OPTIONS = (
    ('', '- Tous -', ),
    ('dr', u"Dans l'intervalle", ),
    ('this_year', u"Depuis le début de l'année", ),
    ('this_month', u"Ce mois-ci", ),
    ("previous_year", u"L'année dernière", ),
    ("previous_month", u"Le mois dernier", ),
    ("nll", u"N'est pas renseigné(e)", ),
    ("nnll", u"Est renseigné(e)", ),
)



def get_options_field(options):
    """
    Return an option selection field
    """
    return colander.SchemaNode(
        colander.String(),
        name='options',
        widget=deform_widget.SelectWidget(values=options),
        validator=colander.OneOf([val[0] for val in options]),
        title=u"",
        missing=colander.null,
    )

class StringStatMapping(colander.MappingSchema):
    """
    The mapping schema corresponding the configuration of a statictic concerning
    string fields

    Example:

        in your model you have a field :
            mycolumn = Column(String(255))

        in the statistic configuration form, you'll have a column with a select
        list of how to search and an input for an optionnal value to use in the
        filter
    """
    options = get_options_field(STRING_OPTIONS)
    search = colander.SchemaNode(
        colander.String(),
        missing="",
    )


class NumericStatMapping(colander.MappingSchema):
    """
    The mapping schema corresponding to the configuration of a statistic
    concerning numeric fields (Integer, Float)
    """
    options = get_options_field(NUMERIC_OPTIONS)
    lower = colander.SchemaNode(
        colander.Float(),
        title=u"Entre",
        description=u"Début ou valeur à rechercher",
        missing=colander.null,
    )
    higher = colander.SchemaNode(
        colander.Float(),
        title=u"et",
        missing=colander.null,
    )


class DateStatMapping(colander.MappingSchema):
    """
    The mapping schema corresponding to date statistics definition
    """
    options = get_options_field(DATE_OPTIONS)
    start = colander.SchemaNode(
        colander.Date(),
        title=u"De",
        description=u"Début ou date à rechercher",
        missing=colander.null,
    )
    end = colander.SchemaNode(
        colander.Date(),
        title=u"à",
        description=u"Fin",
        missing=colander.null,
    )


class RelationStatMapping(colander.MappingSchema):
    """
    The mapping schema corresponding to the configuration of a statistic
    concerning relationship to "options" (See models/user.py for the BaseOption
    model)
    """
    options = get_options_field(OPT_REL_OPTIONS)


def get_relation_stat_mapping(sqla_model):
    """
    Returns a mapping for relations pointing to the given sqla_model

        sqla_model

            An option type model our main model is pointing to should have at
            least two attributes : id and label
    """
    schema = RelationStatMapping().clone()

    deferred_widget = get_deferred_select(sqla_model, multi=True)
    deferred_validator = get_deferred_select_validator(sqla_model)

    schema.add(
        colander.SchemaNode(
            colander.String(),
            name='search',
            widget=deferred_widget,
            validator=deferred_validator,
            title=u"",
            missing=u""
        )
    )
    return schema


def get_fixed_options_stat_mapping(options):
    """
    Return a mapping used to configure statictic for a column pointing to a fix
    set of options

        options

            options as the SelectWidget expects ((key, label), )
    """
    schema = RelationStatMapping().clone()

    schema.add(
        colander.SchemaNode(
            colander.String(),
            name='search',
            widget=get_select(options, multi=True),
            validator=get_select_validator(options),
            title=u"",
            missing=u""
        )
    )
    return schema
