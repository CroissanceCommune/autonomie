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
)
from sqlalchemy.orm import (
    relationship,
    backref,
)
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)


class BusinessTypeTaskMention(DBBASE):
    """
    Relationship table between BusinessType and TaskMention
    """
    __tablename__ = "business_type_task_mention"
    __table_args__ = default_table_args
    task_mention_id = Column(ForeignKey("task_mention.id"), primary_key=True)
    business_type_id = Column(ForeignKey("business_type.id"), primary_key=True)
    doctype = Column(String(14), primary_key=True)

    task_mention = relationship(
        "TaskMention",
        backref=backref("business_type_rel", cascade='all, delete-orphan'),
    )
    business_type = relationship(
        "BusinessType",
        backref=backref("task_mention_rel", cascade='all, delete-orphan'),
    )
    mandatory = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': u"Obligatoire",
                "description": u"Si cette mention est obligatoire, elle sera "
                u"automatiquement intégrée dans les PDFs des documents associés"
                u" à ces types d'affaires",
            }
        },
    )
