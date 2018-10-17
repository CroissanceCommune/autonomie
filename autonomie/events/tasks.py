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
Handle task (invoice/estimation) related events
"""
import logging
from zope.interface import implements

from autonomie.utils.strings import (
    format_status,
    format_account,
)

from autonomie_base.mail import (
    format_link,
)
from autonomie.interfaces import IMailEventWrapper

logger = logging.getLogger(__name__)

# Events for which a mail will be sended
EVENTS = {
    "valid": u"validé",
    "invalid": u"invalidé",
    "paid": u"partiellement payé",
    "resulted": u"payé"
}

SUBJECT_TMPL = u"{docname} ({customer}) : {statusstr}"

MAIL_TMPL = u"""
Bonjour {username},

{docname} {docnumber} du projet {project} avec le client {customer} \
a été {status_verb}{gender}.

Vous pouvez {determinant} consulter ici :
{addr}

Commentaires associés au document :
    {comment}"""


class TaskMailStatusChangedWrapper(object):
    implements(IMailEventWrapper)

    def __init__(self, event):
        self.event = event
        self.request = event.request
        self.status = event.status
        # Silly hack :
        # When a payment is registered, the new status is "paid",
        # if the resulted box has been checked, it's set to resulted later on.
        # So here, we got the paid status, but in reality, the status has
        # already been set to resulted. This hack avoid to send emails with the
        # wrong message
        if self.status == 'paid' and self.event.node.paid_status == 'resulted':
            self.status = 'resulted'
        self.settings = self.request.registry.settings

    @property
    def recipients(self):
        """
            return the recipients' emails
        """
        if self.event.node.company.email:
            email = [self.event.node.company.email]
        elif self.event.node.owner and self.event.node.owner.email:
            email = [self.event.node.owner.email]
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
            logger.info(
                u"'{0}' has not set his email".format(
                    self.event.request.user.login
                )
            )
            mail = "Unknown"
        return mail

    @property
    def subject(self):
        """
            return the subject of the email
        """
        return SUBJECT_TMPL.format(
            docname=self.event.node.name,
            customer=self.event.node.customer.label,
            statusstr=format_status(self.event.node),
        )

    @property
    def body(self):
        """
            return the body of the email
        """
        status_verb = get_status_verb(self.status)

        # If the document is validated, we directly send the link to the pdf
        # file
        if self.status == 'valid':
            query_args = dict(view="pdf")
        else:
            query_args = {}

        addr = self.request.route_url(
                    "/%ss/{id}.html" % self.event.node.type_,
                    id=self.event.node.id,
                    _query=query_args,
                    )
        addr = format_link(self.settings, addr)

        docnumber = self.event.node.internal_number.lower()
        customer = self.event.node.customer.label
        project = self.event.node.project.name.capitalize()
        if self.event.node.type_ == 'invoice':
            docname = u"La facture"
            gender = u"e"
            determinant = u"la"
        elif self.event.node.type_ == 'cancelinvoice':
            docname = u"L'avoir"
            gender = u""
            determinant = u"le"
        else:
            docname = u"Le devis"
            gender = u""
            determinant = u"le"
        if self.event.node.status_comment:
            comment = self.event.node.status_comment
        else:
            comment = u"Aucun"

        username = format_account(self.event.node.owner, reverse=False)
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
        if self.status in EVENTS.keys() \
                and not self.event.node.type_ == 'cancelinvoice':
            return True
        else:
            return False


def get_status_verb(status):
    """
    Return the verb associated to the current status
    """
    return EVENTS.get(status, u"")


def on_status_changed_alert_related_business(event):
    """
    Alert the related business on Invoice status change

    :param event: A StatusChanged instance with an Invoice attached
    """
    if event.status == 'valid':
        business = event.node.business
        logger.info(
            u"+ Status Changed : updating business {} invoicing status".format(
                business.id
            )
        )
        business.status_service.update_invoicing_status(business, event.node)
        business.status_service.update_status(business)
