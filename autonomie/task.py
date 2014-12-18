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
All asynchronous tasks runned through Autonomie are stored here
Tasks are handled by a celery service
Redis is used as the central bus
"""
import transaction
import traceback

from celery.task import task

from autonomie.models.user import UserDatas
from autonomie.csv_import import (
    CsvImportAssociator,
    CsvImporter,
)

@task
def async_import_datas(association_dict, csv_filepath, id_key, action):
    """
    Launch the import of the datas provided in the csv_filepath
    """
    print(association_dict)
    transaction.begin()
    # TODO : handle the type of datas we import
    try:
        associator = CsvImportAssociator(UserDatas)
        associator.set_association_dict(association_dict)
        csv_buffer = open(csv_filepath, 'r')
        importer = CsvImporter(
            UserDatas,
            csv_buffer,
            associator,
            action=action,
            id_key=id_key
        )
        importer.import_datas()
    except:
        traceback.print_exc()
        transaction.abort()
    else:
        transaction.commit()

    result = dict(
        messages=importer.messages,
        err_messages=importer.err_messages,
        in_error_fields=importer.in_error_fields,
        unhandled_datas=importer.unhandled_datas,
    )
    return result
