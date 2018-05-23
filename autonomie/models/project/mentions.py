# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Mentions inclues dans les devis et factures

Configurables par l'administrateur
"""
from sqlalchemy import (
    Column,
    ForeignKey,
    Boolean,
    String,
    Integer,
)
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)


class ProjectTypeMention(DBBASE):
    """
    Table relationnelle entre les types de projet et les mentions de
    devis/factures
    """
    __tablename__ = "project_type_mention"
    __table_args__ = default_table_args
    project_type_id = Column(
        ForeignKey('base_project_type.id'),
        primary_key=True,
        info={
            "colanderalchemy": {'title': u"Type de projet"}
        }
    )
    task_mention_id = Column(
        ForeignKey('task_mention.id'),
        primary_key=True,
        info={
            "colanderalchemy": {'title': u"Mention"}
        }
    )
    doctypes = Column(
        String(32),
        primary_key=True,
        info={'colanderalchemy': {"title": u"Types de document"}}
    )
    mandatory = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': u"Obligatoires ?",
                "description": u"Si cette mention n'est pas obligatoire, elle "
                u"sera proposée optionnellement dans le formulaire d'édition "
                u"associé",
            }
        },
    )
    order = Column(
        Integer, default=0, info={'colanderalchemy': {'exclude': True}}
    )
