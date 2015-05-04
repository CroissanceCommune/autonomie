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

from autonomie.views import render_api

from autonomie.mail import (
    send_mail_from_event,
    format_link,
)

log = logging.getLogger(__name__)

# Events for which a mail will be sended
EVENTS = {"valid":u"validé",
            "invalid": u"invalidé",
            "paid": u"partiellement payé",
            "resulted": u"payé"}

SUBJECT_TMPL = u"{docname} ({customer}) : {statusstr}"

MAIL_TMPL = u"""
Bonjour {username},

{docname} {docnumber} du projet {project} avec le client {customer} a été {status_verb}{gender}.

Vous pouvez {determinant} consulter ici :
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

        self.settings = self.request.registry.settings


    @property
    def recipients(self):
        """
            return the recipients' emails
        """
        if self.document.owner and self.document.owner.email:
            email = [self.document.owner.email]
        else:
            email = []
        return email

    @property
    def sendermail(self):
        """
            Return the sender's email
        """
        if 'mail.default_sender' in self.settings:
            mail = self.settings['mail.default_sender']
        else:
            log.info(u"'{0}' has not set his email".format(
                                                    self.request.user.login))
            mail = "Unknown"
        return mail

    @property
    def subject(self):
        """
            return the subject of the email
        """
        return SUBJECT_TMPL.format(
                docname=self.document.name,
                customer=self.document.customer.name,
                statusstr=render_api.format_status(self.document),
                )

    @property
    def body(self):
        """
            return the body of the email
        """
        status_verb = get_status_verb(self.new_status)

        # If the document is validated, we directly send the link to the pdf
        # file
        if self.new_status == 'valid':
            query_args = dict(view="pdf")
        else:
            query_args = {}

        addr = self.request.route_url(
                    self.document.type_,
                    id=self.document.id,
                    _query=query_args,
                    )
        addr = format_link(self.settings, addr)

        docnumber = self.document.number.lower()
        customer = self.document.customer.name.capitalize()
        project = self.document.project.name.capitalize()
        if self.document.is_invoice():
            docname = u"La facture"
            gender = u"e"
            determinant = u"la"
        elif self.document.is_cancelinvoice():
            docname = u"L'avoir"
            gender = u""
            determinant = u"le"
        else:
            docname = u"Le devis"
            gender = u""
            determinant = u"le"
        if self.document.statusComment:
            comment = self.document.statusComment
        else:
            comment = u"Aucun"

        username = render_api.format_account(self.document.owner, reverse=False)
        return MAIL_TMPL.format(
                determinant=determinant,
                username=username,
                docname=docname,
                docnumber=docnumber,
                customer=customer,
                project=project,
                status_verb=status_verb,
                gender=gender,
                addr=addr,
                comment=comment)

    def get_attachment(self):
        """
            Return the file data to be sent with the email
        """
        return None

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


def includeme(config):
    """
    Pyramid's incusion mechanism
    """
    config.add_subscriber(send_mail_from_event, StatusChanged)
