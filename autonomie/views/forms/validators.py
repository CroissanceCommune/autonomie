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