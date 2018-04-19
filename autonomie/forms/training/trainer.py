# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.training.trainer import TrainerDatas


FORM_GRID = {
    u"Profil Professionnel": (
        (('specialty', 6),),
        (('linkedin', 3), ('viadeo', 3)),
        (('career', 6), ('qualifications', 6)),
        (('background', 6), ('references', 6)),
    ),
    u"Concernant votre activité de formation": (
        (('motivation', 6),),
        (('approach', 6),),
    ),
    u"Un petit peu de vous": (
        (('temperament', 6), ('indulgence', 6)),
        (('sound', 6), ('object_', 6)),
    ),
}


def customize_schema(schema):
    """
    Customize the given TrainerDatas schema to setup specific widgets ...
    """
    return schema


def get_add_edit_trainerdatas_schema():
    """
    Build the form schemas for adding/modifying a TrainerDatas entry

    :returns: a colanderalchemy.SQLAlchemySchemaNode
    """
    schema = SQLAlchemySchemaNode(
        TrainerDatas,
        excludes=('name', '_acl', 'user_id', 'active')
    )
    customize_schema(schema)
    return schema
