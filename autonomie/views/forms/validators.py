# -*- coding: utf-8 -*-
# * File Name : validators.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 09-07-2012
# * Last Modified :
#
# * Project :
#
"""
    colander validators
"""
import logging
import colander
log = logging.getLogger(__name__)


def validate_image_mime(node, value):
    """
        Validate mime types for image files
    """
    if value.get('mimetype'):
        if not value['mimetype'].startswith('image/'):
            message = u"Veuillez télécharger un fichier de type jpg, png, \
bmp ou gif"
            raise colander.Invalid(node, message)
