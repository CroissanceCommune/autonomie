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
    Mail sending tools
"""
import logging

from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from pyramid.threadlocal import get_current_registry

from autonomie.views.render_api import format_status

log = logging.getLogger(__name__)

# Events for which a mail will be sended
EVENTS = {"valid":u"validé",
            "invalid": u"invalidé",
            "paid": u"partiellement payé",
            "resulted": u"payé"}


MAIL_TMPL = u"""{docname} {docnumber} du projet {project} avec le client {customer} a été {status_verb}{gender}.

{addr}

Commentaires associés au document :
    {comment}"""


class StatusChanged(object):
    """
        Event raised when a document status changes
    """
    def __init__(self, request, document, status):
        self.request = request
        self.document = document
        self.new_status = status
        # Silly hack :
        # When a payment is registered, the new status is "paid",
        # if the resulted box has been checked, it's set to resulted later on.
        # So here, we got the paid status, but in reality, the status has
        # already been set to resulted. This hack avoid to send emails with the
        # wrong message
        if status == 'paid' and self.document.CAEStatus == 'resulted':
            self.new_status = 'resulted'

    def format_mail(self, mail):
        """
            Format the mail address to fit gmail's rfc interpretation
        """
        return u"<{0}>".format(mail)

    @property
    def recipients(self):
        """
            return the recipients' emails
        """
        if self.document.owner.email:
            email = [self.format_mail(self.document.owner.email)]
        else:
            email = []
        return email

    @property
    def sendermail(self):
        """
            Return the sender's email
        """
        settings = get_current_registry().settings
        if 'mail.default_sender' in settings:
            mail = settings['mail.default_sender']
        else:
            log.info(u"'{0}' has not set his email".format(
                                                    self.request.user.login))
            mail = "Unknown"
        return self.format_mail(mail)

    @property
    def subject(self):
        """
            return the subject of the email
        """
        return u"{0} : {1}".format(self.document.name,
                                    format_status(self.document))

    @property
    def body(self):
        """
            return the body of the email
        """
        status_verb = get_status_verb(self.new_status)
        addr = self.request.route_url(self.document.type_, id=self.document.id)
        docnumber = self.document.number
        customer = self.document.customer.name
        project = self.document.project.name
        if self.document.is_invoice():
            docname = u"La facture"
            gender = u"e"
        else:
            docname = u"Le devis"
            gender = u""
        if self.document.statusComment:
            comment = self.document.statusComment
        else:
            comment = u"Aucun"
        return MAIL_TMPL.format(docname=docname,
                docnumber=docnumber,
                customer=customer,
                project=project,
                status_verb=status_verb,
                gender=gender,
                addr=addr,
                comment=comment)


    def is_key_event(self):
        """
            Return True if the new status requires a mail to be sent
        """
        if self.new_status in EVENTS.keys() \
                and not self.document.is_cancelinvoice():
            return True
        else:
            return False


def get_status_verb(status):
    """
        Return the verb associated to the current status
    """
    return EVENTS.get(status, u"")


def send_mail(event):
    """
        send a mail to dests with subject and body beeing set
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
                mailer.send_immediately(message)
            except:
                log.exception(u" - An error has occured while sending the \
email(s)")

def includeme(config):
    config.add_subscriber(send_mail, StatusChanged)
