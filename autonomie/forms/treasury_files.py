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

import colander
from autonomie.forms import id_node


class MailSchema(colander.MappingSchema):
    company_id = id_node()
    attachment = colander.SchemaNode(
        colander.String(),
        missing=colander.drop,
    )


class MailsSchema(colander.SequenceSchema):
    mail = MailSchema()


class MailSendingSchema(colander.Schema):
    mails = MailsSchema()
    mail_subject = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=1)
    )
    mail_message = colander.SchemaNode(
        colander.String(),
        validator=colander.Length(min=1)
    )
    force = colander.SchemaNode(
        colander.Boolean(),
        missing=colander.drop,
    )
