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
from sqlalchemy.orm.exc import NoResultFound
from pyramid.threadlocal import get_current_request

from celery.task import task
from celery.utils.log import get_task_logger

from autonomie.models.job import (
    CsvImportJob,
    MailingJob,
)
from autonomie.models.company import Company
from autonomie.mail import (
    send_salary_sheet,
    UndeliveredMail,
    MailAlreadySent,
)
from autonomie.csv_import import (
    get_csv_import_associator,
    get_csv_importer,
)


logger = get_task_logger(__name__)

JOB_RETRIEVE_ERROR = u"We can't retrieve the job {jobid}, the task is cancelled"


def record_failure(job_model, job_id, task_id, e):
    """
    Record a job's failure
    """
    transaction.begin()
    # We fetch the job again since we're in a new transaction
    from autonomie.models.base import DBSESSION
    job = DBSESSION().query(job_model).filter(
        job_model.id==job_id
    ).first()
    job.jobid = task_id
    job.status = "failed"
    # We append an error
    if hasattr(job, 'error_messages'):
        if job.error_messages is None:
            job.error_messages = []
        job.error_messages.append(u"%s" % e)
    transaction.commit()


def get_job(celery_request, job_model, job_id):
    """
    Return the current executed job (in autonomie's sens)

    :param obj job_model: The Job model
    :param obj celery_request: The current celery request object
    :param int job_id: The id of the job

    :returns: The current job
    :raises sqlalchemy.orm.exc.NoResultFound: If the job could not be found
    """
    from autonomie.models.base import DBSESSION
    # We sleep a bit to wait for the current request to be finished : since we
    # use a transaction manager, the delay call launched in a view is done
    # before the job  element is commited to the bdd (at the end of the request)
    # if we query for the job too early, the session will not be able to
    # retrieve the newly created job
    time.sleep(10)
    job = DBSESSION().query(job_model).filter(
        job_model.id==job_id
    ).one()
    job.jobid = celery_request.id
    return job


# Here we use the bind argument so that the task will be attached as a bound
# method and thus we can access attributes like request
@task(bind=True)
def async_import_datas(
    self, model_type, job_id, association_dict, csv_filepath, id_key, action,
    force_rel_creation):
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
    :param bool force_rel_creation: Force the creation of configurable related
    elements
    """
    logger.info(u"We are launching an asynchronous csv import")
    logger.info(u"  The job id : %s" % job_id)
    logger.info(u"  The csv_filepath : %s" % csv_filepath)
    logger.info(u"  The association dict : %s" % association_dict)
    logger.info(u"  The id key : %s" % id_key)
    logger.info(u"  Action : %s" % action)

    from autonomie.models.base import DBSESSION
    transaction.begin()
    try:
        job = get_job(self.request, CsvImportJob, job_id)
    except NoResultFound:
        logger.exception(JOB_RETRIEVE_ERROR.format(job_id))
        return

    job.jobid = self.request.id

    # TODO : handle the type of datas we import
    try:
        associator = get_csv_import_associator(model_type)
        associator.set_association_dict(association_dict)
        csv_buffer = open(csv_filepath, 'r')
        importer = get_csv_importer(
            DBSESSION(),
            model_type,
            csv_buffer,
            associator,
            action=action,
            id_key=id_key,
            force_rel_creation=force_rel_creation,
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
        logger.exception(u"The transaction has been aborted")
        logger.error(u"* Task FAILED !!!")
        record_failure(CsvImportJob, job_id, self.request.id, e)
    else:
        transaction.commit()
        logger.info(u"The transaction has been commited")
        logger.info(u"* Task SUCCEEDED !!!")
    return ""


def _mail_format_message(mail_message_tmpl, company, kwds):
    """
    Return the message to be sent to a single company
    :param str mail_message_tmpl: Template for the mail message
    :param obj company: The company object
    :param dict kwds: Additionnal keywords to pass to the string.format method
    """
    kwds['company'] = company
    message = mail_message_tmpl.format(**kwds)
    return message


@task(bind=True)
def async_mail_salarysheets(
    self, job_id, mails, force):
    """
    Asynchronously sent a bunch of emails with attached salarysheets

    :param int job_id: The id of the MailSendJob
    :param mails: a list of dict compound of
        {
            'id': company_id,
            'attachment': attachment filename,
            'attachment_path': attachment filepath,
            'message': The mail message,
            'subject': The mail subject,
            'company_id': The id of the company,
            'email': The email to send it to,
        }
    :param force: Should we force the mail sending
    """
    logger.info(u"We are launching an asynchronous mail sending operation")
    logger.info(u"  The job id : %s" % job_id)

    request = get_current_request()
    from autonomie.models.base import DBSESSION
    # Sleep a bit in case the db was slow
    time.sleep(10)

    # First testing if the job was created
    try:
        job = get_job(self.request, MailingJob, job_id)
    except NoResultFound:
        logger.exception(JOB_RETRIEVE_ERROR.format(job_id))
        return

    mail_count = 0
    error_count = 0
    error_messages = []
    for mail_datas in mails:
        # since we send a mail out of the transaction process, we need to commit
        # each mail_history instance to avoid sending and not storing the
        # history
        try:
            transaction.begin()
            company_id = mail_datas['company_id']
            email = mail_datas['email']

            if email is None:
                logger.error(u"no mail found for company {0}".format(
                    company_id)
                )
                continue
            else:
                message = mail_datas['message']
                subject = mail_datas['subject']
                logger.info(u"  The mail subject : %s" % subject)
                logger.info(u"  The mail message : %s" % message)

                mail_history = send_salary_sheet(
                    request,
                    email,
                    company_id,
                    mail_datas['attachment'],
                    mail_datas['attachment_path'],
                    force=force,
                    message=message,
                    subject=subject,
                )
                # Stores the history of this sent email
                DBSESSION().add(mail_history)

        except MailAlreadySent as e:
            error_count += 1
            msg = u"Ce fichier a déjà été envoyé {0}".format(
                mail_datas['attachment']
            )
            error_messages.append(msg)
            logger.exception(u"Mail already delivered")
            logger.error(u"* Part of the Task FAILED")
            continue

        except UndeliveredMail as e:
            error_count += 1
            msg = u"Impossible de délivrer de mail à l'entreprise {0} \
(mail : {1})".format(company_id, email)
            error_messages.append(msg)
            logger.exception(u"Unable to deliver an e-mail")
            logger.error(u"* Part of the Task FAILED")
            continue

        except Exception as e:
            error_count += 1
            transaction.abort()
            logger.exception(u"The transaction has been aborted")
            logger.error(u"* Part of the task FAILED !!!")
            error_messages.append(u"{0}".format(e))

        else:
            mail_count += 1
            transaction.commit()
            logger.info(u"The transaction has been commited")
            logger.info(u"* Part of the Task SUCCEEDED !!!")
            time.sleep(1)

    logger.info(u"-> Task finished")
    transaction.begin()
    job = get_job(self.request, MailingJob, job_id)
    logger.info(u"The job : %s" % job)
    job.jobid = self.request.id
    if error_count == 0:
        job.status = "completed"
    else:
        job.status = "failed"
    job.messages = [u"{0} mails ont été envoyés".format(mail_count)]
    job.messages.append(
        u"{0} mails n'ont pas pu être envoyés".format(error_count)
    )
    job.error_messages = error_messages
    DBSESSION().merge(job)
    logger.info(u"Committing the transaction")
    transaction.commit()
