# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.files import FileType
from autonomie.forms import customize_field


def get_admin_file_type_schema():
    """
    Build a schéma to administrate file types

    :rtype: :class:`colanderalchemy.SQLAlchemySchemaNode`
    """
    schema = SQLAlchemySchemaNode(FileType, includes=('label',))
    customize_field(schema, 'label', title=u"Libellé")
    return schema
