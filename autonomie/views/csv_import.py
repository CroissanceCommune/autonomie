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
import os
import logging
from pyramid.httpexceptions import HTTPFound
from deform import (
    Form,
    ValidationFailure,
    Button,
)

from autonomie.csv_import import (
    CsvImportAssociator,
    get_csv_reader,
)
from autonomie.models.user import UserDatas
from autonomie.forms.csv_import import (
    CsvFileUploadSchema,
    AssociationSchema,
)
from autonomie.resources import fileupload_js
from autonomie.views import BaseFormView


log = logging.getLogger(__name__)


# The key we use to store informations about the current imported csv file in
# the user's sessioSESSION_KEY = "csv_import"
SESSION_KEY = "csv_import"


#TODO : ask the type of model we want to import in step 1
class CsvFileUploadView(BaseFormView):
    """
    First step view for csv file importation
    """
    schema = CsvFileUploadSchema()

    def before(self, form):
        """
        Ensure the fileupload js stuff is loaded
        """
        fileupload_js.need()

    def submit_success(self, appstruct):
        """
        Launched on successfull file upload
        """
        log.debug(u"The csv file has been uploaded")
        log.debug(appstruct)
        uid = appstruct['csv_file']['uid']
        return HTTPFound(
            self.request.route_path(
                'import_step2',
                _query=dict(uid=uid),
            )
        )


def get_current_csv(request):
    """
    Return the csv file currently stored in the user's session

    :returns: a csv dictreader object with the actual csv datas
    :raises KeyError: if no file datas are stored in the current session
    """
    # Related to pyramid_deform's way to store temporary datas on disk
    tempdir = request.registry.settings['pyramid_deform.tempdir']
    file_uid = request.GET['uid']
    file_informations = request.session['substanced.tempstore'][file_uid]
    filename = file_informations['randid']
    filepath = os.path.join(tempdir, filename)
    filebuffer = open(filepath, 'r')
    return get_csv_reader(filebuffer)


def config_field_association(request):
    """
    View for field association configuration
    Dynamically build a form regarding the previously stored csv datas

    :param request: the pyramid request object
    """
    associator = CsvImportAssociator(UserDatas)
    csv_obj = get_current_csv(request)
    headers = csv_obj.fieldnames
    association_dict = associator.guess_association_dict(headers)

    appstruct = {'entries': []}
    for csv_key, model_attribute in association_dict.items():
        appstruct['entries'].append(
            {
                'csv_field': csv_key,
                "model_attribute": model_attribute
            }
        )
    schema = AssociationSchema().bind(
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
    if 'submit' in request.POST:
        controls = request.POST.items()
        log.info(u"Field association has been configured, we're going to \
    import")
        try:
            importation_datas = form.validate(controls)
        except ValidationFailure, form:
            log.exception(u"Error on field association")
        else:
            action = importation_datas['action']
            id_key = importation_datas['id_key']

            from collections import OrderedDict
            association_dict = OrderedDict()
            for entry in importation_datas['entries']:
                association_dict[entry['csv_field']] = entry['model_attribute']
            log.info(u"The resulting options : ")
            log.info(association_dict)
            log.info(u"Action : %s , id_key : %s" % (action, id_key))
    if 'cancel' in request.POST:
        return HTTPFound(request.route_path('import_step1'))
    else:
        form.set_appstruct(appstruct)
    return dict(
        title=u"Import de données : associer les champs",
        form=form.render(),
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
