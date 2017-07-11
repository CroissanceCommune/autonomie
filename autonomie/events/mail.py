# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie_base.mail import send_mail


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
