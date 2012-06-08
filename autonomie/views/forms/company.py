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
    Company form schemas
"""
import colander
import logging

from deform import FileData

from autonomie.utils.forms import deferred_edit_widget
from autonomie.utils.forms import deferred_upload_widget
from autonomie.utils.forms import validate_image_mime
from autonomie.utils.forms import get_mail_input

log = logging.getLogger(__name__)
HEADER_PATH = "header"
LOGO_PATH = "logo"


class CompanySchema(colander.MappingSchema):
    """
        Company add/edit form schema
    """
    name = colander.SchemaNode(colander.String(),
                               widget=deferred_edit_widget,
                               title=u'Nom')
    goal = colander.SchemaNode(colander.String(),
                                title=u'Objet')
    logo = colander.SchemaNode(FileData(),
                            widget=deferred_upload_widget(path=LOGO_PATH),
                            title=u'Logo',
                            validator=validate_image_mime)
    email = get_mail_input(missing=u'')
    phone = colander.SchemaNode(colander.String(),
                            title=u'Téléphone',
                            missing=u'')
    mobile = colander.SchemaNode(colander.String(),
                            title=u'Téléphone portable',
                            missing=u'')
    RIB = colander.SchemaNode(colander.String(),
                            widget=deferred_edit_widget,
                            title=u'RIB',
                            missing=u'')
    IBAN = colander.SchemaNode(colander.String(),
                            widget=deferred_edit_widget,
                            title=u'IBAN',
                            missing=u'')
    header = colander.SchemaNode(FileData(),
                            widget=deferred_upload_widget(path=HEADER_PATH),
                            title=u'Entête des PDF',
                            validator=validate_image_mime
                            )
