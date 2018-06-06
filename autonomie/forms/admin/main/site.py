# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
import deform
from autonomie.forms import files

from autonomie import forms
from autonomie.forms.validators import validate_image_mime


class SiteConfigSchema(colander.MappingSchema):
    """
        Site configuration
        logos ...
    """
    logo = colander.SchemaNode(
        deform.FileData(),
        widget=files.deferred_upload_widget,
        title=u"Choisir un logo",
        validator=validate_image_mime,
        missing=colander.drop,
        description=u"Charger un fichier de type image *.png *.jpeg \
*.jpg ...")
    welcome = forms.textarea_node(
        title=u"Texte d'accueil",
        richwidget=True,
        missing=u'',
        admin=True,
    )
