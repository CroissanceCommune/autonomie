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
Csv import module related views

1- Download the csv
2- Generate an association form
3- Import datas
4- Return the resume
"""
from __future__ import absolute_import
import os
import logging
import json

from collections import OrderedDict
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPForbidden,
)
from deform import (
    Button,
)

from autonomie.csv_import import (
    get_csv_reader,
    get_csv_import_associator,
)
from autonomie.models.config import Config
from autonomie.models.job import CsvImportJob
from autonomie.models.base import DBSESSION
from autonomie.task import async_import_datas
from autonomie.forms.csv_import import (
    get_csv_file_upload_schema,
    get_association_schema,
)
from autonomie.resources import fileupload_js
from autonomie.views import BaseFormView


log = logging.getLogger(__name__)


# The key we use to store informations about the current imported csv file in
# the user's sessioSESSION_KEY = "csv_import"
SESSION_KEY = "csv_import"

IMPORT_INFO = u"Vous vous apprêtez à importer (ou mettre à jour) {count} \
entrée(s)."


class CsvFileUploadView(BaseFormView):
    """
    First step view for csv file importation

    HEre we get :
        1- a csv file
        2- a model type
        3- a delimiter
        4- a quotechar

    2,3 and 4 are carried to the next step view through the request's GET params
    """
    title = u"Import des dossiers, étape 1 : chargement d'un fichier csv"
    help_message = u"L'import de données, permet, depuis un fichier de type csv, \
d'insérer de nouvelle données dans Autonomie, ou de mettre à jour \
des données existantes. <br />\
Pour importer des données, vous devez disposer d'un \
fichier : <br /> \
            <ul> \
                <li>Enregistré au format csv;</li> \
                <li>Enregistré au format utf-8.</li> \
            </ul> \
Une fois le fichier chargé, vous aller être redirigé vers un formulaire pour \
associer les champs de votre fichier avec les données d'Autonomie."
    _schema = None
    add_template_vars = ('title', 'help_message')
    default_model_type = 'userdatas'
    model_types = ('userdatas',)

    def get_bind_data(self):
        return dict(
            request=self.request,
            model_types=self.model_types,
        )

    # Schema is here a property since we need to build it dynamically regarding
    # the current request (the same should have been built using the after_bind
    # method ?)
    @property
    def schema(self):
        """
        The getter for our schema property
        """
        if self._schema == None:
            self._schema = get_csv_file_upload_schema(self.request)
        return self._schema

    @schema.setter
    def schema(self, value):
        """
        A setter for the schema property
        The BaseClass in pyramid_deform gets and sets the schema attribute that
        is here transformed as a property
        """
        self._schema = value


    def before(self, form):
        """
        Ensure the fileupload js stuff is loaded
        """
        fileupload_js.need()
        form.set_appstruct({'model_type': self.default_model_type})

    def submit_success(self, appstruct):
        """
        Launched on successfull file upload
        """
        log.debug(u"A csv file has been uploaded")
        uid = appstruct['csv_file']['uid']
        association = appstruct.get('association')
        _query=dict(
            uid=uid,
            model_type=appstruct['model_type'],
            delimiter=appstruct['delimiter'],
            quotechar=appstruct['quotechar'],
        )
        if association:
            _query['association'] = association
        return HTTPFound(self.get_next_step_route(_query))

    def get_next_step_route(self, args):
        """
        Returns the path to the next step of the import process (should be
        overriden by subclassing views)
        """
        return self.request.route_path("import_step2", _query=args)


def get_current_csv_filepath(request):
    """
    Return the csv filepath currently stored in the user's session

    :returns: a filepath
    :raises KeyError: if no file datas are stored in the current session
    """
    tempdir = request.registry.settings['pyramid_deform.tempdir']
    file_uid = request.GET['uid']
    file_informations = request.session['substanced.tempstore'][file_uid]
    filename = file_informations['randid']
    filepath = os.path.join(tempdir, filename)
    return filepath


def get_current_csv(filepath, delimiter, quotechar):
    """
    Return the csv file currently stored in the user's session

    :returns: a csv dictreader object with the actual csv datas
    :raises KeyError: if no file datas are stored in the current session
    """
    # Related to pyramid_deform's way to store temporary datas on disk
    filebuffer = open(filepath, 'r')
    return get_csv_reader(filebuffer, delimiter, quotechar)

def count_entries(filepath):
    """
    Count how many csv entries are stored in the given file
    """
    return len(file(filepath, 'r').readlines()) - 1


def get_preferences_obj():
    """
    Return the config object used to store prefereces
    """
    return Config.get('csv_import') or Config(name='csv_import')


def load_preferences(obj):
    """
    Load preferences from the associated config object using json

    :param obj obj: The config object used to store preferences
    """
    val = obj.value
    if val is None:
        return {}
    else:
        return json.loads(val)


def get_preference(name):
    """
    Return a stored association dict

    :param str name: the name this association was stored under
    """
    config_obj = get_preferences_obj()
    preferences = load_preferences(config_obj)
    return preferences.get(name, {})


def record_preference(request, name, association_dict):
    """
    Record a field association in the request config
    """
    config_obj = get_preferences_obj()
    associations = load_preferences(config_obj)
    associations[name] = association_dict

    if config_obj.value is None:
        # It's a new one
        config_obj.value = json.dumps(associations)
        DBSESSION().add(config_obj)
    else:
        # We edit it
        config_obj.value = json.dumps(associations)
        DBSESSION().merge(config_obj)
    return associations


class ConfigFieldAssociationView(BaseFormView):
    """
    View for field association configuration
    Dynamically build a form regarding the previously stored csv datas

    :param request: the pyramid request object
    """
    help_message = u"Vous vous apprêtez à importer des données depuis le \
fichier fournit à l'étape précédente. <br /> \
À cette étape, vous allez : \
            <ul>\
        <li>Choisir la méthode d'import de données (nouvelle entrées, \
mise à jour de données)</li>\
        <li>Dans le cas de la mise à jour de données : Sélectionner le \
champ de votre fichier qui sera utilisé pour retrouver les données déjà \
présentes dans Autonomie</li> \
        <li>Associer les colonnes de votre fichier avec les attributs \
d'Autonomie correspondant</li>"
    add_template_vars = ("title", "info_message", "help_message", )
    title = u"Import de données, étape 2 : associer les champs"
    _schema = None
    buttons=(
        Button('submit', title=u"Lancer l'import",),
        Button('cancel', title=u"Annuler l'import",),
    )
    model_types = CsvFileUploadView.model_types

    def __init__(self, context, request):
        BaseFormView.__init__(self, request)
        self.model_type = self.request.GET['model_type']
        self.quotechar = self.request.GET['quotechar']
        self.delimiter = self.request.GET['delimiter']

        if self.model_type not in self.model_types:
            raise HTTPForbidden()

        # We first count the number of elements in the file
        self.filepath = get_current_csv_filepath(self.request)

        # We build a field - model attr associator
        self.associator = get_csv_import_associator(self.model_type)
        _csv_obj = get_current_csv(self.filepath, self.delimiter, self.quotechar)
        self.headers = [header for header in _csv_obj.fieldnames if header]

    # Schema is here a property since we need to build it dynamically regarding
    # the current request (the same should have been built using the after_bind
    # method ?)
    @property
    def schema(self):
        """
        The getter for our schema property
        """
        if self._schema == None:
            self._schema = get_association_schema(self.request)
        return self._schema

    @schema.setter
    def schema(self, value):
        """
        A setter for the schema property
        The BaseClass in pyramid_deform gets and sets the schema attribute that
        is here transformed as a property
        """
        self._schema = value

    def get_bind_data(self):
        """
        Returns the datas used whend binding the schema for field association
        """
        return dict(
            associator=self.associator,
            csv_headers=self.headers
        )

    def before(self, form):
        """
        Initialize the datas used in the view process and populate the form
        """
        if self.request.GET.has_key('association'):
            preference_name = self.request.GET['association']
            preference = get_preference(preference_name)
            association_dict = self.associator.guess_association_dict(
                self.headers,
                preference,
            )
        else:
            # We try to guess the association dict to initialize the form
            association_dict = self.associator.guess_association_dict(
                self.headers
            )


        log.info(u"We initialize the association form")
        log.info(association_dict)
        log.info(self.headers)
        # We initialize the form
        appstruct = {'entries': []}
        for csv_key, model_attribute in association_dict.items():
            appstruct['entries'].append(
                {
                    'csv_field': csv_key,
                    "model_attribute": model_attribute
                }
            )

        form.set_appstruct(appstruct)
        return form

    @property
    def info_message(self):
        num_lines = count_entries(self.filepath)
        return IMPORT_INFO.format(count=num_lines)

    def get_recording_job(self):
        """
        Initialize a job for importation recording
        """
        # We initialize a job record in the database
        job = CsvImportJob()
        job.set_owner(self.request.user.login)
        DBSESSION().add(job)
        DBSESSION().flush()
        return job

    def build_association_dict(self, importation_datas):
        """
        Build the association dict that describes matching between csv and model
        fields
        """
        # On génère le dictionnaire d'association qui va être utilisé pour
        # l'import
        association_dict = OrderedDict()
        for entry in importation_datas['entries']:
            if entry.has_key('model_attribute'):
                association_dict[entry['csv_field']] = \
                        entry['model_attribute']
        return association_dict

    def get_default_values(self):
        """
        Returns default values for object initialization
        Usefull for subclasses to force some attribute values (like company_id)
        """
        return {}

    def submit_success(self, importation_datas):
        """
        Submission has been called and datas have been validated

        :param dict importation_datas: The datas we want to import
        """
        log.info(u"Field association has been configured, we're going to \
import")
        action = importation_datas['action']
        csv_id_key = importation_datas['id_key']
        force_rel_creation = importation_datas.get(
            'force_rel_creation',
            False,
        )

        association_dict = self.build_association_dict(importation_datas)

        # On enregistre le dictionnaire d'association de champs
        if importation_datas.get('record_association', False):
            name = importation_datas['record_name']
            record_preference(self.request, name, association_dict)

        # On traduit la "valeur primaire" configurée par l'utilisateur en
        # attribut de modèle (si il y en a une de configurée)
        # Colonne du fichier csv -> attribut du modèle à importer
        id_key = association_dict.get(csv_id_key, csv_id_key)

        job = self.get_recording_job()

        celery_job = async_import_datas.delay(
            self.model_type,
            job.id,
            association_dict,
            self.filepath,
            id_key,
            action,
            force_rel_creation,
            self.get_default_values(),
            self.delimiter,
            self.quotechar,
        )

        log.info(u" * The Celery Task {0} has been delayed, its result \
should be retrieved from the CsvImportJob : {1}".format(celery_job.id, job.id)
                )
        return HTTPFound(
            self.request.route_path('job', id=job.id)
        )

    def get_previous_step_route(self):
        """
        Return the path to the previous step of our importation process
        Should be overriden by subclassing views
        """
        return self.request.route_path("import_step1")

    def cancel_success(self, appstruct):
        return HTTPFound(self.get_previous_step_route())

    cancel_failure = cancel_success


def includeme(config):
    """
    Configure views
    """
    config.add_route("import_step1", "/import/1/")
    config.add_route("import_step2", "/import/2/")
    config.add_view(
        CsvFileUploadView,
        route_name="import_step1",
        permission="admin",
        renderer="base/formpage.mako",
    )
    config.add_view(
        ConfigFieldAssociationView,
        route_name="import_step2",
        permission="admin",
        renderer="base/formpage.mako",
    )
