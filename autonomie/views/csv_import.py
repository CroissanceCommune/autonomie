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
from pyramid.httpexceptions import HTTPFound
from deform import (
    Form,
    ValidationFailure,
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
    CsvFileUploadSchema,
    ASSOCIATIONSCHEMA,
)
from autonomie.resources import fileupload_js
from autonomie.views import BaseFormView


log = logging.getLogger(__name__)


# The key we use to store informations about the current imported csv file in
# the user's sessioSESSION_KEY = "csv_import"
SESSION_KEY = "csv_import"

IMPORT_INFO = u"Vous vous apprêtez à importer (ou mettre à jour) {count} \
entrées. <br /> Vous allez désormais configurer le lien entre les colonnes de \
votre fichier csv et les entrées de gestion sociale auxquelles elles \
correspondent."


#TODO : ask the type of model we want to import in step 1
class CsvFileUploadView(BaseFormView):
    """
    First step view for csv file importation
    """
    title = u"Import des dossiers, étape 1 : chargement d'un fichier csv"
    help_message = u"Pour importer des données, vous devez disposer d'un \
fichier de type csv : <br /> \
            <ul class='list-unstyled'> \
<li>Utilisant le caractère ';' comme séparateur </li>\
<li>Utilisant le caractère ' \" ' comme délimiteur de chaîne de caractères </li>\
<li>Enregistré au format utf-8.</li></ul> \
Une fois le fichier chargé, vous aller être redirigé vers un formulaire pour \
associer les champs de votre fichier avec des entrées de gestion sociale."
    schema = CsvFileUploadSchema()
    add_template_vars = ('title', 'help_message')


    def before(self, form):
        """
        Ensure the fileupload js stuff is loaded
        """
        fileupload_js.need()

    def submit_success(self, appstruct):
        """
        Launched on successfull file upload
        """
        log.debug(u"A csv file has been uploaded")
        uid = appstruct['csv_file']['uid']
        association = appstruct.get('association')
        _query=dict(uid=uid, model_type=appstruct['model_type'])
        if association:
            _query['association'] = association
        return HTTPFound(
            self.request.route_path(
                'import_step2',
                _query=_query,
            )
        )


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


def get_current_csv(filepath):
    """
    Return the csv file currently stored in the user's session

    :returns: a csv dictreader object with the actual csv datas
    :raises KeyError: if no file datas are stored in the current session
    """
    # Related to pyramid_deform's way to store temporary datas on disk
    filebuffer = open(filepath, 'r')
    return get_csv_reader(filebuffer)

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


def config_field_association(request):
    """
    View for field association configuration
    Dynamically build a form regarding the previously stored csv datas

    :param request: the pyramid request object
    """
    model_type = request.GET['model_type']

    # We first count the number of elements in the file
    filepath = get_current_csv_filepath(request)
    num_lines = count_entries(filepath)
    info_message = IMPORT_INFO.format(count=num_lines)

    # We build a field - model attr associator
    associator = get_csv_import_associator(model_type)
    csv_obj = get_current_csv(filepath)
    headers = [header for header in csv_obj.fieldnames if header]

    schema = ASSOCIATIONSCHEMA.bind(
        associator=associator,
        csv_headers=headers
    )
    form = Form(
        schema=schema,
        buttons=(
            Button('submit', title=u"Lancer l'import",),
            Button('cancel', title=u"Annuler l'import",),
        )
    )

    # Form submission
    if 'submit' in request.POST:
        controls = request.POST.items()

        try:
            importation_datas = form.validate(controls)
        except ValidationFailure, form:
            log.exception(u"Error on field association")

        else:
            log.info(u"Field association has been configured, we're going to \
import")
            action = importation_datas['action']
            csv_id_key = importation_datas['id_key']
            force_rel_creation = importation_datas.get(
                'force_rel_creation',
                False,
            )

            from collections import OrderedDict
            association_dict = OrderedDict()
            for entry in importation_datas['entries']:
                if entry.has_key('model_attribute'):
                    association_dict[entry['csv_field']] = \
                            entry['model_attribute']

            if importation_datas.get('record_association', False):
                name = importation_datas['record_name']
                record_preference(request, name, association_dict)

            # On traduit la "valeur primaire" configuré par l'utilisateur en
            # attribut de modèle (si il y en a une de configuré)
            id_key = association_dict.get(csv_id_key, csv_id_key)

            csv_filepath = get_current_csv_filepath(request)

            # We initialize a job record in the database
            job = CsvImportJob()
            DBSESSION().add(job)
            DBSESSION().flush()

            celery_job = async_import_datas.delay(
                model_type,
                job.id,
                association_dict,
                csv_filepath,
                id_key,
                action,
                force_rel_creation,
            )

            log.info(u" * The Celery Task {0} has been delayed, its result \
should be retrieved from the CsvImportJob : {1}".format(celery_job.id, job.id)
                    )
            return HTTPFound(request.route_path('job', id=job.id))
    # The form has been canceled going back to step 1
    elif 'cancel' in request.POST:
        log.info(u"Import has been cancelled")
        return HTTPFound(request.route_path('import_step1'))

    else:
        log.info(u"We initialize the association form")
        if request.GET.has_key('association'):
            preference_name = request.GET['association']
            preference = get_preference(preference_name)
            association_dict = associator.guess_association_dict(
                headers,
                preference,
            )
        else:
            # We try to guess the association dict to initialize the form
            association_dict = associator.guess_association_dict(headers)


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

    return dict(
        title=u"Import des dossiers, étape 2 : associer les champs",
        form=form.render(),
        info_message=info_message,
    )


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
        config_field_association,
        route_name="import_step2",
        permission="admin",
        renderer="base/formpage.mako",
    )
