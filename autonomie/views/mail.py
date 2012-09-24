# -*- coding: utf-8 -*-
# * File Name : mail.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 26-06-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Mail sending tools
"""
import logging

from pyramid.events import subscriber
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message
from pyramid.threadlocal import get_current_registry

from autonomie.views.render_api import format_status

log = logging.getLogger(__name__)


class StatusChanged(object):
    """
        Event raised when a document status changes
    """
    def __init__(self, request, document):
        self.request = request
        self.document = document

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
        if self.request.user.email:
            mail = self.request.user.email
        elif settings.has_key('mail.default_sender'):
            mail = settings['mail.default_sender']
        else:
            log.info(u"The current user : {0} has not set his email".format(
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
        status_verb = get_status_verb(self.document.CAEStatus)
        if self.document.is_invoice():
            body = u"La facture {0} du projet {1} (avec le client {2}) \
a été {3}e.".format(self.document.number,
                    self.document.project.name,
                    self.document.project.client.name,
                    status_verb)
            addr = self.request.route_url("invoice", id=self.document.id)
        else:
            body = u"Le devis {0} du projet {1} (avec le client {2}) \
a été {3}.".format(self.document.number,
                   self.document.project.name,
                   self.document.project.client.name,
                   status_verb)
            addr = self.request.route_url("estimation", id=self.document.id)
        body += u"\n\n"
        body += addr
        if self.document.statusComment:
            body += u"\n\nCommentaires associés aux document :"
            body += self.document.statusComment
        return body

    def is_key_event(self):
        """
            Return True if the new status requires a mail to be sent
        """
        if self.document.CAEStatus in ("valid", "invalid", "paid") and \
                                    not self.document.is_cancelinvoice():
            return True
        else:
            return False


def get_status_verb(status):
    """
        Return the verb associated to the current status
    """
    if status == 'valid':
        return u"validé"
    elif status == 'invalid':
        return u"invalidé"
    elif status == "paid":
        return u"payé"
    else:
        return u""


@subscriber(StatusChanged)
def send_mail(event):
    """
        send a mail to dests with subject and body beeing set
    """
    log.debug("# A status Changed event has been fired #")
    if event.is_key_event():
        recipients = event.recipients
        if recipients:
            log.debug(u" + It's a key event, we send an email to {0}".format(
                                                            recipients))
            log.debug(event.subject)
            log.debug(event.body)
            try:
                mailer = get_mailer(event.request)
                message = Message(subject=event.subject,
                      sender=event.sendermail,
                      recipients=recipients,
                      body=event.body)
                mailer.send_immediately(message)
            except:
                log.exception(" - An error has occured while sending the \
email(s)")
        else:
            log.debug(" - No email has been set for the recipient")
    else:
        log.debug(" - It's not a key event, nothing to do")
