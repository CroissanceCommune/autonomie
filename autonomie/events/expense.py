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
"""
Events used while handling expenses :
    Send email

"""
import datetime
import logging

from autonomie.mail import (
    format_link,
    send_mail_from_event,
)
from autonomie.views.render_api import (
    format_account,
    format_date,
)

log = logging.getLogger(__name__)

# Events for which a mail will be sended
EVENTS = {
    "valid": u"validée",
    "invalid": u"invalidée",
    "paid": u"partiellement payée",
    "resulted": u"payée",
}

MAIL_TMPL = u"""
Bonjour {owner},

La note de dépense de {owner} pour la période {date} a été {status_verb}.

Vous pouvez la consulter ici :
{addr}

Commentaires associés au document :
    {comment}"""


EXPENSE_NOTIFY_STATUS = dict(
    (
        ("valid", u"Validée par {0} le {1}"),
        ('paid', u"Paiement partiel notifié par {0} le {1}"),
        ('resulted', u"Paiement notifié par {0} le {1}")
    )
)


class StatusChanged(object):
    """
        Event fired when an expense changes its status
    """
    def __init__(self, request, expense, status, comment=None):
        self.request = request
        self.expense = expense
        self.new_status = status
        self.comment = comment
        self.settings = self.request.registry.settings
        log.debug("Expense StatusChanged event new status : %s" % status)

    @property
    def recipients(self):
        """
            return the recipients' emails
        """
        if self.expense.user.email:
            email = [self.expense.user.email]
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
            log.info(
                u"'{0}' has not set his email".format(
                    self.request.user.login
                )
            )
            mail = "Unknown"
        return mail

    def format_expense_notification(self):
        """
        Return a formatted string for expense status notification
        """
        status_str = EXPENSE_NOTIFY_STATUS.get(self.new_status)
        account_label = format_account(self.request.user)
        date_label = format_date(datetime.date.today())
        return status_str.format(account_label, date_label)

    @property
    def subject(self):
        """
            return the subject of the email
        """
        subject = u"Notes de dépense de {0} : {1}".format(
            format_account(self.expense.user),
            self.format_expense_notification()
        )
        return subject

    @property
    def body(self):
        """
            return the body of the email
        """
        owner = format_account(self.expense.user)
        date = u"{0}/{1}".format(self.expense.month, self.expense.year)
        status_verb = get_status_verb(self.new_status)
        addr = self.request.route_url("expensesheet", id=self.expense.id)
        addr = format_link(self.settings, addr)

        return MAIL_TMPL.format(
            owner=owner,
            addr=addr,
            date=date,
            status_verb=status_verb,
            comment=self.comment,
        )

    @staticmethod
    def get_attachment():
        """
            Return the file data to be sent with the email
        """
        return None

    def is_key_event(self):
        """
            Return True if the new status requires a mail to be sent
        """
        if self.new_status in EVENTS.keys():
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
