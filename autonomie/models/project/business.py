# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
)
from sqlalchemy.orm import (
    relationship,
)
from autonomie_base.models.types import (
    PersistentACLMixin,
)
from autonomie_base.models.base import (
    default_table_args,
    DBBASE,
)


class Business(DBBASE, PersistentACLMixin):
    __tablename__ = "business"
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': {'exclude': True}},
    )

    name = Column(
        String(150),
        info={
            "colanderalchemy": {
                "title": u"Nom du sous-projet",
            }
        }
    )

    closed = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': u"Ce sous-projet est-il fermé ?"
            }
        },
    )

    business_type_id = Column(
        ForeignKey('business_type.id'),
        info={'colanderalchemy': {'title': u"Type d'affaires"}}
    )
    project_id = Column(
        ForeignKey('project.id'),
        info={'colanderalchemy': {'exclude': True}},
    )

    business_type = relationship(
        "BusinessType",
        info={'colanderalchemy': {'exclude': True}},
    )
    project = relationship(
        "Project",
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True}
        },
    )
