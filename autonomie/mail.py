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
Mail utilities
"""
import logging
from pyramid_mailer import get_mailer
from pyramid_mailer.message import (
    Message,
    Attachment,
)

from autonomie.exception import UndeliveredMail
from autonomie.models.files import (
    store_sent_mail,
    check_if_mail_sent,
)


log = logging.getLogger(__file__)


UNSUBSCRIBE_MSG = u"<mailto:{0}?subject=Unsubscribe-{1}>"


UNSUBSCRIBE_LINK = u"""


Vous avez reçu ce mail car vous êtes utilisateurs de l'application Autonomie. \
Si vous avez reçu ce mail par erreur, nous vous prions de nous \
en excuser. Vous pouvez vous désincrire en écrivant à \
{0}?subject=Unsubscribe-{1}."""

SALARYSHEET_MAIL_MESSAGE = u"""Bonjour,
Vous trouverez ci-joint votre bulletin de salaire.
{0}
"""

SALARYSHEET_MAIL_SUBJECT = u"Votre bulletin de salaire"



def format_mail(mail):
    """
    Format the mail address to fit gmail's rfc interpretation
    """
    return u"<{0}>".format(mail)


def format_link(settings, link):
    """
    Format a link to fit the sender's domain name if a bounce url has been
    configured
    """
    bounce_url = settings.get("mail.bounce_url")
    if bounce_url:
        url = u"http://{0}/?url={1}".format(bounce_url, link)
    else:
        url = link
    return url


def get_sender(settings):
    """
    Return the mail sender's address
    """
    if 'mail.default_sender' in settings:
        mail = settings['mail.default_sender']
    else:
        mail = "Unknown"
    return format_mail(mail)


def _handle_optout(settings, mail_body):
    """
    Add additionnal datas for optout declaration
    Allows to fit a bit more the mailing conformity
    """
    headers = {}
    optout_addr = settings.get("mail.optout_address")
    instance_name = settings.get('autonomie.instance_name')
    if optout_addr and instance_name:
        headers['Precedence'] = 'bulk'
        headers['List-Unsubscribe'] = UNSUBSCRIBE_MSG.format(
                optout_addr,
                instance_name,
                )
        mail_body += UNSUBSCRIBE_LINK.format(optout_addr, instance_name)
    return headers, mail_body


def send_mail(request, recipients, body, subject, attachment=None):
    """
    Try to send an email with the given datas

    :param obj request: a pyramid request object
    :param list recipients: A list of recipients strings
    :param str body: The body of the email
    :param str subject: The subject of the email
    :param obj attachment: A pyramid_mailer.message.Attachment object

    """
    if not hasattr(recipients, '__iter__'):
        recipients = [recipients]

    if len(recipients) == 0:
        return False
    log.info(u"Sending an email to '{0}'".format(recipients))
    settings = request.registry.settings
    headers, mail_body = _handle_optout(settings, body)
    try:
        recipients = [format_mail(recipient) for recipient in recipients]
        sender = get_sender(settings)
        mailer = get_mailer(request)
        message = Message(
            subject=subject,
            sender=sender,
            recipients=recipients,
            body=mail_body,
            extra_headers=headers
        )
        if attachment:
            message.attach(attachment)
        mailer.send_immediately(message)
    except Exception:
        import traceback
        traceback.print_exc()
        log.exception(u" - An error has occured while sending the \
email(s)")
        return False
    return True


def send_mail_from_event(event):
    """
        send a mail to dests with subject and body beeing set

        :param @event: an event object providing :
            The following methods :
                is_key_event : return True or False
                get_attachment : return an attachment object or None

            The following attributes:
                request : access to the current request object
                sendermail: the mail's sender
                recipients : list of recipients
                subject : the mail's subject
                body : the body of the mail
                settings : the app settings

    """
    if event.is_key_event():
        recipients = event.recipients
        if recipients:
            send_mail(
                event.request,
                recipients,
                event.body,
                event.subject,
                event.get_attachment(),
            )


def send_salary_sheet(request, company, filename, filepath, force=False, custom_msg=""):
    """
    Send a salarysheet to the given company's e-mail

    :param obj request: A pyramid request object
    :param obj company: A company instance
    :param str filepath: The path to the filename
    :param bool force: Whether to force sending this file again
    :returns: True or False
    :TypeError UndeliveredMail: When the company has no mail or if the file has
        already been sent and no force option was passed
    """
    filebuf = file(filepath, 'r')
    filedatas = filebuf.read()

    if not force and check_if_mail_sent(filedatas, company):
        log.warn(u"Undelivered email : mail already sent")
        raise UndeliveredMail(u"Mail already sent")

    filebuf.seek(0)

    if company.email is None:
        log.warn(u"Undelivered email : no mail found for company {0}".format(
            company.name)
        )
        raise UndeliveredMail(u"no mail found for company {0}".format(
            company.name)
        )
    else:
        print('Sending the file %s' % filepath)
        print("Sending it to %s" % company.email)
        attachment = Attachment(filename, "application/pdf", filebuf)

        send_mail(
            request,
            SALARYSHEET_MAIL_MESSAGE.format(custom_msg),
            SALARYSHEET_MAIL_SUBJECT,
            company.email,
            attachment,
        )
        store_sent_mail(filepath, filedatas, company)
        return True
