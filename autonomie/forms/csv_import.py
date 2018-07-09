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
Forms elements related to csv import


1- Upload a csv file and choose the type of datas you want to import

2- Associate the datas with the model's columns



"""
import logging
import colander
import json
import deform

from deform_extensions import DisabledInput
from autonomie_celery.tasks import csv_import
from autonomie.forms.files import FileNode


IMPORTATION_TYPE_OPTIONS = (
    (
        u"only_update",
        u"Mise à jour seulement : Compléter des données existantes \
(aucune nouvelle entrée ne sera créée)",
    ),
    (
        u"only_override",
        u"Mise à jour seulement : Mettre à jour les données existantes \
(aucune nouvelle entrée ne sera créée)",
    ),
    (
        u"update",
        u"Mise à jour : Compléter des données existantes \
(si de nouvelles entrées sont rencontrées, elles seront créées dans la base)"
    ),
    (
        u"override",
        u"Mise à jour : Mettre à jour les données existantes \
(si de nouvelles entrées sont rencontrées, elles seront ajoutées dans la base)"
    ),
    (
        u"insert",
        u"Insérer de nouvelles données",
    ),
)


log = logging.getLogger(__name__)


def check_csv_content(node, value):
    """
    check the file datas are composed of csv datas
    """
    file_obj = value.get('fp')
    if file_obj:
        file_obj.seek(0)
        reader = csv_import.get_csv_reader(file_obj)
        first_line = reader.next()
        if not first_line or None in first_line.keys():
            message = u"Les données de ce fichier ne semblent pas être au \
format csv."
            raise colander.Invalid(node, message)


@colander.deferred
def deferred_preferences(node, kw):
    request = kw['request']
    associations = json.loads(request.config.get('csv_import', '{}'))

    options = zip(associations.keys(), associations.keys())
    options.insert(0, ('', u"- Sélectionner des préférences -"))
    return deform.widget.SelectWidget(values=options)


@colander.deferred
def deferred_model_type_widget(node, kw):
    model_types = kw['model_types']

    if len(model_types) == 1:
        result = deform.widget.HiddenWidget()
    else:
        request = kw['request']
        values = []
        for key in model_types:
            value = csv_import.MODELS_CONFIGURATION.get(key)
            if value is None:
                log.warn(u"The following importation model type doesn't \
exists : {0}".format(key))

            permission = value['permission']
            if request.has_permission(permission, request.context):
                values.append((key, value['label']))

        result = deform.widget.SelectWidget(values=values)

    return result


class CsvFileUploadSchema(colander.Schema):
    """
    Csv import first step schema
    """
    csv_file = FileNode(
        title=u"Fichier csv",
        description=u"Fichier csv contenant les données à importer (delimiter: \
';' quotechar: '\"'), le fichier doit être enregistré au format utf-8",
        validator=check_csv_content,
    )
    model_type = colander.SchemaNode(
        colander.String(),
        widget=deferred_model_type_widget,
        title=u"Type de données",
    )
    association = colander.SchemaNode(
        colander.String(),
        widget=deferred_preferences,
        title=u"Type de fichiers",
        description=u"Permet de pré-charger automatiquement des associations \
de champs pour l'étape 2",
        missing=colander.drop
    )
    delimiter = colander.SchemaNode(
        colander.String(),
        title=u"Caractère utilisé pour délimiter les champs du fichier",
        widget=deform.widget.SelectWidget(
            values=zip(csv_import.DELIMITERS, csv_import.DELIMITERS),
        ),
        default=csv_import.DEFAULT_DELIMITER,
        missing=csv_import.DEFAULT_DELIMITER,
    )
    quotechar = colander.SchemaNode(
        colander.String(),
        title=u"Caractère utilisé pour délimiter les chaînes de caractères",
        widget=deform.widget.SelectWidget(
            values=zip(csv_import.QUOTECHARS, csv_import.QUOTECHARS),
        ),
        default=csv_import.DEFAULT_QUOTECHAR,
        missing=csv_import.DEFAULT_QUOTECHAR,
    )

    def validator(self, node, value):
        """
        Validate the csv file upload ensuring the datas is in the format
        described by delimiter an quotechar
        """
        quotechar = value['quotechar']
        delimiter = value['delimiter']
        csv_file_obj = value['csv_file'].get('fp')
        csv_file_obj.seek(0)
        csv_data = csv_import.get_csv_reader(
            csv_file_obj,
            delimiter=delimiter,
            quotechar=quotechar,
        )
        try:
            first_line = csv_data.next()
            csv_file_obj.seek(0)
        except:
            raise colander.Invalid(node, u"Ce fichier semble vide")
        keys = first_line.keys()
        if not first_line or None in keys or len(keys) < 2:
            message = u"Les données de ce fichier ne semblent pas être au \
bon format."
            raise colander.Invalid(node, message)


def get_csv_file_upload_schema(request):
    """
    Return an import csv file upload schema regarding the current user's rights
    """
    schema = CsvFileUploadSchema().clone()
    if not request.has_permission('admin', request.context):
        del schema['association']
    return schema


@colander.deferred
def deferred_model_attribute_list_schema(node, kw):
    """
    Return the widget for field attributes selection
    """
    associator_object = kw['associator']
    values = [('', 'Ne pas importer')]
    for column in associator_object.get_columns().values():
        values.append((column['name'], column['label']))
    return deform.widget.SelectWidget(values=values)


@colander.deferred
def deferred_id_key_widget(node, kw):
    """
    Return the radio choice widget used to define which field should be used as
    id key
    """
    csv_headers = kw['csv_headers']
    return deform.widget.RadioChoiceWidget(
        values=zip(csv_headers, csv_headers),
    )


@colander.deferred
def deferred_seq_widget(node, kw):
    """
    Dynamically return a sequence widget with fixed length
    """
    csv_headers = kw['csv_headers']
    return deform.widget.SequenceWidget(
        min_len=len(set(csv_headers)),
        max_len=len(set(csv_headers)),
    )


class AssociationEntry(colander.MappingSchema):
    """
    A form entry for csv field <-> model's attribute association
    """
    csv_field = colander.SchemaNode(
        colander.String(),
        title=u"Libellé dans le fichier",
        widget=DisabledInput(),
    )
    model_attribute = colander.SchemaNode(
        colander.String(),
        title=u"Sera importé comme",
        widget=deferred_model_attribute_list_schema,
        missing=colander.drop,
    )


class AssociationEntries(colander.SequenceSchema):
    entry = AssociationEntry(title=u"Champ du fichier csv")


class AssociationSchema(colander.MappingSchema):
    action = colander.SchemaNode(
        colander.String(),
        title=u"Type d'importation",
        description=u"Définit la politique d'insertion d'informations dans la \
base de données.",
        widget=deform.widget.RadioChoiceWidget(values=IMPORTATION_TYPE_OPTIONS),
        default=u"only_update",
        missing=u"only_update",
    )
    id_key = colander.SchemaNode(
        colander.String(),
        title=u"Identifiant unique",
        description=u"Dans le cas de mise à jour de données, vous pouvez \
définir quel champ doit être utilisé pour retrouver des entrées existantes \
dans la base de données.",
        widget=deferred_id_key_widget,
        missing="id",  # par défaut on identifie grâce à l'attribut id
    )
    entries = AssociationEntries(
        widget=deferred_seq_widget,
        title=u"Association des données"
    )
    record_association = colander.SchemaNode(
        colander.Boolean(),
        title=u"Enregistrer ?",
        description=u"Voulez-vous conserver cette association de champ pour de \
futures importations ?",
    )
    record_name = colander.SchemaNode(
        colander.String(),
        title=u"Nom de l'enregistrement",
        description=u"Ce nom vous permettra de recharger cette association",
        missing=colander.drop,
    )
    force_rel_creation = colander.SchemaNode(
        colander.Boolean(),
        title=u"Forcer la création d'élément de configuration",
        description=u"Si des entrées correspondent à des champs à valeur \
multiple dont les options sont configurables depuis l'interface \
d'administration, et qu'aucun option ne correspond, une nouvelle option \
sera créée automatiquement.",
        default=False,
    )


def check_record_name(form, values):
    """
    If we record an association schema, we need the name
    """
    if values.get('record_association', False):
        if not values.get('record_name'):
            exc = colander.Invalid(form, u"Vous devez saisir un nom")
            exc["record_name"] = u"Ce paramètre est requis"
            raise exc


def get_association_schema(request):
    """
    Returns a form schema used to configure field association for csv import
    """
    schema = AssociationSchema(validator=check_record_name).clone()

    if not request.has_permission('admin', request.context):
        del schema['force_rel_creation']
        del schema['record_association']
        del schema['record_name']
    return schema
