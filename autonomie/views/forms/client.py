# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 10-04-2012
# * Last Modified :
#
# * Project :
#
"""
    Client handling forms schemas
"""
import colander
import logging

from deform import widget

from autonomie.models.model import Client
from autonomie.views.forms.widgets import get_mail_input
from autonomie.views.forms.widgets import DisabledInput

log = logging.getLogger(__name__)

@colander.deferred
def deferred_ccode_valid(node, kw):
    company = kw['company']
    company_id = company.id
    client = kw.get('client')
    def unique_ccode(node, value):
        """
            Test customer code unicity
        """
        if len(value) != 4:
            message = u"Le code client doit contenir 4 caractères."
            raise colander.Invalid(node, message)
        #Test unicity
        query = Client.query().filter(Client.company_id==company_id)\
                .filter(Client.code==value)
        if client:
            # In edit mode, it will always fail
            query = query.filter(Client.id!=client.id)
        result = query.all()

        if len(result):
            message = u"Vous avez déjà utilisé ce code '{0}' pour un autre \
client".format(value)
            raise colander.Invalid(node, message)
    return unique_ccode

class ClientSchema(colander.MappingSchema):
    """
        Schema for customer insertion
    """
    code = colander.SchemaNode(colander.String(),
                             widget=widget.TextInputWidget(mask='****'),
                             title=u'Code',
                             validator=deferred_ccode_valid)
    name = colander.SchemaNode(colander.String(),
                            title=u"Nom de l'entreprise",
                            validator=colander.Length(max=255))
    contactLastName = colander.SchemaNode(colander.String(),
                            title=u'Nom du contact principal',
                            validator=colander.Length(max=255))
    contactFirstName = colander.SchemaNode(colander.String(),
                        title=u"Prénom du contact principal",
                        missing=u"",
                        validator=colander.Length(max=255))
    function = colander.SchemaNode(colander.String(),
                        title=u"Fonction du contact principal",
                        missing=u"",
                        validator=colander.Length(max=255))
    email = get_mail_input( missing=u'')
    phone = colander.SchemaNode(colander.String(),
                                title=u'Téléphone',
                                missing=u'',
                                validator=colander.Length(max=50))
    fax = colander.SchemaNode(colander.String(),
                                title=u"Fax",
                                missing=u"",
                                validator=colander.Length(max=50))
    address = colander.SchemaNode(colander.String(),
                    title=u'Adresse',
                    missing=u'',
                    validator=colander.Length(max=255))
    zipCode = colander.SchemaNode(colander.String(),
                    title=u'Code postal',
                    missing=u'',
                    validator=colander.Length(max=20))
    city = colander.SchemaNode(colander.String(),
                    title=u'Ville',
                    missing=u'',
                    validator=colander.Length(max=255))
    country = colander.SchemaNode(colander.String(),
                title=u"Pays",
                missing=u'France',
                validator=colander.Length(max=255)
                )
    intraTVA = colander.SchemaNode(colander.String(),
                    title=u"TVA intracommunautaire",
                    validator=colander.Length(max=50),
                    missing=u'')
    comments = colander.SchemaNode(colander.String(),
            widget=widget.TextAreaWidget(cols=80, rows=4),
            title=u'Commentaires',
            missing=u'')
