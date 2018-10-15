# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from zope.interface.verify import verifyObject
from autonomie_base.mail import send_mail
from autonomie.interfaces import IMailEventWrapper


def send_mail_from_event(mail_event_object):
    """
        send a mail to dests with subject and body beeing set

        :param @mail_event_object: an mail_event_object object providing :
            The following methods :
                is_key_event : return True or False
                get_attachment : return an attachment object or None

            The following attributes:
                request : access to the current request object
                sendermail: the mail's sender
                recipients : list of recipients
                subject : the mail's subject
                body : the body of the mail

    """
    verifyObject(IMailEventWrapper, mail_event_object)
    if mail_event_object.is_key_event():
        recipients = mail_event_object.recipients
        if recipients:
            send_mail(
                mail_event_object.request,
                recipients,
                mail_event_object.body,
                mail_event_object.subject,
                mail_event_object.get_attachment(),
            )
