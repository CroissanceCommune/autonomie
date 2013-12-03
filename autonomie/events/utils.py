# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
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
#
"""
    Tools used to manage events
"""
import logging
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message

log = logging.getLogger(__file__)

def send_mail(event):
    """
        send a mail to dests with subject and body beeing set

        :param @event: an event object providing :
            The following methods :
                is_key_event : return True or False
                get_attachment : return an attachment object or None

            The following attributes:
                request : access to the current request object
                sendermail: the mail's sender
                recipients : list of recipients (a string)
                subject : the mail's subject
                body : the body of the mail

    """
    if event.is_key_event():
        recipients = event.recipients
        if recipients:
            log.info(u"Sending an email to '{0}'".format(recipients))
            try:
                mailer = get_mailer(event.request)
                message = Message(subject=event.subject,
                      sender=event.sendermail,
                      recipients=recipients,
                      body=event.body)
                attachment = event.get_attachment()
                if attachment:
                    message.attach(attachment)
                mailer.send_immediately(message)
            except:
                log.exception(u" - An error has occured while sending the \
email(s)")
