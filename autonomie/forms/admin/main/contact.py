# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
from autonomie import forms
from autonomie.forms.admin import CONFIGURATION_KEYS


class ContactConfigSchema(colander.MappingSchema):
    cae_admin_mail = colander.SchemaNode(
        colander.String(),
        title=CONFIGURATION_KEYS['cae_admin_mail']['title'],
        description=CONFIGURATION_KEYS['cae_admin_mail']['description'],
        validator=forms.mail_validator(),
        missing=u""
    )
