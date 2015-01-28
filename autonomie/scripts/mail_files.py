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
Script used to send file by mail
"""
import re
from autonomie.scripts.utils import (
    command,
    get_value,
)
from autonomie.mail import send_salary_sheet
from autonomie.models.company import Company


# Un registre contenant les regexp permettant de matcher les codes analytiques
# Et un type de fichier (filetype, regexp)
REGISTER = {
    "salarysheet": re.compile('(?P<code_compta>[^_]*).')
}
SENDERS = {
    'salarysheet': send_salary_sheet,
}


def get_company(code_compta):
    """
    Return the company associated to this code_compta
    """
    return Company.query().filter(Company.code_compta==code_compta).first()


def mail_it(arguments, env):
    """
    Send the mail

    :param arguments: arguments gotten from the command line
    :param env: the environment of our bootstrapped command
    """
    force = arguments['-f']
    filetype = get_value(arguments, 'type')
    filepath = get_value(arguments, 'file')
    filename = filepath.split('/')[-1]

    regex = REGISTER.get(filetype)
    groups = regex.match(filename)
    if groups is None:
        raise Exception(
            "The given filepath doesn't match the %s regexp" % filetype
        )

    code_compta = groups.group("code_compta")
    company = get_company(code_compta)

    if company is None:
        print(u"No company found for this code_compta : %s" % code_compta)
    else:
        print('Sending the file %s' % filepath)
        print("Sending it to %s" % company.email)
        sender = SENDERS.get(filetype)
        sender(
            env['request'],
            company.email,
            company.id,
            filename,
            filepath,
            force,
        )


def mail_cmd():
    """
    Send the given file to the email address associated to the account having the good
    Usage:
        autonomie-mail <config_uri> mail --type=<filetype> --file=<filepath> [-f]

    Options:
        -h --help   Show this screen
    """
    try:
        return command(mail_it, mail_cmd.__doc__)
    finally:
        pass
