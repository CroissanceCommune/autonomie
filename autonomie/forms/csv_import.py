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
"""
import colander
import json
import deform
import pyramid_deform

from autonomie.utils.form_widget import DisabledInput
from autonomie import csv_import
from autonomie import forms


IMPORTATION_TYPE_OPTIONS = (
    (u"insert", u"Insérer de nouvelles données",),
    (u"update", u"Compléter des données existantes (les données déjà saisies \
     seront conservées)"),
    (u"override", u"Mettre à jour les données existantes"),
)


@colander.deferred
def deferred_temporary_upload_widget(node, kw):
    """
    Return a file upload widget that stores the datas in the current session
    """
    request = kw['request']
    tmpstore = pyramid_deform.SessionFileUploadTempStore(request)
    return forms.files.CustomFileUploadWidget(
        tmpstore,
        template=forms.TEMPLATES_PATH + "fileupload.mako"
    )


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


#TODO : provide quotechar and delimiter customization
#TODO: provide a list of previsouly field association
class CsvFileUploadSchema(colander.Schema):
    """
    Csv import first step schema
    """
    association = colander.SchemaNode(
        colander.String(),
        widget=deferred_preferences,
        title=u"Type de fichiers",
        description=u"Permet de pré-charger automatiquement des associations \
de champs pour l'étape 2",
        missing=colander.drop
    )
    csv_file = colander.SchemaNode(
        deform.FileData(),
        widget=deferred_temporary_upload_widget,
        title=u"Fichier csv",
        description=u"Fichier csv contenant les données à importer (delimiter: \
';' quotechar: '\"'), le fichier doit être enregistré au format utf-8",
        validator=check_csv_content,
    )


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
        min_len=len(csv_headers),
        max_len=len(csv_headers),
    )


class AssociationEntry(colander.MappingSchema):
    """
    A form entry for csv field <-> model's attribute association
    """
    csv_field = colander.SchemaNode(
        colander.String(),
        title=u"Champ du fichier csv",
        widget=DisabledInput(),
    )
    model_attribute = colander.SchemaNode(
        colander.String(),
        title=u"Sera importé comme",
        widget=deferred_model_attribute_list_schema,
        missing=colander.drop,
    )


class AssociationEntries(colander.SequenceSchema):
    entry = AssociationEntry()


class AssociationSchema(colander.MappingSchema):
    entries = AssociationEntries(
        widget=deferred_seq_widget,
        title=u"Association des données"
    )
    id_key = colander.SchemaNode(
        colander.String(),
        title=u"Identifiant unique",
        description=u"Dans le cas de mise à jour de données, vous pouvez \
définir quel champ doit être utilisé pour retrouver des entrées existantes \
dans la base de données.",
        widget=deferred_id_key_widget,
        missing="id", # par défaut on identifie grâce à l'attribut id
    )
    action = colander.SchemaNode(
        colander.String(),
        title=u"Type d'importation",
        description=u"Définit la politique d'insertion d'informations dans la \
base de données.",
        widget=deform.widget.RadioChoiceWidget(values=IMPORTATION_TYPE_OPTIONS),
        default=u"insert",
        missing=u"insert",
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

def check_record_name(form, values):
    """
    If we record an association schema, we need the name
    """
    if values.get('record_association', False):
        if not values.get('record_name'):
            exc = colander.Invalid(form, u"Vous devez saisir un nom")
            exc["record_name"] = u"Ce paramètre est requis"
            raise exc

ASSOCIATIONSCHEMA = AssociationSchema(validator=check_record_name)
