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
import os
import colander
import logging

from deform import FileData

from autonomie.views.forms.widgets import deferred_edit_widget
from autonomie.views.forms.widgets import get_fileupload_widget
from autonomie.views.forms.validators import validate_image_mime
from autonomie.views.forms.widgets import get_mail_input
from autonomie.utils.image import ImageResizer

log = logging.getLogger(__name__)
HEADER_PATH = "header"
LOGO_PATH = "logo"

HEADER_RESIZER = ImageResizer(4, 1)

def get_upload_options_from_request(request, directory):
    """
        Return the upload path and url from the request object
    """
    company = request.context
    rootpath = request.registry.settings.get('autonomie.assets', '/tmp')
    store_path = os.path.join(rootpath, company.get_path(), directory)
    store_url = os.path.join("/assets", company.get_path(), directory)
    return store_path, store_url

@colander.deferred
def deferred_edit_adminonly_widget(node, kw):
    """
        return a deferred adminonly edit widget
    """
    request = kw['request']
    if request.user.is_contractor():
        return deferred_edit_widget(node, dict(edit=True))
    else:
        return deferred_edit_widget(node, dict(edit=False))

@colander.deferred
def deferred_logo_widget(node, kw):
    """
        Return the logo upload widget
    """
    request = kw['request']
    path, url = get_upload_options_from_request(request, LOGO_PATH)
    return get_fileupload_widget(url, path, request.session)

@colander.deferred
def deferred_header_widget(node, kw):
    """
        Return the header upload widget
    """
    request = kw['request']
    path, url = get_upload_options_from_request(request, HEADER_PATH)
    return get_fileupload_widget(url, path, request.session,
                                    [HEADER_RESIZER.complete])

class CompanySchema(colander.MappingSchema):
    """
        Company add/edit form schema
    """
    name = colander.SchemaNode(
            colander.String(),
            widget=deferred_edit_adminonly_widget,
            title=u'Nom')
    code_compta = colander.SchemaNode(
            colander.String(),
            widget=deferred_edit_adminonly_widget,
            title=u"Compte analytique",
            description=u"Compte analytique utilisé dans le logiciel de compta",
            missing="")
    goal = colander.SchemaNode(
            colander.String(),
            title=u'Objet')
    logo = colander.SchemaNode(
            FileData(),
            widget=deferred_logo_widget,
            title=u'Logo',
            validator=validate_image_mime,
            description=u"Charger un fichier de type image *.png *.jpeg \
*.jpg ...")
    email = get_mail_input(missing=u'')
    phone = colander.SchemaNode(
            colander.String(),
            title=u'Téléphone',
            missing=u'')
    mobile = colander.SchemaNode(
            colander.String(),
            title=u'Téléphone portable',
            missing=u'')
    compte_cg_banque = colander.SchemaNode(
            colander.String(),
            widget=deferred_edit_adminonly_widget,
            title=u"Compte CG Banque",
            missing=u"Compte CG Banque de l'entreprise")
    RIB = colander.SchemaNode(
            colander.String(),
            widget=deferred_edit_adminonly_widget,
            title=u'RIB',
            missing=u'')
    IBAN = colander.SchemaNode(
            colander.String(),
            widget=deferred_edit_adminonly_widget,
            title=u'IBAN',
            missing=u'')
    header = colander.SchemaNode(
            FileData(),
            widget=deferred_header_widget,
            title=u'Entête des fichiers PDF',
            description=u"Charger un fichier de type image *.png *.jpeg \
*.jpg ... Le fichier est idéalement au format 20/4 (par exemple 1000px x \
200 px)",
            validator=validate_image_mime)
