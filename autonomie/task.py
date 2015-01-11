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
import time
import transaction

from celery.task import task
from celery.utils.log import get_task_logger

from autonomie.models.job import CsvImportJob
from autonomie.csv_import import (
    get_csv_import_associator,
    get_csv_importer,
)


logger = get_task_logger(__name__)

JOB_RETRIEVE_ERROR = u"We can't retrieve the job {jobid}, the task is cancelled"


def record_failure(job_id, task_id, e):
    """
    Record a job's failure
    """
    transaction.begin()
    from autonomie.models.base import DBSESSION
    job = DBSESSION().query(CsvImportJob).filter(
        CsvImportJob.id==job_id
    ).first()
    job.jobid = task_id
    job.status = "failed"
    job.error_messages = [u"%s" % e]
    transaction.commit()


# Here we use the bind argument so that the task will be attached as a bound
# method and thus we can access attributes like request
@task(bind=True)
def async_import_datas(
    self, model_type, job_id, association_dict, csv_filepath, id_key, action):
    """
    Launch the import of the datas provided in the csv_filepath

    :param str model_type: A handled model_type
    :param int job_id: The id of the db job object that should handle the return
        datas
    :param dict association_dict: describes the association
        csv_key<->SQLA model attribute
    :param str csv_filepath: The absolute path to the csv file
    :param str id_key: The model attribute used to handle updates
    :param str action: The name of the action we want to run
        (insert/update/override)
    """
    logger.info(u"We are launching an asynchronous csv import")
    logger.info(u"  The job id : %s" % job_id)
    logger.info(u"  The csv_filepath : %s" % csv_filepath)
    logger.info(u"  The association dict : %s" % association_dict)
    logger.info(u"  The id key : %s" % id_key)

    transaction.begin()
    from autonomie.models.base import DBSESSION
    # We sleep a bit to wait for the current request to be finished : since we
    # use a transaction manager, the delay call launched in a view is done
    # before the job  element is commited to the bdd (at the end of the request)
    # if we query for the job too early, the session will not be able to
    # retrieve the newly created job
    time.sleep(10)
    job = DBSESSION().query(CsvImportJob).filter(
        CsvImportJob.id==job_id
    ).first()

    if job is None:
        logger.exception(JOB_RETRIEVE_ERROR.format(job_id))
        return

    task_id = self.request.id
    job.jobid = task_id
    # TODO : handle the type of datas we import
    try:
        associator = get_csv_import_associator(model_type)
        associator.set_association_dict(association_dict)
        csv_buffer = open(csv_filepath, 'r')
        importer = get_csv_importer(
            model_type,
            csv_buffer,
            associator,
            action=action,
            id_key=id_key
        )
        logger.info(u"Importing the datas")
        importer.import_datas()
        logger.info(u"We update the job informations")
        for key, value in importer.log().items():
            setattr(job, key, value)
        job.status = "completed"
        DBSESSION().merge(job)
    except Exception as e:
        transaction.abort()
        logger.exception(u"The transaction was aborted")
        record_failure(job_id, task_id, e)
        logger.info(u"* Task FAILED !!!")
        # TODO : log failed task
    else:
        transaction.commit()
        logger.info(u"The transaction has been commited")
        logger.info(u"* Task SUCCEEDED !!!")
    return ""
