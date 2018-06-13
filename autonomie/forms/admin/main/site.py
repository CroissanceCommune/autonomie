# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import colander
from autonomie.forms import files

from autonomie import forms


class SiteConfigSchema(colander.MappingSchema):
    """
        Site configuration
        logos ...
    """
    logo = files.ImageNode(
        title=u"Choisir un logo",
        missing=colander.drop,
        description=u"Charger un fichier de type image *.png *.jpeg \
 *.jpg ...")

    welcome = forms.textarea_node(
        title=u"Texte d'accueil",
        richwidget=True,
        missing=u'',
        admin=True,
    )
